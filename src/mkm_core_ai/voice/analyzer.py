"""
음성 분석 전체 과정을 총괄하는 메인 모듈
"""
import numpy as np
import librosa
import scipy.signal as signal
from typing import Dict, Any, Optional
import logging

# my-voice-analysis 라이브러리 import
try:
    from my_voice_analysis import analyze_voice
    MY_VOICE_ANALYSIS_AVAILABLE = True
except ImportError:
    MY_VOICE_ANALYSIS_AVAILABLE = False
    logging.warning("my-voice-analysis 라이브러리를 사용할 수 없습니다. 기본 분석만 사용합니다.")

logger = logging.getLogger(__name__)

class VoiceAnalyzer:
    """
음성 분석 클래스
"""
    
    def __init__(self):
        self.sample_rate = 22050  # 기본 샘플링 레이트
        
    def analyze_voice_file(self, audio_file_path: str) -> Dict[str, Any]:
        """
음성 파일 분석 메인 함수
"""
        try:
            # 오디오 파일 로드
            y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
            
            results = {}
            
            # 1. 기본 음성 분석 (my-voice-analysis 사용)
            if MY_VOICE_ANALYSIS_AVAILABLE:
                basic_analysis = self._analyze_with_my_voice_analysis(audio_file_path)
                results.update(basic_analysis)
            
            # 2. 고급 음성 분석
            advanced_analysis = self._advanced_voice_analysis(y, sr)
            results.update(advanced_analysis)
            
            # 3. 한의학 오음(五音) 분석
            five_sounds_analysis = self._analyze_five_sounds(y, sr)
            results.update(five_sounds_analysis)
            
            # 4. 건강 상태 평가
            health_assessment = self._assess_health_status(results)
            results['health_assessment'] = health_assessment
            
            return results
            
        except Exception as e:
            logger.error(f"음성 분석 중 오류 발생: {str(e)}")
            raise
    # ... 이하 기존 코드 ...
