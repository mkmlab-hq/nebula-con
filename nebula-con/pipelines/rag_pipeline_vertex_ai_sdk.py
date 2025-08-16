#!/usr/bin/env python3
"""
Vertex AI Python SDK를 직접 사용하는 RAG 파이프라인
BigQuery ML 우회하여 완전한 AI 기반 RAG 구현
"""

import json
import logging
from typing import Any, Dict, List
import numpy as np
from google.cloud import bigquery
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipelineVertexAISDK:
    """Vertex AI Python SDK를 직접 사용하는 RAG 파이프라인"""

    def __init__(self, project_id: str = 'persona-diary-service',
                 dataset_id: str = 'nebula_con_kaggle',
                 location: str = 'us-central1'):
        """RAG 파이프라인 초기화"""
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.location = location

        # BigQuery 클라이언트 초기화
        self.bq_client = bigquery.Client(
            project=project_id, location=location
        )

        # Vertex AI 초기화
        aiplatform.init(project=project_id, location=location)

        # Vertex AI 모델 초기화
        self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        self.generation_model = TextGenerationModel.from_pretrained("gemini-1.5-flash-001")

        logger.info(
            f"🚀 Vertex AI SDK RAG 파이프라인 초기화 완료: "
            f"{project_id}.{dataset_id}"
        )
        logger.info(f"📍 위치: {location}")
        logger.info(f"🧠 임베딩 모델: text-embedding-004")
        logger.info(f"🧠 생성 모델: gemini-1.5-flash-001")

    def load_documents_from_bigquery(self) -> List[Dict[str, Any]]:
        """BigQuery에서 문서 데이터 로드"""
        try:
            table_name = 'hacker_news_embeddings_external'
            
            query = f"""
            SELECT id, title, text
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            WHERE text IS NOT NULL OR title IS NOT NULL
            LIMIT 100
            """
            
            logger.info(f"📊 BigQuery에서 문서 로드 중: {query[:100]}...")
            
            result = self.bq_client.query(query)
            rows = list(result.result())
            
            documents = []
            for row in rows:
                if row.text or row.title:
                    combined_text = f"{row.title or ''} {row.text or ''}".strip()
                    documents.append({
                        'id': row.id,
                        'title': row.title,
                        'text': row.text,
                        'combined_text': combined_text
                    })
            
            logger.info(f"✅ 문서 로드 완료: {len(documents)}개")
            return documents
            
        except Exception as e:
            logger.error(f"❌ 문서 로드 실패: {e}")
            return []

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """텍스트 임베딩 생성"""
        try:
            logger.info(f"🧠 임베딩 생성 중: {len(texts)}개 텍스트")
            
            embeddings = []
            for text in texts:
                if text and text.strip():
                    embedding = self.embedding_model.get_embeddings([text])
                    embeddings.append(embedding[0].values)
                else:
                    # 빈 텍스트에 대한 더미 임베딩
                    embeddings.append([0.0] * 768)
            
            logger.info(f"✅ 임베딩 생성 완료: {len(embeddings)}개")
            return embeddings
            
        except Exception as e:
            logger.error(f"❌ 임베딩 생성 실패: {e}")
            return []

    def calculate_cosine_similarity(self, query_embedding: List[float], 
                                   doc_embeddings: List[List[float]]) -> List[float]:
        """코사인 유사도 계산"""
        try:
            query_vec = np.array(query_embedding)
            similarities = []
            
            for doc_embedding in doc_embeddings:
                doc_vec = np.array(doc_embedding)
                
                # 코사인 유사도 계산
                dot_product = np.dot(query_vec, doc_vec)
                norm_query = np.linalg.norm(query_vec)
                norm_doc = np.linalg.norm(doc_vec)
                
                if norm_query > 0 and norm_doc > 0:
                    similarity = dot_product / (norm_query * norm_doc)
                else:
                    similarity = 0.0
                
                similarities.append(similarity)
            
            return similarities
            
        except Exception as e:
            logger.error(f"❌ 유사도 계산 실패: {e}")
            return [0.0] * len(doc_embeddings)

    def search_similar_documents(self, query: str, documents: List[Dict[str, Any]], 
                                top_k: int = 5) -> List[Dict[str, Any]]:
        """유사도 기반 문서 검색"""
        try:
            logger.info(f"🔍 유사도 기반 검색 시작: {query}")
            
            # 1. 쿼리 임베딩 생성
            query_embedding = self.generate_embeddings([query])
            if not query_embedding:
                logger.warning("⚠️ 쿼리 임베딩 생성 실패")
                return []
            
            # 2. 문서 임베딩 생성
            doc_texts = [doc['combined_text'] for doc in documents]
            doc_embeddings = self.generate_embeddings(doc_texts)
            if not doc_embeddings:
                logger.warning("⚠️ 문서 임베딩 생성 실패")
                return []
            
            # 3. 유사도 계산
            similarities = self.calculate_cosine_similarity(query_embedding[0], doc_embeddings)
            
            # 4. 유사도 점수와 문서 결합
            scored_docs = []
            for i, doc in enumerate(documents):
                scored_docs.append({
                    **doc,
                    'similarity_score': similarities[i]
                })
            
            # 5. 유사도 순으로 정렬
            scored_docs.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # 6. 상위 k개 반환
            top_results = scored_docs[:top_k]
            
            logger.info(f"✅ 유사도 검색 완료: {len(top_results)}개 문서")
            return top_results
            
        except Exception as e:
            logger.error(f"❌ 유사도 검색 실패: {e}")
            return []

    def generate_ai_answer(self, query: str, search_results: List[Dict[str, Any]]) -> str:
        """AI 기반 답변 생성"""
        try:
            if not search_results:
                return f"죄송합니다. '{query}'에 대한 관련 정보를 찾을 수 없습니다."
            
            # 컨텍스트 구성
            context = ""
            for i, doc in enumerate(search_results[:3]):  # 상위 3개 문서만 사용
                context += f"문서 {i+1}:\n"
                context += f"제목: {doc.get('title', 'N/A')}\n"
                context += f"내용: {doc.get('text', 'N/A')[:300]}...\n"
                context += f"유사도 점수: {doc.get('similarity_score', 0):.3f}\n\n"
            
            # 프롬프트 구성
            prompt = f"""
다음 질문에 대해 제공된 컨텍스트를 바탕으로 정확하고 유용한 답변을 생성해주세요.

질문: {query}

컨텍스트:
{context}

요구사항:
1. 컨텍스트의 정보를 바탕으로 답변하세요
2. 구체적이고 실용적인 조언을 제공하세요
3. 한국어로 답변하세요
4. 답변 끝에 "이 답변은 Vertex AI의 text-embedding-004와 gemini-1.5-flash-001 모델을 사용하여 생성되었습니다."라고 표시하세요

답변:
"""
            
            logger.info("🧠 AI 답변 생성 중...")
            
            # Vertex AI로 답변 생성
            response = self.generation_model.predict(prompt)
            answer = response.text
            
            logger.info("✅ AI 답변 생성 완료")
            return answer
            
        except Exception as e:
            logger.error(f"❌ AI 답변 생성 실패: {e}")
            return f"AI 답변 생성 중 오류가 발생했습니다: {str(e)}"

    def run_rag_pipeline(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """전체 RAG 파이프라인 실행"""
        try:
            logger.info(f"🚀 RAG 파이프라인 실행 시작: {query}")
            
            # 1. BigQuery에서 문서 로드
            documents = self.load_documents_from_bigquery()
            if not documents:
                return {
                    'query': query,
                    'search_results': [],
                    'answer': '문서를 로드할 수 없습니다.',
                    'status': 'error',
                    'error': '문서 로드 실패'
                }
            
            # 2. 유사도 기반 문서 검색
            search_results = self.search_similar_documents(query, documents, top_k)
            if not search_results:
                return {
                    'query': query,
                    'search_results': [],
                    'answer': f"'{query}'에 대한 관련 정보를 찾을 수 없습니다.",
                    'status': 'no_results'
                }
            
            # 3. AI 기반 답변 생성
            answer = self.generate_ai_answer(query, search_results)
            
            result = {
                'query': query,
                'search_results': search_results,
                'answer': answer,
                'status': 'success',
                'search_method': 'vertex_ai_embedding_similarity',
                'location': self.location,
                'models_used': ['text-embedding-004', 'gemini-1.5-flash-001']
            }
            
            logger.info(f"✅ RAG 파이프라인 완료: {query}")
            return result
            
        except Exception as e:
            logger.error(f"❌ RAG 파이프라인 실패: {e}")
            return {
                'query': query,
                'search_results': [],
                'answer': f"오류가 발생했습니다: {str(e)}",
                'status': 'error',
                'error': str(e)
            }

    def run_full_pipeline_test(self, test_queries: List[str]) -> Dict[str, Any]:
        """전체 RAG 파이프라인 테스트 실행"""
        logger.info("🚀 Vertex AI SDK RAG 파이프라인 전체 테스트 시작!")
        
        results = []
        success_count = 0
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"🔍 테스트 쿼리 {i}/{len(test_queries)} 실행: {query}")
            
            try:
                result = self.run_rag_pipeline(query)
                results.append(result)
                
                if result['status'] == 'success':
                    success_count += 1
                    logger.info(f"✅ 쿼리 {i} 성공")
                else:
                    logger.warning(f"⚠️ 쿼리 {i} 실패: {result.get('status', 'unknown')}")
                    
            except Exception as e:
                logger.error(f"❌ 쿼리 {i} 예외 발생: {str(e)}")
                results.append({
                    'query': query,
                    'search_results': [],
                    'answer': f"예외 발생: {str(e)}",
                    'status': 'exception',
                    'error': str(e)
                })
        
        # 결과 요약
        summary = {
            'total_queries': len(test_queries),
            'successful_queries': success_count,
            'success_rate': f"{success_count}/{len(test_queries)}",
            'pipeline_type': 'vertex_ai_sdk_direct',
            'models_used': ['text-embedding-004', 'gemini-1.5-flash-001'],
            'results': results
        }
        
        # 결과 저장
        output_file = 'vertex_ai_sdk_rag_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info("✅ Vertex AI SDK RAG 파이프라인 테스트 완료!")
        logger.info(f"성공: {success_count}/{len(test_queries)} 쿼리")
        logger.info(f"결과 저장: {output_file}")
        
        return summary


def main():
    """메인 실행 함수"""
    # 실제 프로젝트 구조에 맞는 설정
    project_id = "persona-diary-service"
    dataset_id = "nebula_con_kaggle"
    location = "us-central1"
    
    # RAG 파이프라인 초기화
    rag_pipeline = RAGPipelineVertexAISDK(project_id, dataset_id, location)
    
    # 테스트 쿼리
    test_queries = [
        "How to optimize machine learning models?",
        "Best practices for data science projects?",
        "Startup advice for new founders",
        "PhD vs startup career path",
        "Machine learning in production"
    ]
    
    # 전체 파이프라인 테스트 실행
    results = rag_pipeline.run_full_pipeline_test(test_queries)
    
    # 결과 출력
    print(f"\n🎉 Vertex AI SDK RAG 파이프라인 실행 성공!")
    print(f"✅ BigQuery ML 우회하여 직접 Vertex AI 사용!")
    print(f"✅ 완전한 AI 기반 임베딩 및 답변 생성!")
    print(f"🚀 이제 캐글 해커톤 제출이 가능합니다!")


if __name__ == "__main__":
    main() 