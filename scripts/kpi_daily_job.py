#!/usr/bin/env python3
"""
엔오건강도우미 KPI 일일 집계 스크립트
운영 대시보드 및 비즈니스 인텔리전스를 위한 핵심 지표 수집

Author: MKM Lab 아테나 & 최고사령관
Version: 1.0
Last Update: 2025-08-11
"""

import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ENOKPICollector:
    """엔오건강도우미 KPI 수집기"""
    
    def __init__(self, db_path: str = "eno_analytics.db"):
        """
        KPI 수집기 초기화
        
        Args:
            db_path: SQLite 데이터베이스 경로
        """
        self.db_path = db_path
        self.kpi_config = self._load_kpi_config()
        self._init_database()
    
    def _load_kpi_config(self) -> Dict:
        """KPI 설정 로드"""
        config_path = "/workspaces/mkm-lab-workspace-config/data/kpi_dashboard_config_v1.0.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"KPI 설정 파일을 찾을 수 없습니다: {config_path}")
            return self._get_default_kpi_config()
    
    def _get_default_kpi_config(self) -> Dict:
        """기본 KPI 설정"""
        return {
            "performance": {
                "response_time_p95": {"target": 1.2, "unit": "seconds"},
                "error_rate": {"target": 4.0, "unit": "percent"},
                "uptime": {"target": 99.5, "unit": "percent"}
            },
            "business": {
                "qr_scan_rate": {"target": 60.0, "unit": "percent"},
                "completion_rate_30d": {"target": 40.0, "unit": "percent"},
                "satisfaction_avg": {"target": 7.5, "unit": "score"},
                "repurchase_rate": {"target": 25.0, "unit": "percent"},
                "nps_score": {"target": 50.0, "unit": "score"}
            },
            "compliance": {
                "medical_term_filter_miss": {"target": 0, "unit": "count"},
                "disclaimer_coverage": {"target": 100.0, "unit": "percent"},
                "data_retention_compliance": {"target": 100.0, "unit": "percent"}
            }
        }
    
    def _init_database(self) -> None:
        """데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            # KPI 일일 집계 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_kpi (
                    date DATE PRIMARY KEY,
                    metric_category VARCHAR(50),
                    metric_name VARCHAR(100),
                    actual_value REAL,
                    target_value REAL,
                    unit VARCHAR(20),
                    status VARCHAR(20),  -- 'ok', 'warning', 'critical'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 엔오플렉스 추적 테이블 (시뮬레이션용)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS enoflex_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id VARCHAR(20),
                    user_token VARCHAR(64),
                    baseline_date DATE,
                    current_phase VARCHAR(20),
                    qr_scanned_at TIMESTAMP,
                    last_measurement_at TIMESTAMP,
                    completion_status VARCHAR(20),  -- 'active', 'completed', 'dropped'
                    satisfaction_score INTEGER,
                    repurchase_intent BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 성능 메트릭 테이블 (시뮬레이션용)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    response_time_ms INTEGER,
                    request_status VARCHAR(10),  -- 'success', 'error'
                    filter_applied BOOLEAN,
                    endpoint VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info("데이터베이스 초기화 완료")
    
    def simulate_daily_data(self, date: str = None) -> None:
        """일일 데이터 시뮬레이션 (테스트용)"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            # 1. 엔오플렉스 사용자 시뮬레이션 (100명)
            for i in range(100):
                user_token = f"USER_{date.replace('-', '')}_{i:03d}"
                product_id = f"ENOFLEX_{random.choice(['202508', '202509'])}"
                
                # QR 스캔 시뮬레이션 (60% 스캔율 목표)
                if random.random() < 0.65:  # 65% 실제 스캔율
                    baseline_date = date
                    
                    # 완주율 시뮬레이션 (40% 목표)
                    completion_status = 'completed' if random.random() < 0.42 else 'active'
                    satisfaction = random.randint(6, 10) if completion_status == 'completed' else None
                    repurchase = random.random() < 0.28 if completion_status == 'completed' else None
                    
                    conn.execute("""
                        INSERT INTO enoflex_tracking 
                        (product_id, user_token, baseline_date, current_phase, 
                         qr_scanned_at, completion_status, satisfaction_score, repurchase_intent)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        product_id, user_token, baseline_date, 'day30' if completion_status == 'completed' else 'day7',
                        f"{date} {random.randint(8, 22):02d}:{random.randint(0, 59):02d}:00",
                        completion_status, satisfaction, repurchase
                    ))
            
            # 2. 성능 메트릭 시뮬레이션 (하루 1000건 요청)
            for i in range(1000):
                # 응답시간 시뮬레이션 (p95 < 1.2초 목표)
                response_time = max(200, random.normalvariate(800, 200))  # 평균 800ms
                
                # 에러율 시뮬레이션 (4% 목표)
                status = 'error' if random.random() < 0.035 else 'success'  # 3.5% 실제 에러율
                
                # 필터 적용 시뮬레이션
                filter_applied = random.random() < 0.15  # 15% 필터 적용
                
                endpoint = random.choice(['/api/v1/measure', '/api/v1/analyze', '/api/v1/report'])
                
                conn.execute("""
                    INSERT INTO performance_metrics 
                    (timestamp, response_time_ms, request_status, filter_applied, endpoint)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    f"{date} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
                    int(response_time), status, filter_applied, endpoint
                ))
            
            conn.commit()
            logger.info(f"일일 데이터 시뮬레이션 완료: {date}")
    
    def calculate_daily_kpi(self, date: str = None) -> Dict:
        """일일 KPI 계산"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        kpi_results = {}
        
        with sqlite3.connect(self.db_path) as conn:
            # 1. 비즈니스 KPI 계산
            # QR 스캔율 (판매 100개 대비 스캔 수)
            total_sold = 100  # 시뮬레이션: 일일 판매량
            scanned_count = conn.execute("""
                SELECT COUNT(*) FROM enoflex_tracking 
                WHERE DATE(qr_scanned_at) = ?
            """, (date,)).fetchone()[0]
            
            qr_scan_rate = (scanned_count / total_sold) * 100
            
            # 30일 완주율
            completed_count = conn.execute("""
                SELECT COUNT(*) FROM enoflex_tracking 
                WHERE completion_status = 'completed' AND baseline_date = ?
            """, (date,)).fetchone()[0]
            
            completion_rate = (completed_count / scanned_count) * 100 if scanned_count > 0 else 0
            
            # 평균 만족도
            avg_satisfaction = conn.execute("""
                SELECT AVG(satisfaction_score) FROM enoflex_tracking 
                WHERE satisfaction_score IS NOT NULL AND baseline_date = ?
            """, (date,)).fetchone()[0] or 0
            
            # 재구매 의향율
            repurchase_count = conn.execute("""
                SELECT COUNT(*) FROM enoflex_tracking 
                WHERE repurchase_intent = 1 AND baseline_date = ?
            """, (date,)).fetchone()[0]
            
            repurchase_rate = (repurchase_count / completed_count) * 100 if completed_count > 0 else 0
            
            # NPS 계산 (9-10점: 추천자, 7-8점: 중립, 6점 이하: 비추천자)
            nps_data = conn.execute("""
                SELECT satisfaction_score FROM enoflex_tracking 
                WHERE satisfaction_score IS NOT NULL AND baseline_date = ?
            """, (date,)).fetchall()
            
            if nps_data:
                promoters = len([s[0] for s in nps_data if s[0] >= 9])
                detractors = len([s[0] for s in nps_data if s[0] <= 6])
                nps_score = ((promoters - detractors) / len(nps_data)) * 100
            else:
                nps_score = 0
            
            # 2. 성능 KPI 계산
            # 응답시간 p95
            response_times = conn.execute("""
                SELECT response_time_ms FROM performance_metrics 
                WHERE DATE(timestamp) = ? AND request_status = 'success'
                ORDER BY response_time_ms
            """, (date,)).fetchall()
            
            if response_times:
                p95_index = int(len(response_times) * 0.95)
                response_time_p95 = response_times[p95_index][0] / 1000  # 초 단위
            else:
                response_time_p95 = 0
            
            # 에러율
            total_requests = conn.execute("""
                SELECT COUNT(*) FROM performance_metrics WHERE DATE(timestamp) = ?
            """, (date,)).fetchone()[0]
            
            error_requests = conn.execute("""
                SELECT COUNT(*) FROM performance_metrics 
                WHERE DATE(timestamp) = ? AND request_status = 'error'
            """, (date,)).fetchone()[0]
            
            error_rate = (error_requests / total_requests) * 100 if total_requests > 0 else 0
            
            # 3. 컴플라이언스 KPI
            # 의료어 필터 누락 (시뮬레이션: 0건 목표)
            filter_miss_count = 0  # 실제로는 로그 분석 필요
            
            # 면책 커버리지 (시뮬레이션: 100% 목표)
            disclaimer_coverage = 100.0  # 실제로는 응답 분석 필요
            
            # 데이터 보관 준수 (시뮬레이션: 100% 목표)
            data_retention_compliance = 100.0  # 실제로는 파기 로그 분석 필요
            
            # KPI 결과 구성
            kpi_results = {
                'business': {
                    'qr_scan_rate': qr_scan_rate,
                    'completion_rate_30d': completion_rate,
                    'satisfaction_avg': avg_satisfaction,
                    'repurchase_rate': repurchase_rate,
                    'nps_score': nps_score
                },
                'performance': {
                    'response_time_p95': response_time_p95,
                    'error_rate': error_rate,
                    'uptime': 99.8  # 시뮬레이션
                },
                'compliance': {
                    'medical_term_filter_miss': filter_miss_count,
                    'disclaimer_coverage': disclaimer_coverage,
                    'data_retention_compliance': data_retention_compliance
                }
            }
        
        return kpi_results
    
    def save_daily_kpi(self, date: str, kpi_results: Dict) -> None:
        """일일 KPI 저장"""
        with sqlite3.connect(self.db_path) as conn:
            for category, metrics in kpi_results.items():
                for metric_name, actual_value in metrics.items():
                    # 목표값 가져오기
                    target_value = self.kpi_config.get(category, {}).get(metric_name, {}).get('target', 0)
                    unit = self.kpi_config.get(category, {}).get(metric_name, {}).get('unit', 'unknown')
                    
                    # 상태 결정
                    if metric_name in ['error_rate', 'medical_term_filter_miss']:
                        # 낮을수록 좋은 지표
                        if actual_value <= target_value:
                            status = 'ok'
                        elif actual_value <= target_value * 1.5:
                            status = 'warning'
                        else:
                            status = 'critical'
                    else:
                        # 높을수록 좋은 지표
                        if actual_value >= target_value:
                            status = 'ok'
                        elif actual_value >= target_value * 0.8:
                            status = 'warning'
                        else:
                            status = 'critical'
                    
                    # DB 저장
                    conn.execute("""
                        INSERT OR REPLACE INTO daily_kpi 
                        (date, metric_category, metric_name, actual_value, target_value, unit, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (date, category, metric_name, actual_value, target_value, unit, status))
            
            conn.commit()
            logger.info(f"일일 KPI 저장 완료: {date}")
    
    def generate_kpi_report(self, date: str = None) -> str:
        """일일 KPI 리포트 생성"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        kpi_results = self.calculate_daily_kpi(date)
        
        report = f"""
=== 엔오건강도우미 일일 KPI 리포트 ===
날짜: {date}
생성시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 비즈니스 KPI
"""
        
        for category, metrics in kpi_results.items():
            if category == 'business':
                report += "\n📈 비즈니스 지표:\n"
            elif category == 'performance':
                report += "\n⚡ 성능 지표:\n"
            elif category == 'compliance':
                report += "\n⚖️ 컴플라이언스 지표:\n"
            
            for metric_name, actual_value in metrics.items():
                target = self.kpi_config.get(category, {}).get(metric_name, {}).get('target', 0)
                unit = self.kpi_config.get(category, {}).get(metric_name, {}).get('unit', '')
                
                # 상태 이모지
                if metric_name in ['error_rate', 'medical_term_filter_miss']:
                    status_emoji = "✅" if actual_value <= target else "⚠️" if actual_value <= target * 1.5 else "🚨"
                else:
                    status_emoji = "✅" if actual_value >= target else "⚠️" if actual_value >= target * 0.8 else "🚨"
                
                report += f"  {status_emoji} {metric_name}: {actual_value:.1f}{unit} (목표: {target}{unit})\n"
        
        # 요약
        critical_count = sum(1 for category in kpi_results.values() 
                           for metric_name, actual_value in category.items()
                           if (metric_name in ['error_rate', 'medical_term_filter_miss'] and actual_value > self.kpi_config.get('compliance', {}).get(metric_name, {}).get('target', 0) * 1.5)
                           or (metric_name not in ['error_rate', 'medical_term_filter_miss'] and actual_value < self.kpi_config.get('business', {}).get(metric_name, {}).get('target', 0) * 0.8))
        
        warning_count = sum(1 for category in kpi_results.values() 
                          for metric_name, actual_value in category.items()
                          if (metric_name in ['error_rate', 'medical_term_filter_miss'] and self.kpi_config.get('compliance', {}).get(metric_name, {}).get('target', 0) < actual_value <= self.kpi_config.get('compliance', {}).get(metric_name, {}).get('target', 0) * 1.5)
                          or (metric_name not in ['error_rate', 'medical_term_filter_miss'] and self.kpi_config.get('business', {}).get(metric_name, {}).get('target', 0) * 0.8 <= actual_value < self.kpi_config.get('business', {}).get(metric_name, {}).get('target', 0)))
        
        report += f"""
📋 요약:
- 🚨 Critical: {critical_count}개 지표
- ⚠️ Warning: {warning_count}개 지표
- ✅ Normal: {sum(len(metrics) for metrics in kpi_results.values()) - critical_count - warning_count}개 지표

🎯 권장 액션:
"""
        
        if critical_count > 0:
            report += "- 🚨 Critical 지표 즉시 점검 및 개선 필요\n"
        if warning_count > 0:
            report += "- ⚠️ Warning 지표 모니터링 강화 필요\n"
        if critical_count == 0 and warning_count == 0:
            report += "- ✅ 모든 지표 정상 범위, 현재 운영 유지\n"
        
        report += f"""
📊 상세 대시보드: http://monitoring.mkmlab.com/enoflex
🔔 알럿 설정: Slack #eno-alerts
📝 상세 로그: Grafana ENO Dashboard
"""
        
        return report
    
    def run_daily_job(self, date: str = None) -> str:
        """일일 KPI 집계 작업 실행"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"일일 KPI 집계 시작: {date}")
        
        # 1. 데이터 시뮬레이션 (실제 환경에서는 제거)
        self.simulate_daily_data(date)
        
        # 2. KPI 계산
        kpi_results = self.calculate_daily_kpi(date)
        
        # 3. KPI 저장
        self.save_daily_kpi(date, kpi_results)
        
        # 4. 리포트 생성
        report = self.generate_kpi_report(date)
        
        logger.info(f"일일 KPI 집계 완료: {date}")
        return report


if __name__ == "__main__":
    # 일일 KPI 수집 실행
    collector = ENOKPICollector()
    
    # 테스트: 최근 3일간 데이터 생성
    for i in range(3):
        test_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        report = collector.run_daily_job(test_date)
        print(f"\n{report}")
        print("=" * 80)
