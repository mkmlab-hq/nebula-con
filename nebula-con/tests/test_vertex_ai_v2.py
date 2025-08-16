#!/usr/bin/env python3
"""
업그레이드된 Vertex AI SDK 테스트 스크립트
새로운 버전에서 GenerativeModel 클래스 사용 가능 여부 확인
"""

from google.cloud import aiplatform
import os


def test_upgraded_vertex_ai():
    """업그레이드된 Vertex AI SDK를 테스트합니다."""
    
    print("🧪 업그레이드된 Vertex AI SDK 테스트 시작...")
    
    try:
        # 1. SDK 버전 확인
        print(f"✅ aiplatform 버전: {aiplatform.__version__}")
        
        # 2. 사용 가능한 클래스 확인
        available_classes = [attr for attr in dir(aiplatform) if 'Model' in attr]
        print(f"✅ 사용 가능한 Model 클래스: {available_classes}")
        
        # 3. GenerativeModel 클래스 존재 확인
        try:
            from google.cloud.aiplatform import GenerativeModel
            print("✅ GenerativeModel 클래스 import 성공!")
            
            # 4. 모델 초기화 테스트
            aiplatform.init(
                project="persona-diary-service",
                location="us-central1"
            )
            
            model = GenerativeModel("gemini-1.5-flash")
            print("✅ GenerativeModel 초기화 성공!")
            
            # 5. 간단한 테스트
            response = model.generate_content("Hello, test message")
            print(f"✅ 모델 응답 성공: {response.text[:100]}...")
            
            return True
            
        except ImportError as e:
            print(f"❌ GenerativeModel 클래스 import 실패: {str(e)}")
            return False
            
        except Exception as e:
            print(f"❌ 모델 테스트 실패: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ Vertex AI SDK 테스트 실패: {str(e)}")
        return False


def test_alternative_models():
    """대안 모델 클래스들을 테스트합니다."""
    
    print("\n🔍 대안 모델 클래스 테스트...")
    
    try:
        # 1. TextGenerationModel 테스트
        try:
            from google.cloud.aiplatform import TextGenerationModel
            print("✅ TextGenerationModel 클래스 import 성공!")
            
            aiplatform.init(
                project="persona-diary-service",
                location="us-central1"
            )
            
            model = TextGenerationModel.from_pretrained("gemini-pro")
            print("✅ TextGenerationModel 초기화 성공!")
            
            response = model.predict("Hello, test")
            print(f"✅ 모델 응답 성공: {response.text[:100]}...")
            
            return True
            
        except ImportError as e:
            print(f"❌ TextGenerationModel 클래스 import 실패: {str(e)}")
        
        # 2. TextEmbeddingModel 테스트
        try:
            from google.cloud.aiplatform import TextEmbeddingModel
            print("✅ TextEmbeddingModel 클래스 import 성공!")
            
            model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
            print("✅ TextEmbeddingModel 초기화 성공!")
            
            embeddings = model.get_embeddings(["test text"])
            print(f"✅ 임베딩 생성 성공: {len(embeddings)}개")
            
            return True
            
        except ImportError as e:
            print(f"❌ TextEmbeddingModel 클래스 import 실패: {str(e)}")
        
        return False
        
    except Exception as e:
        print(f"❌ 대안 모델 테스트 실패: {str(e)}")
        return False


def main():
    """메인 실행 함수"""
    print("🚨 업그레이드된 Vertex AI SDK 테스트 시작...")
    
    try:
        # 1. 기본 GenerativeModel 테스트
        success1 = test_upgraded_vertex_ai()
        
        # 2. 대안 모델 클래스 테스트
        success2 = test_alternative_models()
        
        if success1 or success2:
            print("\n🎉 Vertex AI SDK 테스트 성공!")
            print("✅ 이제 AI 모델을 사용할 수 있습니다!")
        else:
            print("\n❌ 모든 Vertex AI 모델 테스트 실패")
            print("🔍 다른 접근법이 필요합니다")
        
        return 0
        
    except Exception as e:
        print(f"❌ 메인 테스트 실패: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 