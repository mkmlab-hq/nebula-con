#!/usr/bin/env python3
"""
기록의 정수(Essence of Record) 포인트 시스템
사용자의 모든 활동을 가치로 변환하고 측정하는 핵심 엔진
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActivityType(Enum):
    """활동 유형 정의"""
    HEALTH_WALKING = "health_walking"
    HEALTH_EXERCISE = "health_exercise"
    HEALTH_MEDITATION = "health_meditation"
    HEALTH_DIET = "health_diet"
    HEALTH_SLEEP = "health_sleep"
    HEALTH_HYDRATION = "health_hydration"
    CREATIVE_WRITING = "creative_writing"
    CREATIVE_DRAWING = "creative_drawing"
    CREATIVE_MUSIC = "creative_music"
    CREATIVE_PHOTOGRAPHY = "creative_photography"
    LEARNING_READING = "learning_reading"
    LEARNING_STUDY = "learning_study"
    LEARNING_SKILL = "learning_skill"
    SOCIAL_INTERACTION = "social_interaction"
    SOCIAL_HELP = "social_help"
    SOCIAL_SHARING = "social_sharing"

@dataclass
class EssenceActivity:
    """정수 활동 데이터 구조"""
    user_id: str
    activity_type: ActivityType
    essence_points: int
    description: str
    duration_minutes: Optional[int] = None
    intensity_level: Optional[int] = None  # 1-10 스케일
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []

@dataclass
class EssenceBalance:
    """정수 잔액 데이터 구조"""
    user_id: str
    total_essence: int
    available_essence: int
    used_essence: int
    last_updated: datetime
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

class EssenceCalculator:
    """정수 포인트 계산기"""
    
    # 활동별 기본 정수 포인트
    ACTIVITY_BASE_POINTS = {
        ActivityType.HEALTH_WALKING: 10,
        ActivityType.HEALTH_EXERCISE: 25,
        ActivityType.HEALTH_MEDITATION: 15,
        ActivityType.HEALTH_DIET: 5,
        ActivityType.HEALTH_SLEEP: 20,
        ActivityType.HEALTH_HYDRATION: 3,
        ActivityType.CREATIVE_WRITING: 30,
        ActivityType.CREATIVE_DRAWING: 40,
        ActivityType.CREATIVE_MUSIC: 35,
        ActivityType.CREATIVE_PHOTOGRAPHY: 25,
        ActivityType.LEARNING_READING: 20,
        ActivityType.LEARNING_STUDY: 25,
        ActivityType.LEARNING_SKILL: 30,
        ActivityType.SOCIAL_INTERACTION: 15,
        ActivityType.SOCIAL_HELP: 20,
        ActivityType.SOCIAL_SHARING: 10
    }
    
    @staticmethod
    def calculate_essence_points(
        activity_type: ActivityType,
        duration_minutes: Optional[int] = None,
        intensity_level: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> int:
        """정수 포인트 계산"""
        base_points = EssenceCalculator.ACTIVITY_BASE_POINTS.get(activity_type, 10)
        
        # 지속 시간 보너스 (30분 이상 시)
        duration_bonus = 0
        if duration_minutes and duration_minutes >= 30:
            duration_bonus = min(duration_minutes // 30, 5) * 5  # 최대 25점
        
        # 강도 보너스 (강도 7 이상 시)
        intensity_bonus = 0
        if intensity_level and intensity_level >= 7:
            intensity_bonus = (intensity_level - 6) * 3  # 최대 12점
        
        # 태그 보너스 (특별한 태그 시)
        tag_bonus = 0
        if tags:
            special_tags = ['first_time', 'milestone', 'breakthrough', 'consistency']
            tag_bonus = len([tag for tag in tags if tag in special_tags]) * 5
        
        total_points = base_points + duration_bonus + intensity_bonus + tag_bonus
        
        logger.info(f"정수 계산: {activity_type.value} = {base_points} + {duration_bonus} + {intensity_bonus} + {tag_bonus} = {total_points}")
        
        return total_points

class EssenceDatabase:
    """정수 데이터베이스 관리"""
    
    def __init__(self, db_path: str = "essence_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 활동 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS essence_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                essence_points INTEGER NOT NULL,
                description TEXT NOT NULL,
                duration_minutes INTEGER,
                intensity_level INTEGER,
                location TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 잔액 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS essence_balances (
                user_id TEXT PRIMARY KEY,
                total_essence INTEGER DEFAULT 0,
                available_essence INTEGER DEFAULT 0,
                used_essence INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("정수 데이터베이스 초기화 완료")
    
    def add_activity(self, activity: EssenceActivity) -> bool:
        """활동 추가"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO essence_activities 
                (user_id, activity_type, essence_points, description, duration_minutes, 
                 intensity_level, location, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                activity.user_id,
                activity.activity_type.value,
                activity.essence_points,
                activity.description,
                activity.duration_minutes,
                activity.intensity_level,
                activity.location,
                json.dumps(activity.tags),
                activity.created_at.isoformat()
            ))
            
            # 잔액 업데이트
            self._update_balance(activity.user_id, activity.essence_points)
            
            conn.commit()
            conn.close()
            
            logger.info(f"활동 추가 완료: {activity.user_id} - {activity.activity_type.value} ({activity.essence_points}점)")
            return True
            
        except Exception as e:
            logger.error(f"활동 추가 실패: {e}")
            return False
    
    def _update_balance(self, user_id: str, points: int):
        """잔액 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 기존 잔액 확인
        cursor.execute('SELECT total_essence, available_essence, used_essence FROM essence_balances WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            total, available, used = result
            new_total = total + points
            new_available = available + points
        else:
            new_total = points
            new_available = points
            used = 0
        
        # 잔액 업데이트 또는 생성
        cursor.execute('''
            INSERT OR REPLACE INTO essence_balances 
            (user_id, total_essence, available_essence, used_essence, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, new_total, new_available, used, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_balance(self, user_id: str) -> Optional[EssenceBalance]:
        """잔액 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT total_essence, available_essence, used_essence, last_updated 
                FROM essence_balances WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                total, available, used, last_updated = result
                return EssenceBalance(
                    user_id=user_id,
                    total_essence=total,
                    available_essence=available,
                    used_essence=used,
                    last_updated=datetime.fromisoformat(last_updated)
                )
            else:
                return EssenceBalance(
                    user_id=user_id,
                    total_essence=0,
                    available_essence=0,
                    used_essence=0,
                    last_updated=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"잔액 조회 실패: {e}")
            return None
    
    def get_activities(self, user_id: str, limit: int = 50) -> List[EssenceActivity]:
        """활동 내역 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT activity_type, essence_points, description, duration_minutes,
                       intensity_level, location, tags, created_at
                FROM essence_activities 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            activities = []
            for row in cursor.fetchall():
                activity_type, points, desc, duration, intensity, location, tags_json, created_at = row
                
                activity = EssenceActivity(
                    user_id=user_id,
                    activity_type=ActivityType(activity_type),
                    essence_points=points,
                    description=desc,
                    duration_minutes=duration,
                    intensity_level=intensity,
                    location=location,
                    tags=json.loads(tags_json) if tags_json else [],
                    created_at=datetime.fromisoformat(created_at)
                )
                activities.append(activity)
            
            conn.close()
            return activities
            
        except Exception as e:
            logger.error(f"활동 내역 조회 실패: {e}")
            return []
    
    def use_essence(self, user_id: str, points: int) -> bool:
        """정수 사용"""
        try:
            balance = self.get_balance(user_id)
            if not balance or balance.available_essence < points:
                logger.warning(f"정수 부족: {user_id} - 필요: {points}, 보유: {balance.available_essence if balance else 0}")
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE essence_balances 
                SET available_essence = ?, used_essence = ?, last_updated = ?
                WHERE user_id = ?
            ''', (
                balance.available_essence - points,
                balance.used_essence + points,
                datetime.now().isoformat(),
                user_id
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"정수 사용 완료: {user_id} - {points}점 사용")
            return True
            
        except Exception as e:
            logger.error(f"정수 사용 실패: {e}")
            return False

class EssenceSystem:
    """기록의 정수 시스템 메인 클래스"""
    
    def __init__(self, db_path: str = "essence_system.db"):
        self.db = EssenceDatabase(db_path)
        self.calculator = EssenceCalculator()
        logger.info("기록의 정수 시스템 초기화 완료")
    
    def record_activity(
        self,
        user_id: str,
        activity_type: ActivityType,
        description: str,
        duration_minutes: Optional[int] = None,
        intensity_level: Optional[int] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[int]:
        """활동 기록 및 정수 획득"""
        try:
            # 정수 포인트 계산
            essence_points = self.calculator.calculate_essence_points(
                activity_type, duration_minutes, intensity_level, tags
            )
            
            # 활동 생성
            activity = EssenceActivity(
                user_id=user_id,
                activity_type=activity_type,
                essence_points=essence_points,
                description=description,
                duration_minutes=duration_minutes,
                intensity_level=intensity_level,
                location=location,
                tags=tags or []
            )
            
            # 데이터베이스에 저장
            if self.db.add_activity(activity):
                logger.info(f"활동 기록 완료: {user_id} - {activity_type.value} ({essence_points}점)")
                return essence_points
            else:
                logger.error(f"활동 기록 실패: {user_id} - {activity_type.value}")
                return None
                
        except Exception as e:
            logger.error(f"활동 기록 중 오류: {e}")
            return None
    
    def get_user_balance(self, user_id: str) -> Optional[EssenceBalance]:
        """사용자 잔액 조회"""
        return self.db.get_balance(user_id)
    
    def get_user_activities(self, user_id: str, limit: int = 50) -> List[EssenceActivity]:
        """사용자 활동 내역 조회"""
        return self.db.get_activities(user_id, limit)
    
    def use_essence_points(self, user_id: str, points: int) -> bool:
        """정수 포인트 사용"""
        return self.db.use_essence(user_id, points)
    
    def get_activity_stats(self, user_id: str) -> Dict:
        """활동 통계 조회"""
        activities = self.get_user_activities(user_id, limit=1000)
        
        stats = {
            "total_activities": len(activities),
            "total_essence_earned": sum(a.essence_points for a in activities),
            "activity_types": {},
            "daily_averages": {},
            "recent_activity": []
        }
        
        # 활동 유형별 통계
        for activity in activities:
            activity_type = activity.activity_type.value
            if activity_type not in stats["activity_types"]:
                stats["activity_types"][activity_type] = {
                    "count": 0,
                    "total_points": 0,
                    "avg_points": 0
                }
            
            stats["activity_types"][activity_type]["count"] += 1
            stats["activity_types"][activity_type]["total_points"] += activity.essence_points
        
        # 평균 계산
        for activity_type in stats["activity_types"]:
            count = stats["activity_types"][activity_type]["count"]
            total = stats["activity_types"][activity_type]["total_points"]
            stats["activity_types"][activity_type]["avg_points"] = total / count if count > 0 else 0
        
        # 최근 활동 (최근 10개)
        stats["recent_activity"] = [
            {
                "type": a.activity_type.value,
                "points": a.essence_points,
                "description": a.description,
                "created_at": a.created_at.isoformat()
            }
            for a in activities[:10]
        ]
        
        return stats

# 전역 인스턴스
essence_system = EssenceSystem()

def main():
    """테스트 함수"""
    # 테스트 사용자
    test_user = "test_user_001"
    
    # 활동 기록 테스트
    print("=== 기록의 정수 시스템 테스트 ===")
    
    # 1. 건강 활동 기록
    points1 = essence_system.record_activity(
        user_id=test_user,
        activity_type=ActivityType.HEALTH_WALKING,
        description="30분 산책",
        duration_minutes=30,
        intensity_level=5,
        location="공원",
        tags=["first_time", "outdoor"]
    )
    print(f"산책 활동: {points1}점 획득")
    
    # 2. 창작 활동 기록
    points2 = essence_system.record_activity(
        user_id=test_user,
        activity_type=ActivityType.CREATIVE_WRITING,
        description="일기 작성",
        duration_minutes=45,
        intensity_level=8,
        tags=["daily", "reflection"]
    )
    print(f"글쓰기 활동: {points2}점 획득")
    
    # 3. 학습 활동 기록
    points3 = essence_system.record_activity(
        user_id=test_user,
        activity_type=ActivityType.LEARNING_STUDY,
        description="AI 관련 공부",
        duration_minutes=60,
        intensity_level=7,
        tags=["learning", "technology"]
    )
    print(f"학습 활동: {points3}점 획득")
    
    # 잔액 조회
    balance = essence_system.get_user_balance(test_user)
    print(f"\n현재 잔액: {balance.available_essence}점 (총 획득: {balance.total_essence}점)")
    
    # 통계 조회
    stats = essence_system.get_activity_stats(test_user)
    print(f"\n활동 통계:")
    print(f"- 총 활동 수: {stats['total_activities']}")
    print(f"- 총 획득 정수: {stats['total_essence_earned']}")
    
    # 정수 사용 테스트
    if essence_system.use_essence_points(test_user, 50):
        print(f"\n정수 50점 사용 완료")
        new_balance = essence_system.get_user_balance(test_user)
        print(f"남은 잔액: {new_balance.available_essence}점")

if __name__ == "__main__":
    main() 