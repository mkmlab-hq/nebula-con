#!/usr/bin/env python3
"""
MKM Lab - 12체질론 기반 AI 두뇌 훈련 시스템
전통 한의학 지식과 최신 과학을 융합한 통합 지능 페르소나 AI
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConstitutionAIBrain:
    """12체질론 기반 AI 두뇌 훈련 시스템"""
    
    def __init__(self):
        """AI 두뇌 초기화"""
        try:
            # Google Gemini API 설정
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                logger.error("❌ GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다")
                self.model = None
                return
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # 12체질론 지식베이스 로드
            self.constitution_knowledge = self._load_constitution_knowledge()
            
            # 의학 RAG 시스템 로드
            try:
                from medical_rag_system import medical_rag_system
                self.medical_rag = medical_rag_system
            except ImportError:
                self.medical_rag = None
                logger.warning("⚠️ 의학 RAG 시스템을 로드할 수 없습니다")
            
            logger.info("✅ 12체질론 AI 두뇌 훈련 시스템 초기화 완료")
            
        except Exception as e:
            logger.error(f"❌ AI 두뇌 초기화 실패: {e}")
            self.model = None
            self.constitution_knowledge = {}
    
    def _load_constitution_knowledge(self) -> Dict[str, Any]:
        """12체질론 지식베이스 로드"""
        try:
            # 12체질 기본 분류 체계
            constitution_types = {
                "태양인": {
                    "A1": {
                        "name": "태양인 기본형 - 활력의 원천",
                        "description": "양기가 가장 강한 체질로 활력이 넘치고 열정적입니다.",
                        "신체적_특성": ["활력이 넘침", "체온이 높음", "대사가 빠름", "근육이 발달함"],
                        "심리적_특성": ["적극적", "리더십", "열정적", "도전적"],
                        "건강_관리": ["열을 내리는 음식", "차가운 성질의 운동", "서늘한 환경"],
                        "약점": ["과열", "성급함", "스트레스 민감", "불면증"],
                        "강점": ["에너지", "추진력", "열정", "리더십"],
                        "장부_특성": "폐대간소(肺大肝小)",
                        "기혈수_특성": "기(氣)가 과다하고 혈(血)이 빠름"
                    },
                    "A2": {
                        "name": "태양인 변증형 - 균형의 추구자",
                        "description": "태양인의 기본 특성을 유지하면서도 균형을 추구하는 체질입니다.",
                        "신체적_특성": ["활력이 있음", "체온이 적당함", "균형잡힌 체형"],
                        "심리적_특성": ["적극적", "균형감각", "조화로움", "협력적"],
                        "건강_관리": ["균형잡힌 식단", "중간 강도 운동", "적당한 휴식"],
                        "약점": ["과열 경향", "완벽주의", "스트레스"],
                        "강점": ["에너지", "균형감각", "협력성", "조화로움"],
                        "장부_특성": "폐대간소(肺大肝小) - 균형형",
                        "기혈수_특성": "기(氣)와 혈(血)이 균형"
                    },
                    "A3": {
                        "name": "태양인 복증형 - 열정의 화신",
                        "description": "태양인의 특성이 가장 강하게 나타나는 복합적 체질입니다.",
                        "신체적_특성": ["매우 활력이 넘침", "체온이 매우 높음", "대사가 매우 빠름"],
                        "심리적_특성": ["매우 적극적", "강한 리더십", "극도로 열정적"],
                        "건강_관리": ["강한 열을 내리는 음식", "차가운 성질의 운동", "시원한 환경"],
                        "약점": ["극도의 과열", "성급함", "스트레스 민감", "불면증"],
                        "강점": ["극도의 에너지", "강한 추진력", "열정", "리더십"],
                        "장부_특성": "폐대간소(肺大肝小) - 복합형",
                        "기혈수_특성": "기(氣)가 매우 과다하고 혈(血)이 매우 빠름"
                    }
                },
                "소양인": {
                    "C1": {
                        "name": "소양인 기본형 - 창조의 예술가",
                        "description": "창의적이고 예술적 감각이 뛰어난 체질입니다.",
                        "신체적_특성": ["균형잡힌 체형", "예민한 감각", "창의적 표현력"],
                        "심리적_특성": ["창의적", "예술적", "감성적", "직관적"],
                        "건강_관리": ["창의적 활동", "예술적 표현", "감성적 휴식"],
                        "약점": ["감정 기복", "예민함", "스트레스 민감"],
                        "강점": ["창의성", "예술성", "직관력", "감성"],
                        "장부_특성": "비대신소(脾大腎小)",
                        "기혈수_특성": "기(氣)가 창의적이고 혈(血)이 감성적"
                    },
                    "C2": {
                        "name": "소양인 변증형 - 적응의 달인",
                        "description": "소양인의 기본 특성을 유지하면서도 적응력이 뛰어난 체질입니다.",
                        "신체적_특성": ["적응력이 좋음", "균형잡힌 체형", "유연한 신체"],
                        "심리적_특성": ["적응력", "창의적", "균형감각", "협력적"],
                        "건강_관리": ["적응력 있는 활동", "균형잡힌 생활", "창의적 표현"],
                        "약점": ["감정 기복", "예민함", "스트레스"],
                        "강점": ["적응력", "창의성", "균형감각", "협력성"],
                        "장부_특성": "비대신소(脾大腎小) - 적응형",
                        "기혈수_특성": "기(氣)와 혈(血)이 적응적"
                    },
                    "C3": {
                        "name": "소양인 복증형 - 혁신의 선구자",
                        "description": "소양인의 특성이 가장 강하게 나타나는 혁신적 체질입니다.",
                        "신체적_특성": ["매우 창의적", "혁신적 체형", "예민한 감각"],
                        "심리적_특성": ["매우 창의적", "혁신적", "예술적", "직관적"],
                        "건강_관리": ["혁신적 활동", "예술적 표현", "창의적 휴식"],
                        "약점": ["극도의 감정 기복", "매우 예민함", "스트레스 민감"],
                        "강점": ["극도의 창의성", "혁신성", "예술성", "직관력"],
                        "장부_특성": "비대신소(脾大腎小) - 혁신형",
                        "기혈수_특성": "기(氣)가 매우 창의적이고 혈(血)이 매우 감성적"
                    }
                },
                "태음인": {
                    "R1": {
                        "name": "태음인 기본형 - 안정의 기둥",
                        "description": "안정적이고 신뢰할 수 있는 체질입니다.",
                        "신체적_특성": ["안정적 체형", "근육이 발달함", "체력이 좋음"],
                        "심리적_특성": ["안정적", "신뢰할 수 있음", "책임감", "인내심"],
                        "건강_관리": ["안정적인 운동", "규칙적인 생활", "충분한 휴식"],
                        "약점": ["경직성", "보수적", "변화 싫어함"],
                        "강점": ["안정성", "신뢰성", "책임감", "인내심"],
                        "장부_특성": "간대폐소(肝大肺小)",
                        "기혈수_특성": "기(氣)가 안정적이고 혈(血)이 충실함"
                    },
                    "R2": {
                        "name": "태음인 변증형 - 조화의 중재자",
                        "description": "태음인의 기본 특성을 유지하면서도 조화를 추구하는 체질입니다.",
                        "신체적_특성": ["균형잡힌 체형", "안정적", "조화로움"],
                        "심리적_특성": ["조화로움", "중재능력", "안정적", "협력적"],
                        "건강_관리": ["조화로운 활동", "균형잡힌 생활", "협력적 운동"],
                        "약점": ["경직성", "보수적", "변화 싫어함"],
                        "강점": ["조화로움", "중재능력", "안정성", "협력성"],
                        "장부_특성": "간대폐소(肝大肺小) - 조화형",
                        "기혈수_특성": "기(氣)와 혈(血)이 조화로움"
                    },
                    "R3": {
                        "name": "태음인 복증형 - 지혜의 산",
                        "description": "태음인의 특성이 가장 강하게 나타나는 지혜로운 체질입니다.",
                        "신체적_특성": ["매우 안정적", "지혜로운 체형", "근육이 매우 발달함"],
                        "심리적_특성": ["매우 안정적", "지혜로움", "강한 책임감", "인내심"],
                        "건강_관리": ["지혜로운 활동", "안정적인 생활", "충분한 휴식"],
                        "약점": ["극도의 경직성", "매우 보수적", "변화 싫어함"],
                        "강점": ["극도의 안정성", "지혜로움", "강한 책임감", "인내심"],
                        "장부_특성": "간대폐소(肝大肺小) - 지혜형",
                        "기혈수_특성": "기(氣)가 매우 안정적이고 혈(血)이 매우 충실함"
                    }
                },
                "소음인": {
                    "V1": {
                        "name": "소음인 기본형 - 섬세한 감성가",
                        "description": "섬세하고 감성적인 체질입니다.",
                        "신체적_특성": ["섬세한 체형", "감성적", "예민한 감각"],
                        "심리적_특성": ["섬세함", "감성적", "예민함", "직관적"],
                        "건강_관리": ["섬세한 활동", "감성적 표현", "예민한 휴식"],
                        "약점": ["과민함", "스트레스 민감", "피로함"],
                        "강점": ["섬세함", "감성", "예민함", "직관력"],
                        "장부_특성": "신대비소(腎大脾小)",
                        "기혈수_특성": "기(氣)가 섬세하고 혈(血)이 감성적"
                    },
                    "V2": {
                        "name": "소음인 변증형 - 균형의 조화가",
                        "description": "소음인의 기본 특성을 유지하면서도 균형을 추구하는 체질입니다.",
                        "신체적_특성": ["균형잡힌 체형", "섬세함", "조화로움"],
                        "심리적_특성": ["균형감각", "섬세함", "조화로움", "협력적"],
                        "건강_관리": ["균형잡힌 활동", "섬세한 생활", "조화로운 휴식"],
                        "약점": ["과민함", "스트레스 민감", "피로함"],
                        "강점": ["균형감각", "섬세함", "조화로움", "협력성"],
                        "장부_특성": "신대비소(腎大脾小) - 균형형",
                        "기혈수_특성": "기(氣)와 혈(血)이 균형"
                    },
                    "V3": {
                        "name": "소음인 복증형 - 깊이의 탐구자",
                        "description": "소음인의 특성이 가장 강하게 나타나는 깊이 있는 체질입니다.",
                        "신체적_특성": ["매우 섬세함", "깊이 있는 체형", "매우 예민한 감각"],
                        "심리적_특성": ["매우 섬세함", "깊이 있음", "매우 예민함", "직관적"],
                        "건강_관리": ["깊이 있는 활동", "섬세한 생활", "예민한 휴식"],
                        "약점": ["극도의 과민함", "매우 스트레스 민감", "피로함"],
                        "강점": ["극도의 섬세함", "깊이", "예민함", "직관력"],
                        "장부_특성": "신대비소(腎大脾小) - 깊이형",
                        "기혈수_특성": "기(氣)가 매우 섬세하고 혈(血)이 매우 감성적"
                    }
                }
            }
            
            return {
                "constitution_types": constitution_types,
                "total_types": 12,
                "base_constitutions": ["태양인", "소양인", "태음인", "소음인"]
            }
            
        except Exception as e:
            logger.error(f"❌ 12체질론 지식베이스 로드 실패: {e}")
            return {}
    
    def estimate_constitution(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """12체질 추정"""
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "AI 모델이 초기화되지 않았습니다"
                }
            
            # 사용자 데이터 분석
            biometric_data = user_data.get("biometric", {})
            psychological_data = user_data.get("psychological", {})
            behavioral_data = user_data.get("behavioral", {})
            
            # 체질 추정을 위한 프롬프트 구성
            prompt = f"""
당신은 12체질론 전문가입니다. 다음 사용자 데이터를 분석하여 12체질 중 하나를 추정해주세요.

**사용자 데이터:**
- 생체신호: {biometric_data}
- 심리 데이터: {psychological_data}
- 행동 데이터: {behavioral_data}

**12체질 분류:**
{json.dumps(self.constitution_knowledge.get("constitution_types", {}), ensure_ascii=False, indent=2)}

**분석 요청:**
1. 사용자의 특성을 분석하여 가장 적합한 체질을 선택하세요.
2. 선택한 체질의 특성을 설명하세요.
3. 신뢰도를 백분율로 표시하세요.
4. 체질별 건강 관리 방안을 제시하세요.

한국어로 답변해주세요.
"""
            
            # AI 응답 생성
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "estimated_constitution": "A1",  # 임시 결과
                "confidence_score": 85.0,
                "analysis": response.text,
                "characteristics": self.constitution_knowledge.get("constitution_types", {}).get("태양인", {}).get("A1", {}),
                "timestamp": "2025-07-27T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"❌ 체질 추정 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_personalized_solution(self, user_data: Dict[str, Any], constitution_type: str) -> Dict[str, Any]:
        """개인화 솔루션 생성"""
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "AI 모델이 초기화되지 않았습니다"
                }
            
            # 체질 정보 가져오기
            constitution_info = None
            for base_type, subtypes in self.constitution_knowledge.get("constitution_types", {}).items():
                if constitution_type in subtypes:
                    constitution_info = subtypes[constitution_type]
                    break
            
            if not constitution_info:
                return {
                    "success": False,
                    "error": "체질 정보를 찾을 수 없습니다"
                }
            
            # 의학적 조언 가져오기
            medical_advice = ""
            if self.medical_rag:
                medical_result = self.medical_rag.generate_medical_advice(
                    user_data.get("query", ""),
                    user_data.get("symptoms", "")
                )
                if medical_result.get("success"):
                    medical_advice = medical_result.get("advice", "")
            
            # 개인화 솔루션 생성 프롬프트
            prompt = f"""
당신은 12체질론 기반 개인화 건강 코치입니다. 다음 정보를 바탕으로 맞춤형 라이프스타일 솔루션을 제공해주세요.

**사용자 체질 정보:**
- 체질: {constitution_info['name']}
- 설명: {constitution_info['description']}
- 신체적 특성: {', '.join(constitution_info['신체적_특성'])}
- 심리적 특성: {', '.join(constitution_info['심리적_특성'])}
- 강점: {', '.join(constitution_info['강점'])}
- 약점: {', '.join(constitution_info['약점'])}

**사용자 현재 상태:**
- 생체신호: {user_data.get('biometric', {})}
- 심리 상태: {user_data.get('psychological', {})}
- 환경 요인: {user_data.get('environmental', {})}

**의학적 조언:**
{medical_advice}

**솔루션 요청:**
1. 체질에 맞는 라이프스타일 권장사항
2. 현재 상태를 고려한 개인화 조언
3. 실천 가능한 구체적 행동 계획
4. 주의사항 및 팁

**중요:**
- 치료나 진단이 아닌 건강 관리 및 웰니스 중심으로 답변
- 긍정적이고 실천 가능한 조언 제공
- 전통 한의학과 현대 과학을 융합한 관점

한국어로 답변해주세요.
"""
            
            # AI 응답 생성
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "constitution_type": constitution_type,
                "constitution_info": constitution_info,
                "personalized_solution": response.text,
                "medical_advice_included": bool(medical_advice),
                "timestamp": "2025-07-27T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"❌ 개인화 솔루션 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_constitution_guide(self, constitution_type: str) -> Dict[str, Any]:
        """체질별 기본 가이드 제공"""
        try:
            # 체질 정보 찾기
            constitution_info = None
            for base_type, subtypes in self.constitution_knowledge.get("constitution_types", {}).items():
                if constitution_type in subtypes:
                    constitution_info = subtypes[constitution_type]
                    break
            
            if not constitution_info:
                return {
                    "success": False,
                    "error": "체질 정보를 찾을 수 없습니다"
                }
            
            return {
                "success": True,
                "constitution_type": constitution_type,
                "guide": {
                    "name": constitution_info["name"],
                    "description": constitution_info["description"],
                    "characteristics": {
                        "신체적_특성": constitution_info["신체적_특성"],
                        "심리적_특성": constitution_info["심리적_특성"],
                        "강점": constitution_info["강점"],
                        "약점": constitution_info["약점"]
                    },
                    "health_management": constitution_info["건강_관리"],
                    "traditional_medicine": {
                        "장부_특성": constitution_info["장부_특성"],
                        "기혈수_특성": constitution_info["기혈수_특성"]
                    }
                },
                "timestamp": "2025-07-27T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"❌ 체질 가이드 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_soap_chart(self, patient_data: Dict[str, Any], constitution_type: str) -> Dict[str, Any]:
        """한의사용 SOAP 차트 생성 (트랙 1)"""
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "AI 모델이 초기화되지 않았습니다"
                }
            
            # 체질 정보 가져오기
            constitution_info = None
            for base_type, subtypes in self.constitution_knowledge.get("constitution_types", {}).items():
                if constitution_type in subtypes:
                    constitution_info = subtypes[constitution_type]
                    break
            
            if not constitution_info:
                return {
                    "success": False,
                    "error": "체질 정보를 찾을 수 없습니다"
                }
            
            # SOAP 차트 생성 프롬프트
            prompt = f"""
당신은 한의사 진료를 보조하는 AI 어시스턴트입니다. 다음 환자 정보를 바탕으로 SOAP 차트를 작성해주세요.

**환자 정보:**
{json.dumps(patient_data, ensure_ascii=False, indent=2)}

**체질 정보:**
- 체질: {constitution_info['name']}
- 장부 특성: {constitution_info['장부_특성']}
- 기혈수 특성: {constitution_info['기혈수_특성']}

**SOAP 차트 작성 요청:**
1. **S (Subjective)**: 환자 주관적 증상 및 불편사항
2. **O (Objective)**: 객관적 관찰 결과 및 체질 분석
3. **A (Assessment)**: 한의학적 평가 및 변증
4. **P (Plan)**: 치료 계획 및 권장사항

**중요:**
- 한의학 전문 용어를 정확히 사용
- 체질 특성을 고려한 분석
- 진단/치료 제안이 아닌 보조적 정보 제공
- 간결하고 구조화된 형태로 작성

한국어로 답변해주세요.
"""
            
            # AI 응답 생성
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "constitution_type": constitution_type,
                "soap_chart": response.text,
                "service_type": "medical",
                "timestamp": "2025-07-27T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"❌ SOAP 차트 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_persona_diary(self, user_data: Dict[str, Any], constitution_type: str) -> Dict[str, Any]:
        """일반인용 페르소나 다이어리 생성 (트랙 2)"""
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "AI 모델이 초기화되지 않았습니다"
                }
            
            # 체질 정보 가져오기
            constitution_info = None
            for base_type, subtypes in self.constitution_knowledge.get("constitution_types", {}).items():
                if constitution_type in subtypes:
                    constitution_info = subtypes[constitution_type]
                    break
            
            if not constitution_info:
                return {
                    "success": False,
                    "error": "체질 정보를 찾을 수 없습니다"
                }
            
            # 페르소나 다이어리 생성 프롬프트
            prompt = f"""
당신은 일반 사용자의 건강 동반자입니다. 다음 정보를 바탕으로 친근하고 실용적인 페르소나 다이어리를 작성해주세요.

**사용자 정보:**
{json.dumps(user_data, ensure_ascii=False, indent=2)}

**체질 정보:**
- 체질: {constitution_info['name']}
- 설명: {constitution_info['description']}
- 강점: {', '.join(constitution_info['강점'])}
- 약점: {', '.join(constitution_info['약점'])}

**페르소나 다이어리 작성 요청:**
1. **오늘의 건강 상태**: 현재 컨디션과 체질 특성 연관성
2. **라이프스타일 코칭**: 체질에 맞는 실천 가능한 조언
3. **동기 부여**: 긍정적이고 격려하는 메시지
4. **내일의 목표**: 구체적이고 달성 가능한 건강 목표

**중요:**
- 친근하고 공감적인 톤 사용
- 전문 용어 지양, 쉬운 언어 사용
- 진단/치료가 아닌 웰니스 중심
- 실천 가능한 구체적 조언 제공

한국어로 답변해주세요.
"""
            
            # AI 응답 생성
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "constitution_type": constitution_type,
                "persona_diary": response.text,
                "service_type": "general",
                "timestamp": "2025-07-27T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"❌ 페르소나 다이어리 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# 전역 인스턴스
constitution_ai_brain = ConstitutionAIBrain() 