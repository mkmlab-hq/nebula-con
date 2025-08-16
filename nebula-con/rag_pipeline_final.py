#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) 파이프라인 - 최종 버전
기존 테이블 활용하여 즉시 실행 가능
"""

import json
import logging
import os
from typing import Any, Dict

from google.cloud import bigquery

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipelineFinal:
    """RAG 파이프라인 최종 클래스 - 기존 테이블 활용"""

    def __init__(self, project_id: str, dataset_id: str):
        """RAG 파이프라인 초기화"""
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client()
        
        logger.info("✅ RAG 파이프라인 최종 버전 초기화 완료")
        logger.info(f"프로젝트: {project_id}, 데이터셋: {dataset_id}")

    def retrieve_and_generate(self, query_text: str,
                             embeddings_table: str = "hacker_news_embeddings_external",
                             top_k: int = 5) -> Dict[str, Any]:
        """유사도 검색 및 답변 생성 - 기존 임베딩 테이블 활용"""
        try:
            # 1. 기존 임베딩 테이블에서 유사도 검색
            # 간단한 키워드 기반 검색으로 시작 (비용 절약)
            search_query = f"""
            SELECT 
                id,
                title,
                text,
                combined_text
            FROM `{self.project_id}.{self.dataset_id}.{embeddings_table}`
            WHERE 
                LOWER(combined_text) LIKE LOWER('%{query_text.lower()}%')
                OR LOWER(title) LIKE LOWER('%{query_text.lower()}%')
            ORDER BY id DESC
            LIMIT {top_k}
            """
            
            logger.info("🔍 키워드 기반 검색 실행 중...")
            logger.info(f"검색 쿼리: {search_query}")
            
            search_job = self.client.query(search_query)
            search_results = list(search_job.result())
            
            if not search_results:
                logger.warning("⚠️ 검색 결과가 없습니다. 전체 테이블에서 샘플 추출")
                # 검색 결과가 없으면 전체 테이블에서 샘플 추출
                sample_query = f"""
                SELECT id, title, text, combined_text
                FROM `{self.project_id}.{self.dataset_id}.{embeddings_table}`
                LIMIT {top_k}
                """
                search_job = self.client.query(sample_query)
                search_results = list(search_job.result())
            
            # 2. AI 답변 생성
            context = "\n".join([
                f"제목: {row.title}\n내용: {row.text[:200]}..."
                for row in search_results
            ])
            
            ai_query = f"""
            SELECT 
                AI.GENERATE_TEXT(
                    '다음 HackerNews 게시글들을 바탕으로 질문에 답변해주세요. '
                    '질문: {query_text}\n\n'
                    '참고 자료:\n{context}',
                    'gemini-pro'
                ) AS answer
            LIMIT 1
            """
            
            logger.info("🔍 AI 답변 생성 중...")
            ai_job = self.client.query(ai_query)
            ai_result = list(ai_job.result())
            
            if not ai_result:
                raise ValueError("AI 답변 생성 실패")
            
            answer = ai_result[0].answer
            
            return {
                "query": query_text,
                "context": context,
                "answer": answer,
                "sources": [
                    {
                        "id": row.id,
                        "title": row.title,
                        "text_preview": row.text[:100] + "..." if row.text else "내용 없음"
                    }
                    for row in search_results
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ 검색 및 생성 실패: {str(e)}")
            return {"error": str(e)}

    def run_full_pipeline(self) -> bool:
        """전체 RAG 파이프라인 실행 - 기존 테이블 활용"""
        try:
            logger.info("🚀 RAG 파이프라인 최종 실행 시작...")
            
            # 테스트 쿼리 실행
            test_queries = [
                "What are the latest trends in AI?",
                "How to optimize machine learning models?",
                "Best practices for data science projects?",
                "Startup advice for new founders",
                "PhD vs startup career path"
            ]
            
            results = []
            for i, query in enumerate(test_queries, 1):
                logger.info(f"🔍 테스트 쿼리 {i}/{len(test_queries)} 실행: {query}")
                result = self.retrieve_and_generate(query)
                results.append(result)
                
                if "error" in result:
                    logger.error(f"❌ 쿼리 실패: {result['error']}")
                    # 개별 쿼리 실패는 전체 파이프라인을 중단하지 않음
                    continue
            
            # 3. 결과 저장
            output_file = "rag_pipeline_final_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            # 성공한 쿼리 수 계산
            successful_queries = sum(1 for r in results if "error" not in r)
            
            logger.info("✅ RAG 파이프라인 최종 실행 완료!")
            logger.info(f"성공: {successful_queries}/{len(test_queries)} 쿼리")
            logger.info(f"결과 저장: {output_file}")
            
            return successful_queries > 0
            
        except Exception as e:
            logger.error(f"❌ 파이프라인 실행 실패: {str(e)}")
            return False


def main():
    """메인 실행 함수"""
    try:
        # 환경 변수에서 프로젝트 정보 가져오기
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT',
                                   'persona-diary-service')
        dataset_id = os.environ.get('BIGQUERY_DATASET', 'nebula_con_kaggle')
        
        # RAG 파이프라인 초기화 및 실행
        pipeline = RAGPipelineFinal(project_id, dataset_id)
        success = pipeline.run_full_pipeline()
        
        if success:
            print("🎉 RAG 파이프라인 최종 실행 성공!")
            print("결과 파일: rag_pipeline_final_results.json")
            print("📊 답변 샘플이 생성되었습니다.")
        else:
            print("❌ RAG 파이프라인 최종 실행 실패")
            return 1
            
        return 0
        
    except Exception as e:
        print(f"❌ 메인 실행 오류: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 