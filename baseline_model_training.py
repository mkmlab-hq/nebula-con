#!/usr/bin/env python3
"""
🏆 해커톤 베이스라인 모델 훈련 스크립트
BigQuery에서 저장된 임베딩 데이터를 사용하여 RandomForest 분류기를 훈련합니다.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
import warnings
warnings.filterwarnings('ignore')

class BaselineModelTrainer:
    def __init__(self, project_id: str, dataset_id: str):
        """베이스라인 모델 훈련기 초기화"""
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id)
        self.table_id = f"{self.project_id}.{self.dataset_id}.hacker_news_embeddings_pseudo"
        
    def load_data_from_bigquery(self) -> pd.DataFrame:
        """BigQuery에서 임베딩 데이터 로드"""
        try:
            print("🔍 BigQuery에서 임베딩 데이터 로드 중...")
            
            query = f"""
            SELECT 
                id,
                title,
                text,
                combined_text,
                embedding
            FROM `{self.table_id}`
            ORDER BY id
            """
            
            df = self.client.query(query).to_dataframe()
            print(f"✅ 데이터 로드 완료: {len(df)}개 행")
            print(f"📊 데이터 형태: {df.shape}")
            print(f"🔍 컬럼: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {str(e)}")
            return pd.DataFrame()
    
    def prepare_features_and_labels(self, df: pd.DataFrame):
        """특성(X)과 레이블(Y) 준비"""
        try:
            print("\n🔍 특성과 레이블 준비 중...")
            
            # 임베딩 벡터를 특성으로 변환
            embeddings = np.array(df['embedding'].tolist())
            print(f"📊 임베딩 벡터 형태: {embeddings.shape}")
            
            # 가상의 레이블 생성 (실제 대회에서는 실제 레이블 사용)
            # 여기서는 텍스트 길이를 기반으로 한 간단한 분류 문제 생성
            text_lengths = df['combined_text'].str.len()
            labels = (text_lengths > text_lengths.median()).astype(int)
            
            print(f"📊 레이블 분포:")
            print(f"   - 클래스 0: {sum(labels == 0)}개")
            print(f"   - 클래스 1: {sum(labels == 1)}개")
            
            return embeddings, labels
            
        except Exception as e:
            print(f"❌ 특성/레이블 준비 실패: {str(e)}")
            return None, None
    
    def train_baseline_model(self, X, y):
        """RandomForest 베이스라인 모델 훈련"""
        try:
            print("\n🚀 RandomForest 베이스라인 모델 훈련 시작...")
            
            # 데이터 분할 (80% 훈련, 20% 테스트)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            print(f"📊 훈련 데이터: {X_train.shape[0]}개")
            print(f"📊 테스트 데이터: {X_test.shape[0]}개")
            
            # 모델 초기화 및 훈련
            rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            print("🔄 모델 훈련 중...")
            rf_model.fit(X_train, y_train)
            print("✅ 모델 훈련 완료!")
            
            # 예측
            y_pred = rf_model.predict(X_test)
            y_pred_proba = rf_model.predict_proba(X_test)
            
            return rf_model, X_train, X_test, y_train, y_test, y_pred, y_pred_proba
            
        except Exception as e:
            print(f"❌ 모델 훈련 실패: {str(e)}")
            return None, None, None, None, None, None, None
    
    def hyperparameter_tuning(self, X, y):
        """GridSearchCV를 사용한 하이퍼파라미터 튜닝"""
        try:
            print("\n🔍 하이퍼파라미터 튜닝 시작...")
            
            # 파라미터 그리드 정의
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2', None]
            }
            
            print(f"📊 탐색할 파라미터 조합: {len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split']) * len(param_grid['min_samples_leaf']) * len(param_grid['max_features'])}개")
            
            # GridSearchCV 객체 생성
            rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
            grid_search = GridSearchCV(
                estimator=rf_base,
                param_grid=param_grid,
                cv=5,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            print("🔄 GridSearchCV 실행 중... (시간이 다소 소요될 수 있습니다)")
            grid_search.fit(X, y)
            
            print("✅ 하이퍼파라미터 튜닝 완료!")
            
            # 최적 결과 출력
            print(f"\n🏆 최적 파라미터:")
            for param, value in grid_search.best_params_.items():
                print(f"   - {param}: {value}")
            
            print(f"\n🎯 최적 교차 검증 점수: {grid_search.best_score_:.4f}")
            print(f"📊 최적 모델의 표준편차: {grid_search.cv_results_['std_test_score'][grid_search.best_index_]:.4f}")
            
            # 상위 5개 결과 출력
            print(f"\n📈 상위 5개 파라미터 조합:")
            cv_results = pd.DataFrame(grid_search.cv_results_)
            top_5 = cv_results.nlargest(5, 'mean_test_score')[['mean_test_score', 'std_test_score', 'params']]
            
            for i, (_, row) in enumerate(top_5.iterrows()):
                print(f"   {i+1}위: 점수 {row['mean_test_score']:.4f} (±{row['std_test_score']:.4f})")
                print(f"        파라미터: {row['params']}")
            
            return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_
            
        except Exception as e:
            print(f"❌ 하이퍼파라미터 튜닝 실패: {str(e)}")
            return None, None, None
    
    def evaluate_model(self, y_true, y_pred, y_pred_proba, X_test, y_test):
        """모델 성능 평가"""
        try:
            print("\n📊 모델 성능 평가 결과:")
            print("=" * 50)
            
            # 기본 성능 지표
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted')
            recall = recall_score(y_true, y_pred, average='weighted')
            f1 = f1_score(y_true, y_pred, average='weighted')
            
            print(f"🎯 정확도 (Accuracy): {accuracy:.4f}")
            print(f"🎯 정밀도 (Precision): {precision:.4f}")
            print(f"🎯 재현율 (Recall): {recall:.4f}")
            print(f"🎯 F1-점수: {f1:.4f}")
            
            # 교차 검증
            print("\n🔄 교차 검증 (5-fold) 결과:")
            cv_scores = cross_val_score(
                RandomForestClassifier(n_estimators=100, random_state=42),
                X_test, y_test, cv=5, scoring='accuracy'
            )
            print(f"   - 각 fold 점수: {cv_scores}")
            print(f"   - 평균 점수: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            # 상세 분류 보고서
            print("\n📋 상세 분류 보고서:")
            print(classification_report(y_true, y_pred))
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
        except Exception as e:
            print(f"❌ 모델 평가 실패: {str(e)}")
            return None
    
    def plot_results(self, y_true, y_pred, y_pred_proba):
        """결과 시각화"""
        try:
            print("\n📈 결과 시각화 생성 중...")
            
            # 1. 혼동 행렬
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 3, 1)
            cm = confusion_matrix(y_true, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title('혼동 행렬 (Confusion Matrix)')
            plt.ylabel('실제 값')
            plt.xlabel('예측 값')
            
            # 2. 예측 확률 분포
            plt.subplot(1, 3, 2)
            plt.hist(y_pred_proba[:, 1], bins=20, alpha=0.7, color='skyblue')
            plt.title('클래스 1 예측 확률 분포')
            plt.xlabel('예측 확률')
            plt.ylabel('빈도')
            
            # 3. 성능 지표 막대 그래프
            plt.subplot(1, 3, 3)
            metrics = ['정확도', '정밀도', '재현율', 'F1-점수']
            scores = [accuracy_score(y_true, y_pred), 
                     precision_score(y_true, y_pred, average='weighted'),
                     recall_score(y_true, y_pred, average='weighted'),
                     f1_score(y_true, y_pred, average='weighted')]
            
            plt.bar(metrics, scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            plt.title('모델 성능 지표')
            plt.ylabel('점수')
            plt.ylim(0, 1)
            
            # y축 레이블 회전
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig('baseline_model_results.png', dpi=300, bbox_inches='tight')
            print("✅ 결과 시각화 저장 완료: baseline_model_results.png")
            
        except Exception as e:
            print(f"❌ 시각화 생성 실패: {str(e)}")
    
    def run_complete_training(self):
        """전체 훈련 파이프라인 실행"""
        print("🚀 해커톤 베이스라인 모델 훈련 시작!")
        print("=" * 60)
        
        # 1. 데이터 로드
        df = self.load_data_from_bigquery()
        if df.empty:
            return None
        
        # 2. 특성과 레이블 준비
        X, y = self.prepare_features_and_labels(df)
        if X is None:
            return None
        
        # 3. 모델 훈련
        model, X_train, X_test, y_train, y_test, y_pred, y_pred_proba = self.train_baseline_model(X, y)
        if model is None:
            return None
        
        # 4. 모델 평가
        metrics = self.evaluate_model(y_test, y_pred, y_pred_proba, X_test, y_test)
        if metrics is None:
            return None
        
        # 5. 결과 시각화
        self.plot_results(y_test, y_pred, y_pred_proba)
        
        # 6. 하이퍼파라미터 튜닝
        print("\n" + "=" * 60)
        print("🔍 하이퍼파라미터 튜닝 단계")
        print("=" * 60)
        
        best_model, best_params, best_score = self.hyperparameter_tuning(X, y)
        
        # 7. 최종 요약
        print("\n" + "=" * 60)
        print("🏆 베이스라인 모델 훈련 및 튜닝 완료!")
        print("=" * 60)
        print(f"📊 베이스라인 모델 성능:")
        print(f"   - 정확도: {metrics['accuracy']:.4f}")
        print(f"   - F1-점수: {metrics['f1']:.4f}")
        print(f"   - 교차 검증 평균: {metrics['cv_mean']:.4f}")
        print(f"   - 교차 검증 표준편차: {metrics['cv_std']:.4f}")
        
        if best_score:
            print(f"\n🏆 튜닝된 모델 성능:")
            print(f"   - 최적 교차 검증 점수: {best_score:.4f}")
            print(f"   - 성능 향상: {best_score - metrics['cv_mean']:.4f}")
        
        print("\n💡 다음 단계:")
        print("   1. 더 많은 데이터로 모델 재훈련")
        print("   2. 고급 모델 실험 (딥러닝, 앙상블)")
        print("   3. Kaggle 제출 준비")
        
        return model, metrics, best_model, best_params, best_score

def main():
    """메인 실행 함수"""
    # 설정
    PROJECT_ID = "persona-diary-service"
    DATASET_ID = "nebula_con_kaggle"
    
    # 훈련기 생성 및 실행
    trainer = BaselineModelTrainer(PROJECT_ID, DATASET_ID)
    results = trainer.run_complete_training()
    
    if results:
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
    else:
        print("\n❌ 훈련 과정에서 오류가 발생했습니다.")

if __name__ == "__main__":
    main() 