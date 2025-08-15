#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my-voice-analysis 라이브러리 통합 종합 음성 분석기
"""
import numpy as np
import librosa
import scipy.signal as signal
from scipy.stats import skew, kurtosis
from typing import Dict, Any, Optional, List, Tuple
import logging
import time
from datetime import datetime
import functools
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import hashlib
import pickle
import os

# my-voice-analysis 라이브러리 import
try:
    from my_voice_analysis import analyze_voice
    MY_VOICE_ANALYSIS_AVAILABLE = True
    logging.info("✅ my-voice-analysis 라이브러리 로드 성공")
except ImportError as e:
    MY_VOICE_ANALYSIS_AVAILABLE = False
    logging.warning(f"❌ my-voice-analysis 라이브러리 로드 실패: {e}")
    # Fallback 구현 import
    try:
        from .my_voice_analysis_fallback import analyze_voice
        MY_VOICE_ANALYSIS_AVAILABLE = True
        logging.info("✅ my-voice-analysis fallback 구현 로드 성공")
    except ImportError as e2:
        logging.error(f"❌ fallback 구현도 로드 실패: {e2}")
        MY_VOICE_ANALYSIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class IntegratedVoiceAnalyzer:
    """
my-voice-analysis 라이브러리 통합 종합 음성 분석기
"""
    # ... 이하 기존 코드 ...
