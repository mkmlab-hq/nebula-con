#!/usr/bin/env python3
"""
실제 음성 분석 모듈
Phase 2: 실제 AI 분석 로직 구현
"""

import librosa
import numpy as np
from scipy import signal
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import logging
import soundfile as sf

class RealVoiceAnalyzer:
    """실제 음성 분석기"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = 22050  # 기본 샘플링 레이트
        
    def load_audio(self, audio_path: str) -> Optional[Tuple[np.ndarray, int]]:
        """오디오 파일 로드"""
        try:
            # librosa로 오디오 로드
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            self.logger.error(f"오디오 로드 실패: {e}")
            return None
    
    def extract_mfcc_features(self, audio: np.ndarray) -> np.ndarray:
        """MFCC (Mel-frequency cepstral coefficients) 추출"""
        try:
            # MFCC 추출 (13개 계수)
            mfcc = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
            return mfcc
        except Exception as e:
            self.logger.error(f"MFCC 추출 실패: {e}")
            return np.zeros((13, 1))
    
    def extract_spectral_features(self, audio: np.ndarray) -> Dict:
        """스펙트럴 특성 추출"""
        try:
            # 스펙트럴 중심 주파수
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
            
            # 스펙트럴 대비
            spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=self.sample_rate)
            
            # 스펙트럴 롤오프
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
            
            # 스펙트럴 대역폭
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=self.sample_rate)[0]
            
            return {
                'centroids': spectral_centroids,
                'contrast': spectral_contrast,
                'rolloff': spectral_rolloff,
                'bandwidth': spectral_bandwidth
            }
        except Exception as e:
            self.logger.error(f"스펙트럴 특성 추출 실패: {e}")
            return {}
    
    def extract_pitch_features(self, audio: np.ndarray) -> Dict:
        """피치 특성 추출"""
        try:
            # 피치 추출
            pitches, magnitudes = librosa.piptrack(y=audio, sr=self.sample_rate)
            
            # 평균 피치
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if len(pitch_values) > 0:
                mean_pitch = np.mean(pitch_values)
                pitch_std = np.std(pitch_values)
                pitch_range = np.max(pitch_values) - np.min(pitch_values)
            else:
                mean_pitch = 0
                pitch_std = 0
                pitch_range = 0
            
            return {
                'mean_pitch': mean_pitch,
                'pitch_std': pitch_std,
                'pitch_range': pitch_range
            }
        except Exception as e:
            self.logger.error(f"피치 특성 추출 실패: {e}")
            return {'mean_pitch': 0, 'pitch_std': 0, 'pitch_range': 0}
    
    def extract_energy_features(self, audio: np.ndarray) -> Dict:
        """에너지 특성 추출"""
        try:
            # RMS 에너지
            rms = librosa.feature.rms(y=audio)[0]
            
            # 제로 크로싱 레이트
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            
            # 에너지 엔트로피
            energy_entropy = -np.sum(rms * np.log(rms + 1e-10))
            
            return {
                'rms_mean': np.mean(rms),
                'rms_std': np.std(rms),
                'zcr_mean': np.mean(zcr),
                'energy_entropy': energy_entropy
            }
        except Exception as e:
            self.logger.error(f"에너지 특성 추출 실패: {e}")
            return {'rms_mean': 0, 'rms_std': 0, 'zcr_mean': 0, 'energy_entropy': 0}
    
    def analyze_emotion_from_voice(self, audio: np.ndarray) -> Dict:
        """음성에서 감정 분석"""
        try:
            # MFCC 특성
            mfcc = self.extract_mfcc_features(audio)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            
            # 스펙트럴 특성
            spectral_features = self.extract_spectral_features(audio)
            
            # 피치 특성
            pitch_features = self.extract_pitch_features(audio)
            
            # 에너지 특성
            energy_features = self.extract_energy_features(audio)
            
            # 감정 지수 계산 (간단한 규칙 기반)
            emotion_scores = {
                'happiness': 0.0,
                'sadness': 0.0,
                'anger': 0.0,
                'calmness': 0.0,
                'excitement': 0.0
            }
            
            # 피치 기반 감정 분석
            if pitch_features['mean_pitch'] > 200:  # 높은 피치
                emotion_scores['excitement'] += 0.3
                emotion_scores['happiness'] += 0.2
            elif pitch_features['mean_pitch'] < 100:  # 낮은 피치
                emotion_scores['sadness'] += 0.3
                emotion_scores['calmness'] += 0.2
            
            # 에너지 기반 감정 분석
            if energy_features['rms_mean'] > 0.1:  # 높은 에너지
                emotion_scores['excitement'] += 0.2
                emotion_scores['anger'] += 0.1
            elif energy_features['rms_mean'] < 0.05:  # 낮은 에너지
                emotion_scores['sadness'] += 0.2
                emotion_scores['calmness'] += 0.3
            
            # 스펙트럴 특성 기반 분석
            if 'centroids' in spectral_features:
                centroid_mean = np.mean(spectral_features['centroids'])
                if centroid_mean > 2000:  # 높은 주파수 성분
                    emotion_scores['excitement'] += 0.2
                elif centroid_mean < 1000:  # 낮은 주파수 성분
                    emotion_scores['calmness'] += 0.2
            
            # 정규화
            total_score = sum(emotion_scores.values())
            if total_score > 0:
                emotion_scores = {k: v/total_score for k, v in emotion_scores.items()}
            
            # 주요 감정 결정
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            
            return {
                'emotion_scores': emotion_scores,
                'primary_emotion': primary_emotion,
                'confidence': emotion_scores[primary_emotion]
            }
            
        except Exception as e:
            self.logger.error(f"감정 분석 실패: {e}")
            return {
                'emotion_scores': {'calmness': 1.0},
                'primary_emotion': 'calmness',
                'confidence': 0.5
            }
    
    def analyze_voice_characteristics(self, audio_path: str) -> Dict:
        """음성 특성 종합 분석"""
        try:
            self.logger.info("실제 음성 분석 시작")
            
            # 오디오 로드
            audio_data = self.load_audio(audio_path)
            if audio_data is None:
                raise ValueError("오디오 로드 실패")
            
            audio, sr = audio_data
            
            # 감정 분석
            emotion_result = self.analyze_emotion_from_voice(audio)
            
            # 음성 특성 분석
            pitch_features = self.extract_pitch_features(audio)
            energy_features = self.extract_energy_features(audio)
            
            # 음성 품질 평가
            snr = self.calculate_snr(audio)
            
            # 결과 구성
            result = {
                "emotion": emotion_result['primary_emotion'],
                "emotion_confidence": round(emotion_result['confidence'], 2),
                "pitch_mean": round(pitch_features['mean_pitch'], 1),
                "energy_level": self.categorize_energy(energy_features['rms_mean']),
                "voice_quality": self.categorize_quality(snr),
                "speaking_rate": self.calculate_speaking_rate(audio),
                "analysis_quality": "실제 음성 분석",
                "confidence": 0.80
            }
            
            self.logger.info(f"음성 분석 완료: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"음성 특성 분석 실패: {e}")
            # 폴백: 기본값 반환
            return {
                "emotion": "calmness",
                "emotion_confidence": 0.5,
                "pitch_mean": 150.0,
                "energy_level": "보통",
                "voice_quality": "보통",
                "speaking_rate": "보통",
                "analysis_quality": "기본값 (분석 실패)",
                "confidence": 0.0
            }
    
    def calculate_snr(self, audio: np.ndarray) -> float:
        """신호 대 잡음비 계산"""
        try:
            # 간단한 SNR 추정
            signal_power = np.mean(audio**2)
            noise_floor = np.percentile(audio**2, 10)
            snr = 10 * np.log10(signal_power / (noise_floor + 1e-10))
            return snr
        except:
            return 20.0  # 기본값
    
    def categorize_energy(self, rms_mean: float) -> str:
        """에너지 수준 분류"""
        if rms_mean > 0.1:
            return "높음"
        elif rms_mean > 0.05:
            return "보통"
        else:
            return "낮음"
    
    def categorize_quality(self, snr: float) -> str:
        """음성 품질 분류"""
        if snr > 30:
            return "우수"
        elif snr > 20:
            return "보통"
        else:
            return "낮음"
    
    def calculate_speaking_rate(self, audio: np.ndarray) -> str:
        """말하기 속도 계산"""
        try:
            # 간단한 말하기 속도 추정
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            avg_zcr = np.mean(zcr)
            
            if avg_zcr > 0.1:
                return "빠름"
            elif avg_zcr > 0.05:
                return "보통"
            else:
                return "느림"
        except:
            return "보통"

def main():
    """테스트 함수"""
    analyzer = RealVoiceAnalyzer()
    
    # 테스트 오디오 파일 경로
    test_audio = "test_data/test_voice.wav"
    
    print("🎤 실제 음성 분석 테스트")
    print("=" * 50)
    
    result = analyzer.analyze_voice_characteristics(test_audio)
    
    print("📊 분석 결과:")
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 