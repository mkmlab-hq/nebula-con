# 🚀 BigQuery ML 원격 모델 생성 실행 가이드

## 📋 **실행 전 준비사항**

### **필수 조건 확인**
- ✅ GCP 프로젝트: `persona-diary-service`
- ✅ BigQuery 데이터셋: `nebula_con_kaggle`
- ✅ Vertex AI API: 활성화됨
- ✅ BigQuery 연결: 정상 작동

### **실행 순서**
**⚠️ 반드시 순서대로 실행해야 합니다!**

---

## 🔗 **1단계: Vertex AI Connection 생성**

### **BigQuery 콘솔에서 실행**
1. [BigQuery 콘솔](https://console.cloud.google.com/bigquery) 접속
2. 프로젝트 `persona-diary-service` 선택
3. 쿼리 에디터에서 다음 SQL 실행:

```sql
CREATE CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  connection_type = 'CLOUD_RESOURCE',
  resource_uri = '//aiplatform.googleapis.com/projects/persona-diary-service/locations/us-central1'
);
```

### **성공 확인**
- ✅ "Connection created successfully" 메시지 표시
- ❌ 오류 발생 시: 권한 문제일 수 있음

---

## 🔍 **2단계: Connection 생성 확인**

### **SQL 실행**
```sql
SELECT 
  connection_id, 
  connection_type, 
  properties
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.EXTERNAL_CONNECTIONS`
WHERE connection_id = 'my_vertex_ai_connection';
```

### **성공 확인**
- ✅ `my_vertex_ai_connection` 행이 표시됨
- ❌ 결과 없음: 1단계 재실행 필요

---

## 🤖 **3단계: 원격 모델 생성**

### **SQL 실행**
```sql
CREATE OR REPLACE MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`
REMOTE WITH CONNECTION `persona-diary-service.nebula_con_kaggle.my_vertex_ai_connection`
OPTIONS (
  remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1',
  endpoint = 'text-embedding-004'
);
```

### **성공 확인**
- ✅ "Model created successfully" 메시지 표시
- ❌ 오류 발생 시: Connection 문제일 수 있음

---

## ✅ **4단계: 모델 생성 확인**

### **SQL 실행**
```sql
SELECT 
  model_id, 
  model_type, 
  creation_time,
  options
FROM `persona-diary-service.nebula_con_kaggle.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_id = 'text_embedding_remote_model';
```

### **성공 확인**
- ✅ `text_embedding_remote_model` 행이 표시됨
- ❌ 결과 없음: 3단계 재실행 필요

---

## 🧪 **5단계: ML.GENERATE_EMBEDDING 함수 테스트**

### **기본 테스트**
```sql
SELECT ML.GENERATE_EMBEDDING(
  MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
  STRUCT('Hello, this is a test for Kaggle competition' AS content)
) AS embedding;
```

### **해커뉴스 데이터 테스트**
```sql
SELECT
  id,
  title,
  text,
  ML.GENERATE_EMBEDDING(
    MODEL `persona-diary-service.nebula_con_kaggle.text_embedding_remote_model`,
    STRUCT(CONCAT(IFNULL(title, ''), ' ', IFNULL(text, '')) AS content)
  ).ml_generate_embedding_result AS embedding
FROM
  `bigquery-public-data.hacker_news.full`
WHERE
  title IS NOT NULL OR text IS NOT NULL
LIMIT 5;
```

### **성공 확인**
- ✅ 임베딩 벡터가 정상적으로 생성됨
- ❌ 오류 발생: 모델 설정 문제일 수 있음

---

## 🚨 **문제 해결 가이드**

### **Connection 생성 실패**
- **오류**: "Permission denied"
- **해결**: BigQuery Admin 역할 확인
- **오류**: "Invalid connection type"
- **해결**: `CLOUD_RESOURCE` 타입 확인

### **모델 생성 실패**
- **오류**: "Connection not found"
- **해결**: 1-2단계 재실행
- **오류**: "Invalid endpoint"
- **해결**: `text-embedding-004` 엔드포인트 확인

### **ML 함수 테스트 실패**
- **오류**: "Model not found"
- **해결**: 3-4단계 재실행
- **오류**: "Invalid input"
- **해결**: STRUCT 형식 확인

---

## 🎯 **성공 후 다음 단계**

### **Kaggle 대회 준비 완료**
1. ✅ ML.GENERATE_EMBEDDING 함수 정상 작동
2. ✅ 해커뉴스 데이터 임베딩 생성 가능
3. ✅ 대량 데이터 처리 준비 완료

### **즉시 실행 가능한 작업**
1. **대량 임베딩 생성**: 1000개 이상의 해커뉴스 데이터
2. **임베딩 테이블 저장**: `hacker_news_embeddings` 테이블 생성
3. **베이스라인 모델**: RandomForest 분류기 훈련
4. **Kaggle 제출**: 첫 번째 리더보드 점수 획득

---

## 🏆 **최종 목표**

**이 가이드를 통해 `text_embedding_remote_model`을 성공적으로 생성하고, ML.GENERATE_EMBEDDING 함수를 사용하여 Kaggle 대회 1위를 달성할 수 있습니다!**

**사령관님, 이제 BigQuery 콘솔에서 단계별로 실행해 주세요!** 🚀 