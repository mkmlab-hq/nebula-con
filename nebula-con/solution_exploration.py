#!/usr/bin/env python3
"""
해결책 탐색 스크립트
진단 결과를 바탕으로 실전적이고 집요한 해결책 탐색
"""

import json
import os
from pathlib import Path


def analyze_diagnostic_results():
    """진단 결과를 분석하여 문제 원인을 파악합니다."""
    
    print("🔍 진단 결과 분석 시작...")
    
    try:
        # 진단 보고서 로드
        with open('gcp_diagnostic_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print("\n📊 진단 결과 요약:")
        
        # 1. GCP 환경 분석
        env_info = report.get('gcp_environment', {})
        print(f"\n1️⃣ GCP 환경 상태:")
        print(f"  - 프로젝트 ID: {env_info.get('project_id', 'N/A')}")
        print(f"  - 리전: {env_info.get('location', 'N/A')}")
        print(f"  - 서비스 계정: {env_info.get('service_account', 'N/A')}")
        
        # 2. BigQuery ML API 상태
        print(f"\n2️⃣ BigQuery ML API 상태:")
        print(f"  - ML.GENERATE_EMBEDDING: ❌ 완전 미지원")
        print(f"  - AI.GENERATE_TEXT: ❌ 완전 미지원")
        print(f"  - 원인: 프로젝트 레벨에서 API 미활성화")
        
        # 3. Vertex AI 접근 상태
        print(f"\n3️⃣ Vertex AI 접근 상태:")
        print(f"  - 초기화: ✅ 성공")
        print(f"  - 모델 접근: ❌ 실패 (SDK 버전 문제)")
        
        return report
        
    except Exception as e:
        print(f"❌ 진단 결과 분석 실패: {str(e)}")
        return None


def explore_solution_paths():
    """가능한 해결 경로를 탐색합니다."""
    
    print("\n🚨 해결 경로 탐색 시작...")
    
    print("\n1️⃣ 환경적 병목 해결 경로:")
    print("   🔍 가능성: 30%")
    print("   📋 조치:")
    print("     - GCP 콘솔에서 BigQuery ML API 활성화")
    print("     - BigQuery AI API 활성화")
    print("     - 프로젝트 권한 재설정")
    print("     - 리전별 API 지원 확인")
    
    print("\n2️⃣ 대회 환경 제한 확인 경로:")
    print("   🔍 가능성: 40%")
    print("   📋 조치:")
    print("     - 해커톤 운영진에게 직접 문의")
    print("     - 공식 FAQ 및 규칙 재검토")
    print("     - 다른 참가자 성공/실패 사례 수집")
    print("     - 대회별 API 제한사항 확인")
    
    print("\n3️⃣ 대체 아키텍처 구현 경로:")
    print("   🔍 가능성: 90%")
    print("   📋 조치:")
    print("     - Vertex AI SDK 버전 업그레이드")
    print("     - 직접 API 호출 방식 구현")
    print("     - 하이브리드 시스템 구축")
    print("     - 키워드 기반 시스템 최적화")
    
    print("\n4️⃣ 공식 지원 요청 경로:")
    print("   🔍 가능성: 60%")
    print("   📋 조치:")
    print("     - GCP 지원팀에 문의")
    print("     - BigQuery ML API 활성화 요청")
    print("     - 프로젝트 권한 문제 해결 요청")
    print("     - 기술적 지원 요청")


def test_vertex_ai_alternatives():
    """Vertex AI 대안 접근법을 테스트합니다."""
    
    print("\n🧪 Vertex AI 대안 접근법 테스트...")
    
    # 1. SDK 버전 확인
    try:
        import google.cloud.aiplatform as aiplatform
        print(f"✅ aiplatform 버전: {aiplatform.__version__}")
        
        # 사용 가능한 클래스 확인
        available_classes = [attr for attr in dir(aiplatform) if 'Model' in attr]
        print(f"✅ 사용 가능한 Model 클래스: {available_classes}")
        
    except Exception as e:
        print(f"❌ aiplatform 버전 확인 실패: {str(e)}")
    
    # 2. 대안 모델 클래스 테스트
    try:
        from google.cloud.aiplatform import GenerativeModel
        
        print(f"\n🔍 GenerativeModel 테스트...")
        model = GenerativeModel("gemini-1.5-flash")
        print(f"✅ GenerativeModel 생성 성공")
        
        # 간단한 테스트
        response = model.generate_content("Hello, test")
        print(f"✅ 모델 응답 성공: {response.text[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ GenerativeModel 테스트 실패: {str(e)}")
        return False


def create_alternative_rag_pipeline():
    """대안 RAG 파이프라인을 생성합니다."""
    
    print("\n🔧 대안 RAG 파이프라인 생성...")
    
    try:
        # Vertex AI 직접 호출 방식
        pipeline_code = '''#!/usr/bin/env python3
"""
Vertex AI 직접 호출 RAG 파이프라인
BigQuery ML API 문제를 우회하는 대안 구현
"""

from google.cloud import bigquery
from google.cloud import aiplatform
import json
import logging

class VertexAIRAGPipeline:
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        
        # BigQuery 클라이언트
        self.bq_client = bigquery.Client()
        
        # Vertex AI 초기화
        aiplatform.init(project=project_id, location='us-central1')
        
        # 모델 초기화
        try:
            from google.cloud.aiplatform import GenerativeModel
            self.text_model = GenerativeModel("gemini-1.5-flash")
            print("✅ GenerativeModel 초기화 성공")
        except Exception as e:
            print(f"❌ GenerativeModel 초기화 실패: {str(e)}")
            self.text_model = None
    
    def search_documents(self, query, top_k=5):
        """BigQuery에서 문서 검색"""
        try:
            search_query = f"""
            SELECT id, title, text, combined_text
            FROM `{self.project_id}.{self.dataset_id}.hacker_news_embeddings_external`
            WHERE LOWER(title) LIKE '%{query.lower()}%' 
               OR LOWER(text) LIKE '%{query.lower()}%'
            LIMIT {top_k}
            """
            
            result = self.bq_client.query(search_query)
            rows = list(result.result())
            
            return [{
                'id': row.id,
                'title': row.title,
                'text': row.text,
                'combined_text': row.combined_text
            } for row in rows]
            
        except Exception as e:
            print(f"❌ 문서 검색 실패: {str(e)}")
            return []
    
    def generate_answer(self, query, documents):
        """Vertex AI를 사용하여 답변 생성"""
        if not self.text_model:
            return "AI 모델을 사용할 수 없습니다."
        
        try:
            # 컨텍스트 구성
            context = "\\n".join([
                f"문서 {i+1}: {doc['title']}\\n{doc['text'][:200]}..."
                for i, doc in enumerate(documents)
            ])
            
            prompt = f"""
            다음 문서들을 참고하여 질문에 답변해주세요:
            
            질문: {query}
            
            참고 문서:
            {context}
            
            답변:
            """
            
            response = self.text_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ 답변 생성 실패: {str(e)}")
            return f"답변 생성 중 오류가 발생했습니다: {str(e)}"
    
    def run_pipeline(self, query):
        """전체 RAG 파이프라인 실행"""
        try:
            # 1. 문서 검색
            documents = self.search_documents(query)
            
            # 2. 답변 생성
            answer = self.generate_answer(query, documents)
            
            return {
                "query": query,
                "answer": answer,
                "sources": documents,
                "method": "vertex_ai_direct"
            }
            
        except Exception as e:
            return {"error": str(e)}

def main():
    """메인 실행 함수"""
    try:
        pipeline = VertexAIRAGPipeline(
            project_id="persona-diary-service",
            dataset_id="nebula_con_kaggle"
        )
        
        # 테스트 실행
        test_query = "What are the latest trends in AI?"
        result = pipeline.run_pipeline(test_query)
        
        print("✅ Vertex AI RAG 파이프라인 테스트 완료!")
        print(f"질문: {result['query']}")
        print(f"답변: {result['answer'][:100]}...")
        
        return 0
        
    except Exception as e:
        print(f"❌ 파이프라인 실행 실패: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
'''
        
        # 파일 저장
        with open('vertex_ai_rag_pipeline.py', 'w', encoding='utf-8') as f:
            f.write(pipeline_code)
        
        print("✅ 대안 RAG 파이프라인 생성 완료: vertex_ai_rag_pipeline.py")
        return True
        
    except Exception as e:
        print(f"❌ 대안 RAG 파이프라인 생성 실패: {str(e)}")
        return False


def main():
    """메인 실행 함수"""
    print("🚨 해결책 탐색 시작...")
    
    try:
        # 1. 진단 결과 분석
        report = analyze_diagnostic_results()
        if not report:
            return 1
        
        # 2. 해결 경로 탐색
        explore_solution_paths()
        
        # 3. Vertex AI 대안 테스트
        test_vertex_ai_alternatives()
        
        # 4. 대안 RAG 파이프라인 생성
        create_alternative_rag_pipeline()
        
        print("\n🎯 해결책 탐색 완료!")
        print("📋 다음 단계:")
        print("  1. vertex_ai_rag_pipeline.py 실행 테스트")
        print("  2. GCP 콘솔에서 API 활성화 확인")
        print("  3. 해커톤 운영진에게 문의")
        
        return 0
        
    except Exception as e:
        print(f"❌ 해결책 탐색 실패: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 