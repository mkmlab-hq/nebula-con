# 레전더리 카드 획득 동기 부여 시스템 v1.0
## MKM Lab 핵심 전략: 데이터 기반 AI 진화 및 사용자 참여 극대화

### 1. 시스템 개요

#### 1.1 핵심 철학
- **목표**: 사용자의 '지속적인 참여'와 '양질의 데이터 제공'을 유도
- **비전**: MKM Lab의 '데이터 기반 AI 진화' 및 '지능형 조직' 구현
- **원칙**: 진실성 우선, 투명성 보장, 윤리적 균형

#### 1.2 전략적 가치
- **강력한 사용자 동기 부여**: 희소하고 가치 있는 보상으로 지속적 참여 유도
- **데이터 품질 향상**: 양질의 정보 기록에 대한 보상으로 AI 학습 데이터 확보
- **사용자 유지율 증대**: 목표 지향적 노력으로 장기적 관계 형성
- **커뮤니티 활성화**: 성취감과 자랑거리로 공유 및 상호작용 촉진

### 2. 양질의 정보 측정 시스템

#### 2.1 핵심 측정 지표

##### 2.1.1 기록의 일관성/빈도 (30%)
```typescript
interface ConsistencyMetrics {
  dailyDiaryFrequency: {
    weight: 0.15,
    measurement: 'consecutive_days_with_diary',
    bonus: {
      '7_days': 10,
      '30_days': 25,
      '90_days': 50,
      '365_days': 100
    }
  },
  weeklyAnalysisRequests: {
    weight: 0.10,
    measurement: 'analysis_requests_per_week',
    bonus: {
      '3_requests': 10,
      '5_requests': 20,
      '7_requests': 30
    }
  },
  monthlyEngagement: {
    weight: 0.05,
    measurement: 'active_days_per_month',
    bonus: {
      '20_days': 10,
      '25_days': 20,
      '30_days': 30
    }
  }
}
```

##### 2.1.2 기록의 상세도/완성도 (25%)
```typescript
interface CompletenessMetrics {
  diaryContentLength: {
    weight: 0.10,
    measurement: 'average_words_per_entry',
    bonus: {
      '100_words': 10,
      '200_words': 20,
      '300_words': 30,
      '500_words': 50
    }
  },
  informationDiversity: {
    weight: 0.08,
    measurement: 'unique_categories_covered',
    categories: ['emotion', 'activity', 'diet', 'sleep', 'social', 'work', 'health'],
    bonus: {
      '3_categories': 10,
      '5_categories': 20,
      '7_categories': 30
    }
  },
  requiredFieldsCompletion: {
    weight: 0.07,
    measurement: 'required_fields_filled_percentage',
    requiredFields: ['mood', 'energy', 'stress', 'activities'],
    bonus: {
      '75_percent': 10,
      '90_percent': 20,
      '100_percent': 30
    }
  }
}
```

##### 2.1.3 피드백 참여 (20%)
```typescript
interface FeedbackMetrics {
  aiSolutionFeedback: {
    weight: 0.10,
    measurement: 'feedback_provided_frequency',
    bonus: {
      'weekly_feedback': 10,
      'biweekly_feedback': 20,
      'monthly_feedback': 30
    }
  },
  feedbackQuality: {
    weight: 0.05,
    measurement: 'detailed_feedback_score',
    criteria: ['specificity', 'constructiveness', 'honesty'],
    bonus: {
      'high_quality': 20,
      'medium_quality': 10,
      'low_quality': 0
    }
  },
  communityParticipation: {
    weight: 0.05,
    measurement: 'community_interactions_per_month',
    bonus: {
      '5_interactions': 10,
      '10_interactions': 20,
      '20_interactions': 30
    }
  }
}
```

##### 2.1.4 서비스 기능 활용도 (15%)
```typescript
interface UtilizationMetrics {
  aiAnalysisFeatures: {
    weight: 0.08,
    measurement: 'unique_features_used',
    features: ['face_analysis', 'voice_analysis', 'survey_analysis', 'persona_generation'],
    bonus: {
      '2_features': 10,
      '3_features': 20,
      '4_features': 30
    }
  },
  featureDepth: {
    weight: 0.04,
    measurement: 'deep_feature_usage',
    deepFeatures: ['advanced_analytics', 'trend_analysis', 'comparative_studies'],
    bonus: {
      '1_deep_feature': 10,
      '2_deep_features': 20,
      '3_deep_features': 30
    }
  },
  crossFeatureIntegration: {
    weight: 0.03,
    measurement: 'cross_feature_data_correlation',
    bonus: {
      'high_integration': 20,
      'medium_integration': 10,
      'low_integration': 0
    }
  }
}
```

##### 2.1.5 데이터 일관성 (10%)
```typescript
interface ConsistencyMetrics {
  aiUserAlignment: {
    weight: 0.06,
    measurement: 'ai_analysis_user_record_correlation',
    bonus: {
      'high_correlation': 20,
      'medium_correlation': 10,
      'low_correlation': 0
    }
  },
  temporalConsistency: {
    weight: 0.04,
    measurement: 'data_pattern_consistency_over_time',
    bonus: {
      'high_consistency': 15,
      'medium_consistency': 8,
      'low_consistency': 0
    }
  }
}
```

#### 2.2 종합 점수 계산
```typescript
interface QualityScoreCalculation {
  totalScore: number;
  categoryScores: {
    consistency: number;    // 30%
    completeness: number;   // 25%
    feedback: number;       // 20%
    utilization: number;    // 15%
    dataConsistency: number; // 10%
  };
  bonusPoints: number;
  penaltyPoints: number;
  finalScore: number;
}
```

### 3. 부정행위 방지 및 조작 감지

#### 3.1 다층 감지 시스템

##### 3.1.1 데이터 품질 이상 패턴 감지
```typescript
interface DataQualityFraudDetection {
  suspiciousPatterns: {
    repetitiveContent: {
      threshold: 0.8,
      penalty: -50,
      detection: 'text_similarity_analysis'
    },
    artificialVolume: {
      threshold: 'unusual_activity_spike',
      penalty: -30,
      detection: 'activity_pattern_analysis'
    },
    inconsistentTiming: {
      threshold: 'irregular_timing_patterns',
      penalty: -20,
      detection: 'temporal_consistency_check'
    },
    botLikeBehavior: {
      threshold: 'automated_input_patterns',
      penalty: -100,
      detection: 'behavioral_analysis'
    }
  }
}
```

##### 3.1.2 사용자 행동 패턴 분석
```typescript
interface UserBehaviorAnalysis {
  normalPatterns: [
    'natural_daily_rhythm',
    'gradual_improvement_trends',
    'consistent_engagement_patterns',
    'organic_interaction_timing'
  ],
  suspiciousPatterns: [
    'rapid_score_inflation',
    'artificial_engagement_spikes',
    'coordinated_activity_patterns',
    'manipulation_attempts'
  ],
  riskAssessment: {
    low: 'score_multiplier: 1.0',
    medium: 'score_multiplier: 0.8',
    high: 'score_multiplier: 0.5',
    critical: 'score_multiplier: 0.0, account_review'
  }
}
```

#### 3.2 실시간 모니터링 및 대응
```typescript
interface RealTimeMonitoring {
  immediateActions: {
    fraudDetection: 'session_termination',
    dataInvalidation: 'score_recalculation',
    userNotification: 'transparent_communication',
    adminAlert: 'manual_review_trigger'
  },
  progressivePenalties: {
    firstOffense: 'warning_and_score_reduction',
    secondOffense: 'temporary_restriction',
    thirdOffense: 'permanent_restriction',
    severeOffense: 'account_termination'
  }
}
```

### 4. 점수 시스템과 확률 연동

#### 4.1 투명한 확률 계산
```typescript
interface ProbabilityCalculation {
  baseProbability: {
    Legendary: 0.01,    // 1%
    Epic: 0.05,         // 5%
    Rare: 0.15,         // 15%
    Uncommon: 0.30,     // 30%
    Common: 0.49        // 49%
  },
  qualityScoreMultiplier: {
    '90-100': 2.0,      // 최고 품질: 2배 확률
    '80-89': 1.5,       // 높은 품질: 1.5배 확률
    '70-79': 1.2,       // 양호한 품질: 1.2배 확률
    '60-69': 1.0,       // 기본 품질: 기본 확률
    '50-59': 0.8,       // 낮은 품질: 0.8배 확률
    '0-49': 0.5         // 매우 낮은 품질: 0.5배 확률
  },
  marketAdjustment: {
    saturationFactor: 'current_legendary_distribution',
    demandFactor: 'user_engagement_trends',
    seasonalFactor: 'time_based_adjustments'
  }
}
```

#### 4.2 동적 확률 조정
```typescript
interface DynamicProbabilityAdjustment {
  realTimeFactors: {
    marketSaturation: {
      currentLegendaryCount: number,
      targetDistribution: 0.01,
      adjustmentFactor: number
    },
    userEngagement: {
      activeUserCount: number,
      averageQualityScore: number,
      engagementTrend: 'increasing' | 'stable' | 'decreasing'
    },
    seasonalEvents: {
      specialOccasions: string[],
      eventMultipliers: Record<string, number>
    }
  },
  finalProbability: number;
  transparencyReport: {
    baseProbability: number,
    qualityMultiplier: number,
    marketAdjustment: number,
    finalProbability: number,
    explanation: string
  }
}
```

### 5. 윤리적 고려사항

#### 5.1 건강 본질 유지
```typescript
interface HealthEssencePreservation {
  corePrinciples: [
    'health_improvement_primary_goal',
    'gaming_secondary_motivation',
    'balanced_engagement_encouragement',
    'sustainable_habit_formation'
  ],
  safeguards: {
    excessiveGamingPrevention: {
      dailyTimeLimit: 60, // 분
      weeklySessionLimit: 7,
      healthReminderFrequency: 'every_3_sessions'
    },
    healthFocusReinforcement: {
      healthGoalTracking: true,
      wellnessAchievementCelebration: true,
      medicalAdviceIntegration: true
    }
  }
}
```

#### 5.2 포용적 보상 시스템
```typescript
interface InclusiveRewardSystem {
  alternativeRewards: {
    badges: {
      consistency: '7_day_streak',
      quality: 'detailed_recorder',
      engagement: 'community_contributor',
      health: 'wellness_achiever'
    },
    credits: {
      dailyLogin: 10,
      weeklyGoal: 50,
      monthlyMilestone: 200,
      qualityBonus: 100
    },
    features: {
      premiumAnalysis: 'unlock_advanced_features',
      personalizedInsights: 'custom_ai_recommendations',
      communityAccess: 'exclusive_forums'
    }
  },
  accessibility: {
    languageSupport: ['ko', 'en', 'ja', 'zh'],
    deviceCompatibility: ['mobile', 'tablet', 'desktop'],
    connectivityOptions: ['online', 'offline_sync']
  }
}
```

### 6. 구현 로드맵

#### 6.1 Phase 1: 기본 시스템 (4-6주)
- [ ] 사용자 활동 및 데이터 품질 평가 모듈 개발
- [ ] 기본 점수 계산 시스템 구현
- [ ] 부정행위 감지 기본 로직 구현
- [ ] 확률 계산 시스템 구현

#### 6.2 Phase 2: 고급 기능 (6-8주)
- [ ] 실시간 모니터링 시스템 구축
- [ ] 동적 확률 조정 시스템 구현
- [ ] 투명성 대시보드 개발
- [ ] 사용자 피드백 시스템 통합

#### 6.3 Phase 3: 최적화 및 확장 (8-10주)
- [ ] AI 기반 이상 패턴 감지 강화
- [ ] 시장 균형 시스템 고도화
- [ ] 윤리적 가이드라인 구현
- [ ] 포용적 보상 시스템 완성

### 7. 성공 지표 및 KPI

#### 7.1 사용자 참여 지표
- **일일 활성 사용자 (DAU)**: 목표 30% 증가
- **월간 활성 사용자 (MAU)**: 목표 50% 증가
- **사용자 유지율**: 7일 70%, 30일 50%, 90일 30%
- **평균 세션 시간**: 목표 15분 증가

#### 7.2 데이터 품질 지표
- **평균 다이어리 길이**: 목표 200단어
- **기록 완성도**: 목표 85%
- **기능 활용도**: 목표 3개 이상 기능 사용
- **피드백 참여율**: 목표 60%

#### 7.3 시스템 성능 지표
- **부정행위 감지율**: 목표 95%
- **거짓 양성률**: 목표 5% 이하
- **시스템 응답 시간**: 목표 2초 이하
- **확률 계산 정확도**: 목표 99%

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-07-29  
**작성자**: MKM Lab 전략팀  
**승인자**: 프로젝트 키메라 총괄 지휘관  
**상태**: ✅ **공식 채택** 