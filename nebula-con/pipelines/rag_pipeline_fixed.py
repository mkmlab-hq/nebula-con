#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) 파이프라인
BigQuery ML과 Vertex AI를 활용한 HackerNews 데이터 분석 시스템
"""

import json
import logging
import os
from typing import Any, Dict

from google.cloud import bigquery

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG 파이프라인 메인 클래스"""

    def __init__(self, project_id: str, dataset_id: str):
        """RAG 파이프라인 초기화"""
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client()
        self.model_path = (
            f"`{project_id}.{dataset_id}.text_embedding_remote_model`"
        )

        logger.info("✅ RAG 파이프라인 초기화 완료")
        logger.info(f"프로젝트: {project_id}, 데이터셋: {dataset_id}")

    def create_embeddings_table(self, source_table: str,
                               target_table: str) -> bool:
        """임베딩 테이블 생성"""
        try:
            # BigQuery ML 공식 문서 기반 쿼리
            query = f"""
            CREATE OR REPLACE TABLE 
            `{self.project_id}.{self.dataset_id}.{target_table}` AS
            SELECT 
                id,
                title,
                text,
                ML.GENERATE_EMBEDDING(
                    MODEL {self.model_path},
                    STRUCT(
                        CONCAT(
                            IFNULL(title, ''), ' ',
                            IFNULL(text, '')
                        ) AS content
                    )
                ) AS embedding
            FROM `{self.project_id}.{self.dataset_id}.{source_table}`
            LIMIT 100
            """

            logger.info("🔍 임베딩 테이블 생성 쿼리 실행 중...")
            query_job = self.client.query(query)
            query_job.result()

            logger.info(f"✅ 임베딩 테이블 생성 완료: {target_table}")
            return True

        except Exception as e:
            logger.error(f"❌ 임베딩 테이블 생성 실패: {str(e)}")
            return False

    def retrieve_and_generate(self, query_text: str,
                             embeddings_table: str,
                             top_k: int = 5) -> Dict[str, Any]:
        """유사도 검색 및 답변 생성"""
        try:
            # 1. 쿼리 텍스트 임베딩 생성
            embedding_query = f"""
            SELECT 
                ML.GENERATE_EMBEDDING(
                    MODEL {self.model_path},
                    STRUCT('{query_text}' AS content)
                ) AS query_embedding
            LIMIT 1
            """

            logger.info("🔍 쿼리 임베딩 생성 중...")
            query_job = self.client.query(embedding_query)
            query_result = list(query_job.result())

            if not query_result:
                raise ValueError("쿼리 임베딩 생성 실패")

            query_embedding = query_result[0].query_embedding

            # 2. 유사도 검색 (ML.DISTANCE 사용)
            search_query = f"""
            SELECT 
                id,
                title,
                text,
                ML.DISTANCE(embedding, '{query_embedding}') AS distance
            FROM `{self.project_id}.{self.dataset_id}.{embeddings_table}`
            ORDER BY distance ASC
            LIMIT {top_k}
            """

            logger.info("🔍 유사도 검색 실행 중...")
            search_job = self.client.query(search_query)
            search_results = list(search_job.result())

            # 3. AI 답변 생성
            context = "\n".join([
                f"제목: {row.title}\n내용: {row.text}"
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
                        "distance": row.distance
                    }
                    for row in search_results
                ]
            }

        except Exception as e:
            logger.error(f"❌ 검색 및 생성 실패: {str(e)}")
            return {"error": str(e)}

    def run_full_pipeline(self, source_table: str = "hackernews_data",
                         embeddings_table: str = "hackernews_embeddings") -> bool:
        """전체 RAG 파이프라인 실행"""
        try:
            logger.info("🚀 RAG 파이프라인 전체 실행 시작...")

            # 1. 임베딩 테이블 생성
            if not self.create_embeddings_table(source_table, embeddings_table):
                return False

            # 2. 테스트 쿼리 실행
            test_queries = [
                "What are the latest trends in AI?",
                "How to optimize machine learning models?",
                "Best practices for data science projects?"
            ]

            results = []
            for query in test_queries:
                logger.info(f"🔍 테스트 쿼리 실행: {query}")
                result = self.retrieve_and_generate(query, embeddings_table)
                results.append(result)

                if "error" in result:
                    logger.error(f"❌ 쿼리 실패: {result['error']}")
                    return False

            # 3. 결과 저장
            output_file = "rag_pipeline_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            logger.info("✅ RAG 파이프라인 실행 완료!")
            logger.info(f"결과 저장: {output_file}")

            return True

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
        pipeline = RAGPipeline(project_id, dataset_id)
        success = pipeline.run_full_pipeline()

        if success:
            print("🎉 RAG 파이프라인 실행 성공!")
            print("결과 파일: rag_pipeline_results.json")
        else:
            print("❌ RAG 파이프라인 실행 실패")
            return 1

        return 0

    except Exception as e:
        print(f"❌ 메인 실행 오류: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
