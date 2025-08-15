#!/usr/bin/env python3
"""
MKM Lab - 의학 데이터베이스 RAG 시스템
의학 논문, 임상 데이터, 한의학 지식을 활용한 지능형 의학 조언 시스템
"""
import os
import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalRAGSystem:
    """의학 데이터베이스 RAG 시스템"""
    
    def __init__(self):
        """RAG 시스템 초기화"""
        try:
            # Google Gemini API 설정
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                logger.error("❌ GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다")
                self.model = None
                return
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # 의학 데이터베이스 로드
            self.medical_knowledge = self._load_medical_database()
            
            logger.info("✅ 의학 RAG 시스템 초기화 완료")
            
        except Exception as e:
            logger.error(f"❌ 의학 RAG 시스템 초기화 실패: {e}")
            self.model = None
            self.medical_knowledge = {}
    
    def _load_medical_database(self) -> Dict[str, Any]:
        """의학 데이터베이스 로드"""
        try:
            data_dir = Path(__file__).parent.parent / "data"
            
            # 최신 의학 논문 로드
            medical_papers_path = data_dir / "latest_medical_arxiv_papers.json"
            if medical_papers_path.exists():
                with open(medical_papers_path, 'r', encoding='utf-8') as f:
                    medical_papers = json.load(f)
                    logger.info(f"✅ 의학 논문 {len(medical_papers)}개 로드 완료")
            else:
                medical_papers = []
                logger.warning("⚠️ 의학 논문 데이터를 찾을 수 없습니다")
            
            # 체질 분석 데이터 로드
            constitution_path = data_dir / "constitution_with_embedding.json"
            if constitution_path.exists():
                with open(constitution_path, 'r', encoding='utf-8') as f:
                    constitution_data = json.load(f)
                    logger.info(f"✅ 체질 분석 데이터 로드 완료")
            else:
                constitution_data = {}
                logger.warning("⚠️ 체질 분석 데이터를 찾을 수 없습니다")
            
            return {
                "medical_papers": medical_papers,
                "constitution_data": constitution_data,
                "total_papers": len(medical_papers)
            }
            
        except Exception as e:
            logger.error(f"❌ 의학 데이터베이스 로드 실패: {e}")
            return {}
    
    def search_medical_knowledge(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """의학 지식 검색"""
        try:
            if not self.medical_knowledge.get("medical_papers"):
                return []
            
            # 간단한 키워드 기반 검색
            relevant_papers = []
            query_lower = query.lower()
            
            for paper in self.medical_knowledge["medical_papers"]:
                title = paper.get("title", "").lower()
                summary = paper.get("summary", "").lower()
                
                # 제목이나 요약에서 키워드 검색
                if (query_lower in title or 
                    query_lower in summary or
                    any(keyword in title or keyword in summary 
                        for keyword in query_lower.split())):
                    relevant_papers.append(paper)
                    
                    if len(relevant_papers) >= max_results:
                        break
            
            return relevant_papers
            
        except Exception as e:
            logger.error(f"❌ 의학 지식 검색 실패: {e}")
            return []
    
    def generate_medical_advice(self, user_query: str, user_symptoms: str = "") -> Dict[str, Any]:
        """의학 조언 생성"""
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "AI 모델이 초기화되지 않았습니다"
                }
            
            # 관련 의학 지식 검색
            relevant_papers = self.search_medical_knowledge(user_query)
            
            # 컨텍스트 구성
            context = ""
            if relevant_papers:
                context = "관련 의학 연구:\n"
                for i, paper in enumerate(relevant_papers[:3], 1):
                    context += f"{i}. {paper.get('title', '제목 없음')}\n"
                    context += f"   요약: {paper.get('summary', '요약 없음')[:200]}...\n\n"
            
            # 프롬프트 구성
            prompt = f"""
당신은 전문 의학 AI 어드바이저입니다. 다음 정보를 바탕으로 의학적 조언을 제공해주세요.

사용자 질문: {user_query}
사용자 증상: {user_symptoms if user_symptoms else "제공되지 않음"}

{context}

주의사항:
1. 이는 참고용 조언이며, 정확한 진단을 위해서는 반드시 의료진과 상담하세요.
2. 한의학과 현대의학의 관점을 모두 고려하여 종합적인 조언을 제공하세요.
3. 안전하고 실용적인 조언을 제공하세요.

의학적 조언을 한국어로 제공해주세요.
"""
            
            # AI 응답 생성
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "advice": response.text,
                "relevant_papers": len(relevant_papers),
                "context_used": bool(context)
            }
            
        except Exception as e:
            logger.error(f"❌ 의학 조언 생성 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_constitution_analysis(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """체질 분석"""
        try:
            if not self.medical_knowledge.get("constitution_data"):
                return {
                    "success": False,
                    "error": "체질 분석 데이터가 없습니다"
                }
            
            # 체질 분석 로직 (간단한 예시)
            constitution_result = {
                "constitution_type": "균형잡힌 체질",
                "characteristics": ["안정적", "건강한", "균형잡힌"],
                "recommendations": [
                    "규칙적인 생활습관 유지",
                    "균형잡힌 식단 섭취",
                    "적절한 운동과 휴식"
                ],
                "medical_advice": "현재 상태가 양호하므로 현재의 건강한 생활습관을 유지하시기 바랍니다."
            }
            
            return {
                "success": True,
                "analysis": constitution_result
            }
            
        except Exception as e:
            logger.error(f"❌ 체질 분석 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# 전역 인스턴스
medical_rag_system = MedicalRAGSystem() 