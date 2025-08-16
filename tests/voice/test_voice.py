"""
Unit tests for voice analysis module.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.voice import VoiceAnalyzer, AudioProcessor, VoiceFeatureExtractor


class TestAudioProcessor:
    """Test suite for AudioProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = AudioProcessor(sample_rate=16000, frame_size=1024, hop_size=512)
    
    def test_init(self):
        """Test initialization."""
        assert self.processor.sample_rate == 16000
        assert self.processor.frame_size == 1024
        assert self.processor.hop_size == 512
        assert self.processor.nyquist_freq == 8000
    
    def test_load_audio(self):
        """Test audio loading and preprocessing."""
        # Create test audio data
        audio_data = np.random.randn(16000).astype(np.float64) * 0.5
        
        processed = self.processor.load_audio(audio_data)
        
        assert processed.dtype == np.float32
        assert np.max(np.abs(processed)) <= 1.0
    
    def test_load_audio_normalization(self):
        """Test audio normalization."""
        # Create audio with high amplitude
        audio_data = np.random.randn(16000) * 10.0
        
        processed = self.processor.load_audio(audio_data)
        
        # Should be normalized to [-1, 1]
        assert np.max(np.abs(processed)) <= 1.0
    
    def test_remove_silence(self):
        """Test silence removal."""
        # Create audio with silent and non-silent parts
        audio_data = np.zeros(16000)
        audio_data[5000:10000] = np.random.randn(5000) * 0.5  # Non-silent part
        
        non_silent = self.processor.remove_silence(audio_data, threshold=0.01)
        
        # Should contain some audio (might not be exact due to framing)
        assert len(non_silent) > 0
        assert len(non_silent) <= len(audio_data)
    
    def test_extract_frames(self):
        """Test frame extraction."""
        audio_data = np.random.randn(16000)
        
        frames = self.processor.extract_frames(audio_data)
        
        expected_frames = (len(audio_data) - self.processor.frame_size) // self.processor.hop_size + 1
        assert frames.shape[0] >= expected_frames - 1  # Allow for small variations
        assert frames.shape[1] == self.processor.frame_size
    
    def test_compute_spectrum(self):
        """Test spectrum computation."""
        # Create a sine wave
        freq = 440  # A4 note
        duration = 1.0
        t = np.linspace(0, duration, int(self.processor.sample_rate * duration))
        frame = np.sin(2 * np.pi * freq * t[:self.processor.frame_size])
        
        freqs, magnitudes = self.processor.compute_spectrum(frame)
        
        # Find peak frequency
        peak_idx = np.argmax(magnitudes)
        peak_freq = freqs[peak_idx]
        
        # Should be close to 440 Hz
        assert abs(peak_freq - freq) < 50  # Allow some tolerance
    
    def test_apply_bandpass_filter(self):
        """Test bandpass filtering."""
        audio_data = np.random.randn(16000)
        
        filtered = self.processor.apply_bandpass_filter(audio_data, 300, 3400)
        
        assert len(filtered) == len(audio_data)
        # Basic sanity check - filtered signal should exist
        assert not np.all(filtered == 0)
    
    def test_detect_voice_activity(self):
        """Test voice activity detection."""
        # Create audio with varying energy
        audio_data = np.concatenate([
            np.random.randn(8000) * 0.01,  # Low energy (silence)
            np.random.randn(8000) * 0.5    # High energy (voice)
        ])
        
        vad = self.processor.detect_voice_activity(audio_data)
        
        assert len(vad) > 0
        assert all(isinstance(v, (bool, np.bool_)) for v in vad)


class TestVoiceFeatureExtractor:
    """Test suite for VoiceFeatureExtractor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = VoiceFeatureExtractor(sample_rate=16000)
    
    def test_init(self):
        """Test initialization."""
        assert self.extractor.sample_rate == 16000
        assert self.extractor.n_mels == 13
    
    def test_extract_fundamental_frequency(self):
        """Test F0 extraction."""
        # Create a synthetic periodic signal
        freq = 200  # Hz
        duration = 0.1  # seconds
        t = np.linspace(0, duration, int(self.extractor.sample_rate * duration))
        frame = np.sin(2 * np.pi * freq * t)
        
        f0_features = self.extractor.extract_fundamental_frequency(frame)
        
        assert "f0_mean" in f0_features
        assert "f0_std" in f0_features
        assert "jitter" in f0_features
        
        # F0 should be close to the input frequency
        assert 150 <= f0_features["f0_mean"] <= 250  # Allow some tolerance
    
    def test_extract_spectral_features(self):
        """Test spectral feature extraction."""
        # Create a test frame
        frame = np.random.randn(1024)
        
        features = self.extractor.extract_spectral_features(frame)
        
        assert "spectral_centroid" in features
        assert "spectral_bandwidth" in features
        assert "spectral_rolloff" in features
        assert "zero_crossing_rate" in features
        
        # Basic sanity checks
        assert features["spectral_centroid"] >= 0
        assert features["spectral_bandwidth"] >= 0
        assert features["spectral_rolloff"] >= 0
        assert 0 <= features["zero_crossing_rate"] <= 1
    
    def test_extract_mfcc(self):
        """Test MFCC extraction."""
        frame = np.random.randn(1024)
        
        mfcc = self.extractor.extract_mfcc(frame)
        
        assert len(mfcc) == self.extractor.n_mels
        assert not np.all(mfcc == 0)
    
    def test_extract_prosodic_features(self):
        """Test prosodic feature extraction."""
        # Create multiple frames with varying energy
        frames = []
        for i in range(10):
            frame = np.random.randn(1024) * (0.1 + i * 0.1)
            frames.append(frame)
        
        features = self.extractor.extract_prosodic_features(frames)
        
        assert "energy_mean" in features
        assert "energy_std" in features
        assert "energy_range" in features
        assert "energy_skewness" in features
        assert "energy_kurtosis" in features
        
        # Energy should vary across frames
        assert features["energy_std"] > 0
    
    def test_extract_voice_quality_features(self):
        """Test voice quality feature extraction."""
        frame = np.random.randn(1024)
        
        features = self.extractor.extract_voice_quality_features(frame)
        
        assert "hnr" in features
        assert "shimmer" in features
        assert "spectral_tilt" in features
        
        # HNR should be a reasonable value
        assert -50 <= features["hnr"] <= 50
    
    def test_extract_all_features(self):
        """Test comprehensive feature extraction."""
        frames = [np.random.randn(1024) for _ in range(5)]
        
        all_features = self.extractor.extract_all_features(frames)
        
        # Should contain various feature types
        assert len(all_features) > 10
        
        # Check for expected feature categories
        feature_keys = list(all_features.keys())
        assert any("f0" in key for key in feature_keys)
        assert any("spectral" in key for key in feature_keys)
        assert any("energy" in key for key in feature_keys)
        assert "mfcc_mean" in all_features
        assert "mfcc_std" in all_features


class TestVoiceAnalyzer:
    """Test suite for VoiceAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = VoiceAnalyzer(
            sample_rate=16000, 
            frame_size=1024, 
            hop_size=512, 
            analysis_window=2.0  # Shorter window for testing
        )
    
    def test_init(self):
        """Test initialization."""
        assert self.analyzer.sample_rate == 16000
        assert self.analyzer.frame_size == 1024
        assert self.analyzer.hop_size == 512
        assert self.analyzer.analysis_window == 2.0
        assert self.analyzer.window_samples == 32000
    
    def test_process_audio_chunk_insufficient_data(self):
        """Test processing with insufficient data."""
        small_chunk = np.random.randn(1000)
        
        result = self.analyzer.process_audio_chunk(small_chunk)
        
        assert "voice_detected" in result
        assert "audio_quality" in result
        # Should not have full analysis with insufficient data
    
    def test_process_audio_chunk_sufficient_data(self):
        """Test processing with sufficient data."""
        # Process multiple chunks to build up buffer
        for i in range(5):
            chunk = np.random.randn(8000) * 0.5  # Moderate amplitude
            result = self.analyzer.process_audio_chunk(chunk)
        
        # Final result should have analysis
        assert "voice_detected" in result
        assert "audio_quality" in result
        assert "features" in result
        assert "health_indicators" in result
    
    def test_process_complete_audio(self):
        """Test complete audio processing."""
        # Create 5 seconds of audio
        duration = 5.0
        audio_data = np.random.randn(int(self.analyzer.sample_rate * duration)) * 0.3
        
        result = self.analyzer.process_complete_audio(audio_data)
        
        assert "voice_detected" in result
        assert "mean_audio_quality" in result
        assert "aggregated_features" in result
        assert "health_profile" in result
        assert "temporal_analysis" in result
        
        if result["voice_detected"]:
            assert result["temporal_analysis"]["analysis_windows"] > 0
    
    def test_assess_audio_quality(self):
        """Test audio quality assessment."""
        # Create frames with good quality characteristics
        frames = [np.random.randn(1024) * 0.3 for _ in range(5)]
        
        quality = self.analyzer._assess_audio_quality(frames)
        
        assert 0 <= quality <= 1
    
    def test_extract_health_indicators(self):
        """Test health indicator extraction."""
        # Create mock features
        features = {
            "f0_mean_mean": 150.0,
            "f0_mean_std": 10.0,
            "hnr_mean": 15.0,
            "spectral_rolloff_mean": 2000.0,
            "f1_mean": 500.0,
            "f2_mean": 1500.0,
            "energy_mean": 0.5,
            "energy_std": 0.1
        }
        
        indicators = self.analyzer._extract_health_indicators(features)
        
        assert "vocal_stability" in indicators
        assert "voice_quality" in indicators
        assert "respiratory_health" in indicators
        assert "articulation_clarity" in indicators
        assert "overall_vocal_health" in indicators
        assert "stress_indicator" in indicators
        
        # All indicators should be in valid range
        for value in indicators.values():
            assert 0 <= value <= 1
    
    def test_reset(self):
        """Test analyzer reset."""
        # Add some data to buffer
        self.analyzer.audio_buffer = np.random.randn(1000)
        
        self.analyzer.reset()
        
        assert len(self.analyzer.audio_buffer) == 0
        assert len(self.analyzer.analysis_results) == 0
    
    def test_configure(self):
        """Test configuration update."""
        new_config = {
            "sample_rate": 22050,
            "frame_size": 2048,
            "hop_size": 1024,
            "analysis_window": 3.0
        }
        
        self.analyzer.configure(**new_config)
        
        assert self.analyzer.sample_rate == 22050
        assert self.analyzer.frame_size == 2048
        assert self.analyzer.hop_size == 1024
        assert self.analyzer.analysis_window == 3.0


if __name__ == "__main__":
    pytest.main([__file__])