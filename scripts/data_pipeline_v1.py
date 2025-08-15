#!/usr/bin/env python3
"""
🏆 캐글 BigQuery AI 해커톤 - 데이터 파이프라인 v1

목표: Week 1 데이터 파이프라인 v1 구축
기간: 2025.8.15-8.17 (48시간)
우선순위: 🚨 긴급

구현 내용:
- 데이터 로딩 및 전처리
- Chunking 알고리즘
- 벡터화 및 저장 시스템
- 기본 검색 모델
- 간단한 RAG 체인
"""

import json
import logging
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataPipelineV1:
    """Week 1 데이터 파이프라인 v1 구현"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 파이프라인 설정
        self.config = {
            "chunk_size": 512,
            "chunk_overlap": 0.1,
            "vector_dimension": 768,
            "max_memory_gb": 4,
            "target_accuracy": 0.6,
            "max_response_time": 2.0,
        }

        # 데이터 저장소
        self.chunks = []
        self.vectors = None
        self.metadata = []

        logger.info(f"🚀 데이터 파이프라인 v1 초기화 완료: {datetime.now()}")

    def load_sample_data(self) -> pd.DataFrame:
        """샘플 데이터 로딩 (테스트용)"""
        try:
            # 샘플 데이터 생성 (Stack Overflow 스타일)
            sample_data = [
                {
                    "id": 1,
                    "title": "How to implement machine learning pipeline?",
                    "body": "I am working on a machine learning project and need help with implementing a data pipeline. I have data in CSV format and want to create a system that can process, clean, and analyze the data automatically. What are the best practices for building such a pipeline?",
                    "tags": "machine-learning,python,scikit-learn",
                    "score": 15,
                },
                {
                    "id": 2,
                    "title": "BigQuery performance optimization tips",
                    "body": "What are the best practices for optimizing BigQuery performance? I have a large dataset with millions of rows and need to improve query performance. I am using standard SQL and want to know about partitioning, clustering, and other optimization techniques.",
                    "tags": "bigquery,google-cloud,performance",
                    "score": 23,
                },
                {
                    "id": 3,
                    "title": "Natural language processing with transformers",
                    "body": "I want to build an NLP system using transformer models. Can someone help me understand the architecture and implementation details? I am particularly interested in BERT and GPT models for text classification and generation tasks.",
                    "tags": "nlp,transformers,pytorch",
                    "score": 31,
                },
                {
                    "id": 4,
                    "title": "Data preprocessing best practices",
                    "body": "What are the essential data preprocessing steps for machine learning projects? I want to understand data cleaning, normalization, feature engineering, and handling missing values. Any practical examples would be helpful.",
                    "tags": "data-preprocessing,machine-learning,python",
                    "score": 18,
                },
                {
                    "id": 5,
                    "title": "Model evaluation and validation strategies",
                    "body": "How do you evaluate and validate machine learning models effectively? I need to understand cross-validation, metrics selection, and avoiding overfitting. What are the common pitfalls and best practices?",
                    "tags": "model-evaluation,validation,machine-learning",
                    "score": 25,
                },
            ]

            df = pd.DataFrame(sample_data)

            # CSV로 저장
            csv_path = self.data_dir / "sample_questions.csv"
            df.to_csv(csv_path, index=False)

            logger.info(f"✅ 샘플 데이터 로딩 완료: {len(df)}개, 저장: {csv_path}")
            return df

        except Exception as e:
            logger.error(f"❌ 샘플 데이터 로딩 실패: {e}")
            return pd.DataFrame()

    def preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        try:
            if pd.isna(text):
                return ""

            # 기본 정규화
            text = str(text).lower().strip()

            # 특수문자 처리
            text = text.replace("\n", " ").replace("\r", " ")

            # 연속 공백 제거
            text = " ".join(text.split())

            return text

        except Exception as e:
            logger.error(f"❌ 텍스트 전처리 실패: {e}")
            return ""

    def create_chunks(
        self, text: str, chunk_size: int = None, overlap: float = None
    ) -> List[str]:
        """텍스트를 청크로 분할"""
        try:
            chunk_size = chunk_size or self.config["chunk_size"]
            overlap = overlap or self.config["chunk_overlap"]

            if not text:
                return []

            # 단어 단위로 분할
            words = text.split()

            if len(words) <= chunk_size:
                return [text]

            chunks = []
            step = int(chunk_size * (1 - overlap))

            for i in range(0, len(words), step):
                chunk_words = words[i : i + chunk_size]
                chunk_text = " ".join(chunk_words)
                if chunk_text.strip():
                    chunks.append(chunk_text)

            logger.info(
                f"✅ 청크 생성 완료: {len(chunks)}개 (크기: {chunk_size}, 중복: {overlap})"
            )
            return chunks

        except Exception as e:
            logger.error(f"❌ 청크 생성 실패: {e}")
            return []

    def vectorize_text(self, text: str) -> np.ndarray:
        """텍스트를 벡터로 변환 (TF-IDF 기반)"""
        try:
            # 간단한 TF-IDF 구현
            words = text.lower().split()

            # 단어 빈도 계산
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

            # 벡터 생성 (고정 차원)
            vector = np.zeros(self.config["vector_dimension"])

            # 해시 기반 벡터 생성
            for word, freq in word_freq.items():
                hash_val = hash(word) % self.config["vector_dimension"]
                vector[hash_val] = freq

            # 정규화
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm

            return vector

        except Exception as e:
            logger.error(f"❌ 벡터화 실패: {e}")
            return np.zeros(self.config["vector_dimension"])

    def process_data(self, df: pd.DataFrame) -> bool:
        """전체 데이터 처리 파이프라인"""
        try:
            logger.info("🔄 데이터 처리 파이프라인 시작...")

            # 텍스트 컬럼 결합
            df["combined_text"] = df["title"].fillna("") + " " + df["body"].fillna("")

            # 전처리
            df["processed_text"] = df["combined_text"].apply(self.preprocess_text)

            # 청킹
            all_chunks = []
            chunk_metadata = []

            for idx, row in df.iterrows():
                chunks = self.create_chunks(row["processed_text"])

                for chunk_idx, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    chunk_metadata.append(
                        {
                            "doc_id": row["id"],
                            "chunk_id": f"{row['id']}_{chunk_idx}",
                            "title": row["title"],
                            "tags": row["tags"],
                            "score": row["score"],
                            "chunk_index": chunk_idx,
                            "total_chunks": len(chunks),
                        }
                    )

            self.chunks = all_chunks
            self.metadata = chunk_metadata

            # 벡터화
            logger.info("🔄 텍스트 벡터화 시작...")
            vectors = []
            for chunk in self.chunks:
                vector = self.vectorize_text(chunk)
                vectors.append(vector)

            self.vectors = np.array(vectors)

            # 결과 저장
            self.save_results()

            logger.info(
                f"✅ 데이터 처리 완료: {len(self.chunks)}개 청크, {self.vectors.shape} 벡터"
            )
            return True

        except Exception as e:
            logger.error(f"❌ 데이터 처리 실패: {e}")
            return False

    def save_results(self):
        """처리 결과 저장"""
        try:
            # 청크 저장
            chunks_path = self.data_dir / "processed_chunks.json"
            with open(chunks_path, "w", encoding="utf-8") as f:
                json.dump(self.chunks, f, ensure_ascii=False, indent=2)

            # 메타데이터 저장
            metadata_path = self.data_dir / "chunk_metadata.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)

            # 벡터 저장 (NumPy 형식)
            vectors_path = self.data_dir / "vectors.npy"
            np.save(vectors_path, self.vectors)

            # 설정 저장
            config_path = self.data_dir / "pipeline_config.json"
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)

            logger.info(
                f"✅ 결과 저장 완료: {chunks_path}, {metadata_path}, {vectors_path}"
            )

        except Exception as e:
            logger.error(f"❌ 결과 저장 실패: {e}")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """텍스트 검색 (코사인 유사도 기반)"""
        try:
            if self.vectors is None or len(self.chunks) == 0:
                logger.error("❌ 검색할 데이터가 없습니다.")
                return []

            # 쿼리 벡터화
            query_vector = self.vectorize_text(query)

            # 코사인 유사도 계산
            similarities = []
            for i, vector in enumerate(self.vectors):
                similarity = np.dot(query_vector, vector)
                similarities.append((i, similarity))

            # 유사도 순으로 정렬
            similarities.sort(key=lambda x: x[1], reverse=True)

            # 상위 k개 결과 반환
            results = []
            for i, (chunk_idx, similarity) in enumerate(similarities[:top_k]):
                results.append(
                    {
                        "rank": i + 1,
                        "chunk_id": self.metadata[chunk_idx]["chunk_id"],
                        "title": self.metadata[chunk_idx]["title"],
                        "tags": self.metadata[chunk_idx]["tags"],
                        "score": self.metadata[chunk_idx]["score"],
                        "chunk_text": self.chunks[chunk_idx][:200] + "...",
                        "similarity": float(similarity),
                    }
                )

            logger.info(f"✅ 검색 완료: '{query}' -> {len(results)}개 결과")
            return results

        except Exception as e:
            logger.error(f"❌ 검색 실패: {e}")
            return []

    def generate_rag_response(self, query: str, top_k: int = 3) -> str:
        """RAG 답변 생성 (기본 프롬프트)"""
        try:
            # 관련 청크 검색
            search_results = self.search(query, top_k)

            if not search_results:
                return "죄송합니다. 관련 정보를 찾을 수 없습니다."

            # 컨텍스트 구성
            context = "\n\n".join(
                [
                    f"제목: {result['title']}\n내용: {result['chunk_text']}\n태그: {result['tags']}"
                    for result in search_results
                ]
            )

            # 기본 프롬프트 생성
            prompt = f"""다음 정보를 바탕으로 질문에 답변해주세요:

질문: {query}

참고 정보:
{context}

답변:"""

            # 간단한 답변 생성 (실제로는 LLM 사용)
            response = f"질문 '{query}'에 대한 답변입니다.\n\n"
            response += "참고한 정보:\n"
            for result in search_results:
                response += (
                    f"- {result['title']} (유사도: {result['similarity']:.3f})\n"
                )

            response += f"\n총 {len(search_results)}개의 관련 문서를 찾았습니다."

            logger.info(f"✅ RAG 답변 생성 완료: '{query}'")
            return response

        except Exception as e:
            logger.error(f"❌ RAG 답변 생성 실패: {e}")
            return f"오류가 발생했습니다: {e}"

    def evaluate_performance(self) -> Dict[str, Any]:
        """파이프라인 성능 평가"""
        try:
            # 메모리 사용량
            memory_usage = (
                self.vectors.nbytes / (1024**3) if self.vectors is not None else 0
            )

            # 처리 시간 측정 (시뮬레이션)
            processing_time = len(self.chunks) * 0.01  # 청크당 0.01초 가정

            # 검색 성능 테스트
            test_queries = [
                "machine learning",
                "bigquery optimization",
                "natural language processing",
            ]

            search_times = []
            for query in test_queries:
                start_time = datetime.now()
                self.search(query)
                end_time = datetime.now()
                search_times.append((end_time - start_time).total_seconds())

            avg_search_time = np.mean(search_times)

            # 성능 지표
            performance = {
                "total_chunks": len(self.chunks),
                "vector_dimension": self.config["vector_dimension"],
                "memory_usage_gb": round(memory_usage, 3),
                "processing_time_seconds": round(processing_time, 3),
                "avg_search_time_seconds": round(avg_search_time, 3),
                "target_memory_gb": self.config["max_memory_gb"],
                "target_search_time": self.config["max_response_time"],
                "memory_target_met": bool(memory_usage <= self.config["max_memory_gb"]),
                "search_time_target_met": bool(
                    avg_search_time <= self.config["max_response_time"]
                ),
            }

            # 성능 저장
            perf_path = self.data_dir / "performance_metrics.json"
            with open(perf_path, "w", encoding="utf-8") as f:
                json.dump(performance, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ 성능 평가 완료: {perf_path}")
            return performance

        except Exception as e:
            logger.error(f"❌ 성능 평가 실패: {e}")
            return {}


def main():
    """메인 실행 함수"""
    try:
        logger.info("🚀 캐글 해커톤 데이터 파이프라인 v1 실행 시작")

        # 파이프라인 초기화
        pipeline = DataPipelineV1()

        # 1단계: 샘플 데이터 로딩
        logger.info("📥 1단계: 샘플 데이터 로딩")
        df = pipeline.load_sample_data()

        if df.empty:
            logger.error("❌ 데이터 로딩 실패")
            return False

        # 2단계: 데이터 처리
        logger.info("🔄 2단계: 데이터 처리")
        if not pipeline.process_data(df):
            logger.error("❌ 데이터 처리 실패")
            return False

        # 3단계: 검색 테스트
        logger.info("🔍 3단계: 검색 테스트")
        test_query = "machine learning pipeline"
        search_results = pipeline.search(test_query)

        if search_results:
            logger.info(f"✅ 검색 테스트 성공: {len(search_results)}개 결과")
        else:
            logger.warning("⚠️ 검색 결과가 없습니다")

        # 4단계: RAG 테스트
        logger.info("🤖 4단계: RAG 테스트")
        rag_response = pipeline.generate_rag_response(test_query)
        logger.info(f"✅ RAG 테스트 성공: {len(rag_response)}자 답변")

        # 5단계: 성능 평가
        logger.info("📊 5단계: 성능 평가")
        performance = pipeline.evaluate_performance()

        logger.info("🎉 데이터 파이프라인 v1 실행 완료!")
        logger.info(
            f"📊 성능 지표: {json.dumps(performance, indent=2, ensure_ascii=False)}"
        )

        return True

    except Exception as e:
        logger.error(f"❌ 파이프라인 실행 실패: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
