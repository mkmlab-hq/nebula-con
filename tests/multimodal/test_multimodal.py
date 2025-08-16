"""
Unit tests for multimodal health platform.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.multimodal import (
    MultimodalHealthAnalyzer, 
    ModalityFusionEngine, 
    HealthProfileGenerator,
    ModalityWeight
)
from src.multimodal.health_profiler import HealthProfile


class TestModalityWeight:
    """Test suite for ModalityWeight dataclass."""
    
    def test_default_weights(self):
        """Test default weight values."""
        weights = ModalityWeight()
        
        assert weights.rppg == 0.4
        assert weights.voice == 0.3
        assert weights.mkm12 == 0.3
    
    def test_custom_weights(self):
        """Test custom weight values."""
        weights = ModalityWeight(rppg=0.5, voice=0.25, mkm12=0.25)
        
        assert weights.rppg == 0.5
        assert weights.voice == 0.25
        assert weights.mkm12 == 0.25


class TestModalityFusionEngine:
    """Test suite for ModalityFusionEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fusion_engine = ModalityFusionEngine(
            fusion_strategy="weighted_average",
            modality_weights=ModalityWeight(rppg=0.4, voice=0.3, mkm12=0.3)
        )
    
    def test_init(self):
        """Test initialization."""
        assert self.fusion_engine.fusion_strategy == "weighted_average"
        assert self.fusion_engine.modality_weights.rppg == 0.4
        assert self.fusion_engine.modality_weights.voice == 0.3
        assert self.fusion_engine.modality_weights.mkm12 == 0.3
    
    def test_get_available_modalities_all_reliable(self):
        """Test getting available modalities when all are reliable."""
        modality_results = {
            "rppg": {"confidence": 0.8, "heart_rate": 75.0},
            "voice": {"mean_audio_quality": 0.7, "voice_detected": True},
            "mkm12": {"prediction_confidence": 0.9, "health_score": 0.8}
        }
        
        available = self.fusion_engine._get_available_modalities(modality_results)
        
        assert len(available) == 3
        assert "rppg" in available
        assert "voice" in available
        assert "mkm12" in available
    
    def test_get_available_modalities_some_unreliable(self):
        """Test getting available modalities when some are unreliable."""
        modality_results = {
            "rppg": {"confidence": 0.8, "heart_rate": 75.0},
            "voice": {"mean_audio_quality": 0.2, "voice_detected": True},  # Low quality
            "mkm12": {"prediction_confidence": 0.9, "health_score": 0.8}
        }
        
        available = self.fusion_engine._get_available_modalities(modality_results)
        
        assert len(available) == 2
        assert "rppg" in available
        assert "mkm12" in available
        assert "voice" not in available
    
    def test_weighted_average_fusion(self):
        """Test weighted average fusion."""
        modality_results = {
            "rppg": {"confidence": 0.8, "heart_rate": 80.0, "signal_quality": 0.7},
            "voice": {"mean_audio_quality": 0.6, "health_indicators": {"overall_vocal_health": 0.8}},
            "mkm12": {"prediction_confidence": 0.9, "health_score": 0.9}
        }
        
        result = self.fusion_engine.fuse_health_metrics(modality_results)
        
        assert "overall_health_score" in result
        assert "confidence" in result
        assert "modality_contributions" in result
        assert "health_indicators" in result
        assert result["fusion_method"] == "weighted_average"
        assert len(result["available_modalities"]) == 3
        
        # Overall score should be reasonable
        assert 0 <= result["overall_health_score"] <= 1
        assert 0 <= result["confidence"] <= 1
    
    def test_adaptive_fusion(self):
        """Test adaptive fusion."""
        self.fusion_engine.fusion_strategy = "adaptive"
        
        modality_results = {
            "rppg": {"confidence": 0.9, "heart_rate": 75.0, "signal_quality": 0.8},
            "voice": {"mean_audio_quality": 0.5, "health_indicators": {"overall_vocal_health": 0.7}},
            "mkm12": {"prediction_confidence": 0.7, "health_score": 0.8}
        }
        
        result = self.fusion_engine.fuse_health_metrics(modality_results)
        
        assert result["fusion_method"] == "adaptive"
        assert "adaptive_weights" in result
        
        # Higher confidence modalities should have higher weights
        weights = result["adaptive_weights"]
        assert weights["rppg"] > weights["mkm12"]  # rPPG has higher confidence
    
    def test_fuse_health_metrics_no_reliable_modalities(self):
        """Test fusion when no modalities are reliable."""
        modality_results = {
            "rppg": {"confidence": 0.1, "heart_rate": 0.0},
            "voice": {"mean_audio_quality": 0.2, "voice_detected": False},
            "mkm12": {"prediction_confidence": 0.3, "health_score": 0.0}
        }
        
        result = self.fusion_engine.fuse_health_metrics(modality_results)
        
        assert result["overall_health_score"] == 0.0
        assert result["confidence"] == 0.0
        assert len(result["available_modalities"]) == 0
        assert "error" in result
    
    def test_extract_health_score_rppg(self):
        """Test health score extraction from rPPG."""
        rppg_results = {"heart_rate": 75.0, "signal_quality": 0.8}
        
        score = self.fusion_engine._extract_health_score("rppg", rppg_results)
        
        assert 0 <= score <= 1
        # Should be high for normal heart rate
        assert score > 0.5
    
    def test_extract_health_score_voice(self):
        """Test health score extraction from voice."""
        voice_results = {"health_indicators": {"overall_vocal_health": 0.85}}
        
        score = self.fusion_engine._extract_health_score("voice", voice_results)
        
        assert score == 0.85
    
    def test_extract_health_score_mkm12(self):
        """Test health score extraction from MKM12."""
        mkm12_results = {"health_score": 0.9}
        
        score = self.fusion_engine._extract_health_score("mkm12", mkm12_results)
        
        assert score == 0.9
    
    def test_update_weights(self):
        """Test updating modality weights."""
        new_weights = ModalityWeight(rppg=0.5, voice=0.2, mkm12=0.3)
        
        self.fusion_engine.update_weights(new_weights)
        
        assert self.fusion_engine.modality_weights.rppg == 0.5
        assert self.fusion_engine.modality_weights.voice == 0.2
        assert self.fusion_engine.modality_weights.mkm12 == 0.3
    
    def test_get_modality_reliability(self):
        """Test modality reliability calculation."""
        modality_results = {
            "rppg": {"confidence": 0.6},
            "voice": {"mean_audio_quality": 0.8},
            "mkm12": {"prediction_confidence": 0.9}
        }
        
        reliability = self.fusion_engine.get_modality_reliability(modality_results)
        
        assert "rppg" in reliability
        assert "voice" in reliability
        assert "mkm12" in reliability
        
        # All should be positive values
        for value in reliability.values():
            assert value >= 0


class TestHealthProfileGenerator:
    """Test suite for HealthProfileGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.profiler = HealthProfileGenerator()
    
    def test_init(self):
        """Test initialization."""
        assert len(self.profiler.behavior_regimes) == 8
        assert len(self.profiler.adaptation_labels) == 8
        assert sum(self.profiler.health_weights.values()) == 1.0
    
    def test_normalize_heart_rate(self):
        """Test heart rate normalization."""
        # Test optimal range
        assert self.profiler._normalize_heart_rate(75.0) == 1.0
        assert self.profiler._normalize_heart_rate(85.0) == 1.0
        
        # Test sub-optimal values
        assert self.profiler._normalize_heart_rate(50.0) < 1.0
        assert self.profiler._normalize_heart_rate(120.0) < 1.0
        
        # Test edge cases
        assert self.profiler._normalize_heart_rate(0.0) == 0.0
        assert self.profiler._normalize_heart_rate(-10.0) == 0.0
    
    def test_extract_health_scores(self):
        """Test health score extraction from multimodal data."""
        multimodal_data = {
            "health_indicators": {
                "cardiovascular_health": {
                    "heart_rate": 75.0,
                    "heart_rate_variability": 0.8,
                    "pulse_quality": 0.7
                },
                "respiratory_health": {
                    "vocal_stability": 0.9,
                    "respiratory_support": 0.8
                },
                "mental_health": {
                    "stress_level": 0.3,
                    "emotional_stability": 0.8
                }
            },
            "modality_contributions": {
                "voice": 0.7
            }
        }
        
        health_scores = self.profiler._extract_health_scores(multimodal_data)
        
        assert "cardiovascular" in health_scores
        assert "respiratory" in health_scores
        assert "mental" in health_scores
        assert "vocal" in health_scores
        
        # All scores should be in valid range
        for score in health_scores.values():
            assert 0 <= score <= 1
    
    def test_calculate_overall_health_score(self):
        """Test overall health score calculation."""
        health_scores = {
            "cardiovascular": 0.8,
            "respiratory": 0.7,
            "mental": 0.9,
            "vocal": 0.8
        }
        
        mkm12_predictions = {
            "health_risk": 0.2,
            "adaptation": [0.8, 0.7, 0.9, 0.6, 0.8, 0.7, 0.8, 0.9]
        }
        
        overall_score = self.profiler._calculate_overall_health_score(health_scores, mkm12_predictions)
        
        assert 0 <= overall_score <= 1
        assert overall_score > 0.5  # Should be good with these scores
    
    def test_determine_behavior_regime(self):
        """Test behavior regime determination."""
        mkm12_predictions = {
            "behavior_regime": [0.1, 0.6, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05]
        }
        
        regime = self.profiler._determine_behavior_regime(mkm12_predictions)
        
        assert regime == "High Energy Performer"  # Index 1 has highest probability
    
    def test_calculate_adaptation_capacity(self):
        """Test adaptation capacity calculation."""
        mkm12_predictions = {
            "adaptation": [0.8, 0.7, 0.9, 0.6, 0.8, 0.7, 0.8, 0.9]
        }
        
        capacity = self.profiler._calculate_adaptation_capacity(mkm12_predictions)
        
        expected = np.mean([0.8, 0.7, 0.9, 0.6, 0.8, 0.7, 0.8, 0.9])
        assert abs(capacity - expected) < 0.01
    
    def test_identify_risk_factors(self):
        """Test risk factor identification."""
        health_scores = {
            "cardiovascular": 0.9,
            "respiratory": 0.2,  # Low score
            "mental": 0.5,      # Medium score
            "vocal": 0.8
        }
        
        mkm12_predictions = {
            "health_risk": 0.8,  # High risk
            "adaptation": [0.1, 0.2, 0.8, 0.9, 0.1, 0.8, 0.9, 0.8]  # Some low adaptation
        }
        
        risk_factors = self.profiler._identify_risk_factors(health_scores, mkm12_predictions)
        
        assert len(risk_factors) > 0
        assert any("respiratory" in rf for rf in risk_factors)
        assert any("High overall health risk" in rf for rf in risk_factors)
    
    def test_generate_recommendations(self):
        """Test recommendation generation."""
        health_scores = {
            "cardiovascular": 0.4,  # Low
            "mental": 0.3           # Low
        }
        behavior_regime = "High Energy Performer"
        risk_factors = ["Low cardiovascular health", "High overall health risk"]
        
        recommendations = self.profiler._generate_recommendations(
            health_scores, behavior_regime, risk_factors
        )
        
        assert len(recommendations) > 0
        assert any("cardiovascular" in rec for rec in recommendations)
        assert any("stress" in rec for rec in recommendations)
    
    def test_generate_profile(self):
        """Test complete profile generation."""
        multimodal_data = {
            "overall_health_score": 0.8,
            "confidence": 0.7,
            "health_indicators": {
                "cardiovascular_health": {
                    "heart_rate": 75.0,
                    "heart_rate_variability": 0.8,
                    "pulse_quality": 0.7
                }
            },
            "available_modalities": ["rppg", "voice"]
        }
        
        profile = self.profiler.generate_profile(multimodal_data)
        
        assert isinstance(profile, HealthProfile)
        assert 0 <= profile.overall_score <= 1
        assert 0 <= profile.confidence <= 1
        assert profile.behavior_regime in self.profiler.behavior_regimes
        assert isinstance(profile.risk_factors, list)
        assert isinstance(profile.recommendations, list)


class TestMultimodalHealthAnalyzer:
    """Test suite for MultimodalHealthAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Use minimal config for testing
        config = {
            "rppg_window_size": 30,
            "voice_analysis_window": 2.0,
            "min_analysis_duration": 1.0
        }
        self.analyzer = MultimodalHealthAnalyzer(config)
    
    def test_init(self):
        """Test initialization."""
        assert self.analyzer.rppg_analyzer is not None
        assert self.analyzer.voice_analyzer is not None
        assert self.analyzer.fusion_engine is not None
        assert self.analyzer.health_profiler is not None
    
    def test_start_session(self):
        """Test session start."""
        session_id = "test_session_123"
        
        result = self.analyzer.start_session(session_id)
        
        assert result["session_id"] == session_id
        assert result["status"] == "started"
        assert "timestamp" in result
        
        # Check state is updated
        assert self.analyzer.analysis_state["session_id"] == session_id
        assert self.analyzer.analysis_state["start_time"] is not None
    
    def test_process_video_frame_no_session(self):
        """Test video frame processing without session."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        result = self.analyzer.process_video_frame(frame)
        
        assert "error" in result
    
    def test_process_video_frame_with_session(self):
        """Test video frame processing with active session."""
        self.analyzer.start_session("test_session")
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        
        with patch.object(self.analyzer.rppg_analyzer, 'process_frame') as mock_process:
            mock_process.return_value = {
                "face_detected": True,
                "heart_rate": 75.0,
                "confidence": 0.8
            }
            
            result = self.analyzer.process_video_frame(frame)
            
            assert result["session_id"] == "test_session"
            assert result["frame_number"] == 1
            assert "rppg_result" in result
            assert "timestamp" in result
    
    def test_process_multimodal_data(self):
        """Test complete multimodal data processing."""
        # Create mock data
        video_frames = [np.ones((240, 320, 3), dtype=np.uint8) * 128 for _ in range(10)]
        audio_data = np.random.randn(16000) * 0.3  # 1 second of audio
        additional_data = {
            "demographic_data": {"age": 30},
            "persona_data": {"persona_type": "balanced"}
        }
        
        with patch.object(self.analyzer.rppg_analyzer, 'process_video') as mock_rppg:
            with patch.object(self.analyzer.voice_analyzer, 'process_complete_audio') as mock_voice:
                mock_rppg.return_value = {
                    "mean_heart_rate": 75.0,
                    "mean_confidence": 0.8,
                    "face_detection_rate": 1.0
                }
                mock_voice.return_value = {
                    "voice_detected": True,
                    "mean_audio_quality": 0.7,
                    "health_profile": {"overall_vocal_health": 0.8}
                }
                
                result = self.analyzer.process_multimodal_data(
                    video_frames=video_frames,
                    audio_data=audio_data,
                    additional_data=additional_data
                )
                
                assert "modality_results" in result
                assert "fused_results" in result
                assert "health_profile" in result
                assert "analysis_metadata" in result
                assert "processing_time" in result
    
    def test_get_real_time_update_no_session(self):
        """Test real-time update without session."""
        result = self.analyzer.get_real_time_update()
        
        assert "error" in result
    
    def test_get_real_time_update_collecting_data(self):
        """Test real-time update during data collection phase."""
        self.analyzer.start_session("test_session")
        
        result = self.analyzer.get_real_time_update()
        
        assert result["status"] == "collecting_data"
        assert "session_duration" in result
        assert "required_duration" in result
    
    def test_end_session(self):
        """Test session end."""
        self.analyzer.start_session("test_session")
        
        result = self.analyzer.end_session()
        
        assert result["status"] == "session_ended"
        assert "session_summary" in result
        assert self.analyzer.analysis_state["session_id"] is None
    
    def test_configure(self):
        """Test configuration update."""
        new_config = {
            "rppg_fps": 25.0,
            "voice_sample_rate": 22050,
            "weight_rppg": 0.5
        }
        
        self.analyzer.configure(new_config)
        
        assert self.analyzer.config["rppg_fps"] == 25.0
        assert self.analyzer.config["voice_sample_rate"] == 22050
        assert self.analyzer.config["weight_rppg"] == 0.5
    
    def test_get_system_status(self):
        """Test system status retrieval."""
        status = self.analyzer.get_system_status()
        
        assert status["system_ready"] is True
        assert "components" in status
        assert "current_session" in status
        assert "config" in status
        assert "version" in status


if __name__ == "__main__":
    pytest.main([__file__])