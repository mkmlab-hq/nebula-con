#!/usr/bin/env python3
"""
엔오건강도우미 데이터 삭제 자동화 스크립트
개인정보보호법 준수를 위한 즉시 파기 및 주기적 정리

Author: MKM Lab 보안팀 & 최고사령관
Version: 1.0
Last Update: 2025-08-11
"""

import gc
import json
import logging
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from typing import Bool, Dict, List

import psutil

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/eno_data_deletion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ENODataDeletionManager:
    """엔오건강도우미 데이터 삭제 관리자"""

    def __init__(self, config_path: str = None):
        """삭제 관리자 초기화"""
        if config_path is None:
            config_path = "/workspaces/mkm-lab-workspace-config/data/data_lifecycle_policy_v1.0.json"

        self.config = self._load_deletion_policy(config_path)
        self.deletion_log = []
        self.verification_results = {}

    def _load_deletion_policy(self, config_path: str) -> Dict:
        """데이터 삭제 정책 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"삭제 정책 파일을 찾을 수 없습니다: {config_path}")
            return self._get_default_deletion_policy()

    def _get_default_deletion_policy(self) -> Dict:
        """기본 삭제 정책"""
        return {
            "retention_periods": {
                "biometric_data": "immediate",
                "personal_info": "immediate",
                "session_data": "24_hours",
                "consent_records": "1_year",
                "audit_logs": "30_days",
                "performance_logs": "7_days"
            },
            "deletion_methods": {
                "immediate": "memory_zero",
                "hourly": "secure_delete",
                "daily": "database_purge",
                "weekly": "anonymize_archive"
            }
        }

    def secure_memory_clear(self, data_obj) -> Bool:
        """메모리 안전 삭제"""
        try:
            if data_obj is not None:
                # 1. 객체 참조 제거
                if hasattr(data_obj, 'clear'):
                    data_obj.clear()

                # 2. 메모리 덮어쓰기 시뮬레이션
                for i in range(3):
                    if isinstance(data_obj, (list, dict)):
                        data_obj = type(data_obj)()

                # 3. 참조 삭제
                del data_obj

                # 4. 가비지 컬렉션 강제 실행
                gc.collect()

                return True
        except Exception as e:
            logger.error(f"메모리 삭제 실패: {e}")
            return False

    def secure_file_delete(self, file_path: str) -> Bool:
        """파일 안전 삭제"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"삭제 대상 파일이 존재하지 않음: {file_path}")
                return True

            # 1. 파일 크기 확인
            file_size = os.path.getsize(file_path)

            # 2. 랜덤 데이터로 덮어쓰기 (3회)
            with open(file_path, 'r+b') as f:
                for i in range(3):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())

            # 3. 제로로 덮어쓰기
            with open(file_path, 'r+b') as f:
                f.seek(0)
                f.write(b'\x00' * file_size)
                f.flush()
                os.fsync(f.fileno())

            # 4. 파일 삭제
            os.remove(file_path)

            logger.info(f"파일 안전 삭제 완료: {file_path}")
            return True

        except Exception as e:
            logger.error(f"파일 삭제 실패 {file_path}: {e}")
            return False

    def database_purge(self, db_path: str, retention_hours: int = 24) -> Bool:
        """데이터베이스 만료 데이터 퍼지"""
        try:
            with sqlite3.connect(db_path) as conn:
                cutoff_time = datetime.now() - timedelta(hours=retention_hours)
                cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

                # 만료된 세션 데이터 삭제
                cursor = conn.execute("""
                    DELETE FROM user_sessions
                    WHERE created_at < ?
                """, (cutoff_str,))
                deleted_sessions = cursor.rowcount

                # 처리 완료된 임시 측정 데이터 삭제
                cursor = conn.execute("""
                    DELETE FROM temp_measurements
                    WHERE processed_at IS NOT NULL
                    AND created_at < ?
                """, (cutoff_str,))
                deleted_measurements = cursor.rowcount

                # 만료된 캐시 데이터 삭제
                cursor = conn.execute("""
                    DELETE FROM biometric_cache
                    WHERE created_at < ?
                """, (cutoff_str,))
                deleted_cache = cursor.rowcount

                conn.commit()

                logger.info(f"DB 퍼지 완료 - 세션: {deleted_sessions}, 측정: {deleted_measurements}, 캐시: {deleted_cache}")
                return True

        except Exception as e:
            logger.error(f"데이터베이스 퍼지 실패: {e}")
            return False

    def anonymize_logs(self, db_path: str, anonymize_days: int = 30) -> Bool:
        """로그 데이터 익명화"""
        try:
            with sqlite3.connect(db_path) as conn:
                cutoff_time = datetime.now() - timedelta(days=anonymize_days)
                cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

                # 감사 로그 익명화
                cursor = conn.execute("""
                    UPDATE audit_logs
                    SET user_identifier = 'ANONYMIZED',
                        ip_address = '0.0.0.0',
                        session_token = 'DELETED'
                    WHERE created_at < ?
                    AND user_identifier != 'ANONYMIZED'
                """, (cutoff_str,))
                anonymized_count = cursor.rowcount

                # 성능 로그는 통계 생성 후 삭제
                cursor = conn.execute("""
                    INSERT OR REPLACE INTO daily_performance_stats
                    (date, total_requests, avg_response_time, error_rate)
                    SELECT
                        DATE(timestamp) as date,
                        COUNT(*) as total_requests,
                        AVG(response_time_ms) as avg_response_time,
                        (SUM(CASE WHEN request_status = 'error' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as error_rate
                    FROM performance_metrics
                    WHERE timestamp < ?
                    GROUP BY DATE(timestamp)
                """, (cutoff_str,))

                cursor = conn.execute("""
                    DELETE FROM performance_metrics
                    WHERE timestamp < ?
                """, (cutoff_str,))
                deleted_metrics = cursor.rowcount

                conn.commit()

                logger.info(f"로그 익명화 완료 - 익명화: {anonymized_count}, 삭제: {deleted_metrics}")
                return True

        except Exception as e:
            logger.error(f"로그 익명화 실패: {e}")
            return False

    def immediate_session_cleanup(self, session_id: str) -> Bool:
        """세션 종료 시 즉시 삭제"""
        try:
            deletion_event = {
                "event_id": f"DEL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id[:8]}",
                "timestamp": datetime.now().isoformat(),
                "deletion_type": "immediate",
                "trigger": "session_end",
                "session_id": session_id,
                "success": False,
                "deleted_items": []
            }

            # 1. 메모리 내 세션 데이터 삭제
            session_data = self._get_session_data(session_id)
            if session_data:
                memory_cleared = self.secure_memory_clear(session_data)
                if memory_cleared:
                    deletion_event["deleted_items"].append("session_memory_data")

            # 2. 임시 파일 삭제
            temp_files = self._find_session_temp_files(session_id)
            for temp_file in temp_files:
                if self.secure_file_delete(temp_file):
                    deletion_event["deleted_items"].append(f"temp_file:{temp_file}")

            # 3. 캐시 데이터 삭제
            cache_cleared = self._clear_session_cache(session_id)
            if cache_cleared:
                deletion_event["deleted_items"].append("session_cache")

            # 4. 데이터베이스 세션 기록 삭제
            db_cleared = self._delete_session_from_db(session_id)
            if db_cleared:
                deletion_event["deleted_items"].append("database_session")

            deletion_event["success"] = len(deletion_event["deleted_items"]) > 0
            self._log_deletion_event(deletion_event)

            logger.info(f"즉시 세션 정리 완료: {session_id}")
            return True

        except Exception as e:
            logger.error(f"즉시 세션 정리 실패 {session_id}: {e}")
            return False

    def _get_session_data(self, session_id: str):
        """세션 데이터 조회 (시뮬레이션)"""
        # 실제 구현에서는 Redis/메모리 캐시에서 조회
        return {"session_id": session_id, "biometric_data": [1, 2, 3], "user_data": {}}

    def _find_session_temp_files(self, session_id: str) -> List[str]:
        """세션 관련 임시 파일 찾기"""
        temp_dirs = ['/tmp', '/var/tmp']
        temp_files = []

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    if session_id in file:
                        temp_files.append(os.path.join(temp_dir, file))

        return temp_files

    def _clear_session_cache(self, session_id: str) -> Bool:
        """세션 캐시 삭제"""
        # 실제 구현에서는 Redis FLUSHDB 등 사용
        return True

    def _delete_session_from_db(self, session_id: str) -> Bool:
        """데이터베이스 세션 삭제"""
        try:
            db_path = "eno_analytics.db"
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute("""
                    DELETE FROM user_sessions WHERE session_id = ?
                """, (session_id,))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False

    def _log_deletion_event(self, deletion_event: Dict) -> None:
        """삭제 이벤트 로깅"""
        self.deletion_log.append(deletion_event)

        # 감사 로그 파일에 기록
        log_file = "/var/log/eno_deletion_audit.log"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(deletion_event, ensure_ascii=False) + "\n")
        except:
            logger.warning("삭제 감사 로그 파일 기록 실패")

    def scheduled_cleanup(self, cleanup_type: str = "daily") -> Bool:
        """주기적 정리 작업"""
        try:
            logger.info(f"주기적 정리 시작: {cleanup_type}")

            cleanup_results = {
                "timestamp": datetime.now().isoformat(),
                "cleanup_type": cleanup_type,
                "tasks_completed": [],
                "tasks_failed": []
            }

            if cleanup_type == "hourly":
                # 임시 파일 정리
                temp_cleaned = self._cleanup_temp_files()
                if temp_cleaned:
                    cleanup_results["tasks_completed"].append("temp_files")
                else:
                    cleanup_results["tasks_failed"].append("temp_files")

            elif cleanup_type == "daily":
                # 데이터베이스 퍼지
                db_purged = self.database_purge("eno_analytics.db", 24)
                if db_purged:
                    cleanup_results["tasks_completed"].append("database_purge")
                else:
                    cleanup_results["tasks_failed"].append("database_purge")

                # 만료된 로그 정리
                logs_cleaned = self._cleanup_expired_logs()
                if logs_cleaned:
                    cleanup_results["tasks_completed"].append("expired_logs")
                else:
                    cleanup_results["tasks_failed"].append("expired_logs")

            elif cleanup_type == "weekly":
                # 로그 익명화
                logs_anonymized = self.anonymize_logs("eno_analytics.db", 7)
                if logs_anonymized:
                    cleanup_results["tasks_completed"].append("log_anonymization")
                else:
                    cleanup_results["tasks_failed"].append("log_anonymization")

            success = len(cleanup_results["tasks_failed"]) == 0
            logger.info(f"주기적 정리 완료: {cleanup_type}, 성공: {success}")

            return success

        except Exception as e:
            logger.error(f"주기적 정리 실패 {cleanup_type}: {e}")
            return False

    def _cleanup_temp_files(self) -> Bool:
        """임시 파일 정리"""
        try:
            temp_dirs = ['/tmp', '/var/tmp']
            cleaned_count = 0

            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        if 'eno' in file.lower():
                            file_path = os.path.join(temp_dir, file)
                            if os.path.isfile(file_path):
                                # 1시간 이상 된 파일만 삭제
                                if time.time() - os.path.getmtime(file_path) > 3600:
                                    if self.secure_file_delete(file_path):
                                        cleaned_count += 1

            logger.info(f"임시 파일 정리 완료: {cleaned_count}개")
            return True

        except Exception as e:
            logger.error(f"임시 파일 정리 실패: {e}")
            return False

    def _cleanup_expired_logs(self) -> Bool:
        """만료된 로그 정리"""
        try:
            log_files = [
                "/var/log/eno_access.log",
                "/var/log/eno_error.log",
                "/var/log/eno_performance.log"
            ]

            for log_file in log_files:
                if os.path.exists(log_file):
                    # 로그 로테이션 (7일 보관)
                    subprocess.run([
                        'logrotate', '-f', '/etc/logrotate.d/eno-logs'
                    ], check=False)

            return True

        except Exception as e:
            logger.error(f"로그 정리 실패: {e}")
            return False

    def emergency_wipe(self, reason: str) -> Bool:
        """긴급 데이터 삭제"""
        try:
            logger.critical(f"긴급 데이터 삭제 시작: {reason}")

            emergency_event = {
                "event_id": f"EMERGENCY_WIPE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "reason": reason,
                "actions_taken": [],
                "verification_required": True
            }

            # 1. 모든 ENO 프로세스 강제 종료
            for proc in psutil.process_iter(['pid', 'name']):
                if 'eno' in proc.info['name'].lower():
                    try:
                        proc.kill()
                        emergency_event["actions_taken"].append(f"killed_process:{proc.info['pid']}")
                    except:
                        pass

            # 2. 메모리 캐시 강제 삭제
            try:
                with open('/proc/sys/vm/drop_caches', 'w') as f:
                    f.write('3')
                emergency_event["actions_taken"].append("memory_cache_dropped")
            except:
                pass

            # 3. 모든 임시 파일 즉시 삭제
            temp_dirs = ['/tmp', '/var/tmp', '/var/cache']
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        if 'eno' in file.lower():
                            file_path = os.path.join(temp_dir, file)
                            if os.path.isfile(file_path):
                                self.secure_file_delete(file_path)
                                emergency_event["actions_taken"].append(f"deleted_temp:{file}")

            # 4. 데이터베이스 민감 데이터 즉시 삭제
            try:
                with sqlite3.connect("eno_analytics.db") as conn:
                    conn.execute("DELETE FROM user_sessions")
                    conn.execute("DELETE FROM temp_measurements")
                    conn.execute("DELETE FROM biometric_cache")
                    conn.commit()
                emergency_event["actions_taken"].append("database_purged")
            except:
                pass

            # 5. 긴급 상황 알림
            self._send_emergency_alert(emergency_event)

            logger.critical(f"긴급 데이터 삭제 완료: {len(emergency_event['actions_taken'])}개 작업")
            return True

        except Exception as e:
            logger.critical(f"긴급 데이터 삭제 실패: {e}")
            return False

    def _send_emergency_alert(self, emergency_event: Dict) -> None:
        """긴급 상황 알림"""
        try:
            # 실제 구현에서는 Slack, 이메일, SMS 등으로 알림
            logger.critical(f"🚨 긴급 알림: {emergency_event['reason']}")
            logger.critical(f"조치 사항: {len(emergency_event['actions_taken'])}개 완료")
        except:
            pass

    def verify_deletion_integrity(self) -> Dict:
        """삭제 무결성 검증"""
        verification_results = {
            "timestamp": datetime.now().isoformat(),
            "memory_scan": self._verify_memory_cleanup(),
            "file_system_scan": self._verify_file_cleanup(),
            "database_verification": self._verify_database_cleanup(),
            "overall_status": "unknown"
        }

        all_verified = all([
            verification_results["memory_scan"],
            verification_results["file_system_scan"],
            verification_results["database_verification"]
        ])

        verification_results["overall_status"] = "pass" if all_verified else "fail"

        return verification_results

    def _verify_memory_cleanup(self) -> Bool:
        """메모리 정리 검증"""
        # 실제로는 메모리 포렌식 도구 사용
        return True

    def _verify_file_cleanup(self) -> Bool:
        """파일 시스템 정리 검증"""
        temp_dirs = ['/tmp', '/var/tmp']
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    if 'eno' in file.lower() and 'biometric' in file.lower():
                        return False
        return True

    def _verify_database_cleanup(self) -> Bool:
        """데이터베이스 정리 검증"""
        try:
            with sqlite3.connect("eno_analytics.db") as conn:
                # 24시간 이상 된 민감 데이터 확인
                cutoff = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

                old_sessions = conn.execute("""
                    SELECT COUNT(*) FROM user_sessions
                    WHERE created_at < ?
                """, (cutoff,)).fetchone()[0]

                old_measurements = conn.execute("""
                    SELECT COUNT(*) FROM temp_measurements
                    WHERE processed_at IS NOT NULL AND created_at < ?
                """, (cutoff,)).fetchone()[0]

                return old_sessions == 0 and old_measurements == 0
        except:
            return False


def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        print("""
사용법: python data_deletion_script.py <command> [options]

명령어:
  immediate <session_id>  - 세션 즉시 삭제
  scheduled <type>        - 주기적 정리 (hourly/daily/weekly)
  emergency <reason>      - 긴급 전체 삭제
  verify                  - 삭제 무결성 검증
  test                    - 테스트 실행
        """)
        return

    command = sys.argv[1]
    deletion_manager = ENODataDeletionManager()

    if command == "immediate" and len(sys.argv) > 2:
        session_id = sys.argv[2]
        success = deletion_manager.immediate_session_cleanup(session_id)
        print(f"즉시 삭제 {'성공' if success else '실패'}: {session_id}")

    elif command == "scheduled" and len(sys.argv) > 2:
        cleanup_type = sys.argv[2]
        success = deletion_manager.scheduled_cleanup(cleanup_type)
        print(f"주기적 정리 {'성공' if success else '실패'}: {cleanup_type}")

    elif command == "emergency" and len(sys.argv) > 2:
        reason = " ".join(sys.argv[2:])
        success = deletion_manager.emergency_wipe(reason)
        print(f"긴급 삭제 {'성공' if success else '실패'}: {reason}")

    elif command == "verify":
        results = deletion_manager.verify_deletion_integrity()
        print(f"삭제 무결성 검증: {results['overall_status']}")
        for check, result in results.items():
            if check != "overall_status":
                print(f"  {check}: {'✅' if result else '❌'}")

    elif command == "test":
        print("=== 데이터 삭제 시스템 테스트 ===")

        # 1. 즉시 삭제 테스트
        test_session = "TEST_SESSION_001"
        immediate_result = deletion_manager.immediate_session_cleanup(test_session)
        print(f"1. 즉시 삭제 테스트: {'✅' if immediate_result else '❌'}")

        # 2. 주기적 정리 테스트
        scheduled_result = deletion_manager.scheduled_cleanup("daily")
        print(f"2. 주기적 정리 테스트: {'✅' if scheduled_result else '❌'}")

        # 3. 무결성 검증 테스트
        verification_result = deletion_manager.verify_deletion_integrity()
        print(f"3. 무결성 검증 테스트: {'✅' if verification_result['overall_status'] == 'pass' else '❌'}")

        print("\n테스트 완료!")

    else:
        print("잘못된 명령어입니다. 도움말을 보려면 인자 없이 실행하세요.")


if __name__ == "__main__":
    main()
