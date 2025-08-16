#!/usr/bin/env python3
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
            context = "\n".join([
                f"문서 {i+1}: {doc['title']}\n{doc['text'][:200]}..."
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
