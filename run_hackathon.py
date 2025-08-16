#!/usr/bin/env python3
"""
🏆 BigQuery AI 해커톤 1위 달성을 위한 통합 실행 스크립트

이 스크립트는 해커톤의 모든 핵심 기능을 순차적으로 실행하여
완벽한 솔루션을 검증합니다.
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HackathonRunner:
    """해커톤 실행 및 검증 클래스"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def run_test(self, test_name: str, command: str, description: str) -> bool:
        """테스트 실행 및 결과 기록"""
        logger.info(f"🧪 실행 중: {test_name}")
        logger.info(f"📝 설명: {description}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            success = result.returncode == 0
            
            self.results[test_name] = {
                "success": success,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "description": description
            }
            
            if success:
                logger.info(f"✅ 성공: {test_name}")
            else:
                logger.error(f"❌ 실패: {test_name}")
                logger.error(f"에러: {result.stderr}")
            
            return success
            
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ 타임아웃: {test_name}")
            self.results[test_name] = {
                "success": False,
                "error": "Timeout",
                "description": description
            }
            return False
        except Exception as e:
            logger.error(f"💥 예외 발생: {test_name} - {e}")
            self.results[test_name] = {
                "success": False,
                "error": str(e),
                "description": description
            }
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """모든 해커톤 테스트 실행"""
        logger.info("🚀 BigQuery AI 해커톤 테스트 시작")
        
        # 1. BigQuery 연결 테스트
        self.run_test(
            "BigQuery 연결",
            "python test_accessible_datasets.py",
            "BigQuery 데이터셋 접근성 확인"
        )
        
        # 2. 가상 임베딩 솔루션 테스트
        self.run_test(
            "가상 임베딩",
            "python pseudo_embedding_solution.py",
            "가상 임베딩 솔루션 검증"
        )
        
        # 3. 외부 임베딩 솔루션 테스트
        self.run_test(
            "외부 임베딩",
            "python external_embedding_solution.py",
            "외부 임베딩 솔루션 검증"
        )
        
        # 4. 최종 ML 모델 테스트
        self.run_test(
            "ML 모델",
            "python final_ml_test.py",
            "최종 ML 모델 성능 검증"
        )
        
        return self.results
    
    def generate_report(self) -> str:
        """테스트 결과 리포트 생성"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get("success", False))
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
🏆 BigQuery AI 해커톤 테스트 결과 리포트
{'='*50}

📊 전체 결과
- 총 테스트: {total_tests}개
- 성공: {successful_tests}개
- 실패: {total_tests - successful_tests}개
- 성공률: {success_rate:.1f}%

⏱️ 실행 시간: {time.time() - self.start_time:.2f}초

📋 상세 결과
"""
        
        for test_name, result in self.results.items():
            status = "✅ 성공" if result.get("success", False) else "❌ 실패"
            report += f"\n{test_name}: {status}"
            if not result.get("success", False):
                error = result.get("error", result.get("stderr", "알 수 없는 오류"))
                report += f"\n  └─ 오류: {error[:100]}..."
        
        # 성공률에 따른 평가
        if success_rate >= 90:
            report += "\n\n🎉 우수! 해커톤 1위 가능성이 높습니다!"
        elif success_rate >= 70:
            report += "\n\n👍 양호! 추가 최적화가 필요합니다."
        elif success_rate >= 50:
            report += "\n\n⚠️ 주의! 주요 문제를 해결해야 합니다."
        else:
            report += "\n\n🚨 위험! 즉시 문제 해결이 필요합니다."
        
        return report
    
    def save_results(self, filename: str = "hackathon_results.json"):
        """결과를 JSON 파일로 저장"""
        output = {
            "timestamp": time.time(),
            "execution_time": time.time() - self.start_time,
            "results": self.results,
            "summary": {
                "total_tests": len(self.results),
                "successful_tests": sum(1 for r in self.results.values() if r.get("success", False)),
                "success_rate": (sum(1 for r in self.results.values() if r.get("success", False)) / len(self.results) * 100) if self.results else 0
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 결과 저장: {filename}")

def main():
    """메인 실행 함수"""
    print("🏆 BigQuery AI 해커톤 1위 달성을 위한 통합 테스트")
    print("="*60)
    
    runner = HackathonRunner()
    
    try:
        # 모든 테스트 실행
        results = runner.run_all_tests()
        
        # 결과 리포트 생성
        report = runner.generate_report()
        print(report)
        
        # 결과 저장
        runner.save_results()
        
        # 성공률 계산
        success_rate = (sum(1 for r in results.values() if r.get("success", False)) / len(results) * 100) if results else 0
        
        if success_rate >= 80:
            print("\n🎯 다음 단계: 성능 최적화 및 하이퍼파라미터 튜닝")
        else:
            print("\n🚨 다음 단계: 실패한 테스트 문제 해결")
            
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단됨")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 예상치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 