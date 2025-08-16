"""
Unit tests for rPPG module.
"""

import os
import sys
from unittest.mock import patch

import numpy as np
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.rppg import FaceDetector, RPPGAnalyzer, SignalProcessor


class TestFaceDetector:
    """Test suite for FaceDetector class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = FaceDetector()

    def test_init(self):
        """Test initialization."""
        assert self.detector.detection_confidence == 0.7

    def test_detect_face_with_mock_frame(self):
        """Test face detection with mock frame."""
        # Create a simple test frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[150:330, 200:440] = 255  # White rectangle as "face"

        # Mock the cascade detector
        with patch.object(self.detector, 'face_cascade') as mock_cascade:
            mock_cascade.detectMultiScale.return_value = np.array([[200, 150, 240, 180]])

            result = self.detector.detect_face(frame)

            assert result is not None
            assert len(result) == 4
            assert result == (200, 150, 240, 180)

    def test_detect_face_no_detection(self):
        """Test face detection when no face is found."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        with patch.object(self.detector, 'face_cascade') as mock_cascade:
            mock_cascade.detectMultiScale.return_value = np.array([])

            result = self.detector.detect_face(frame)
            assert result is None

    def test_extract_roi_forehead(self):
        """Test ROI extraction for forehead region."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        face_box = (200, 150, 240, 180)

        roi = self.detector.extract_roi(frame, face_box, "forehead")

        assert roi is not None
        assert roi.shape[0] == 180 // 3  # Height is 1/3 of face height
        assert roi.shape[1] == 240 // 2  # Width is 1/2 of face width

    def test_extract_roi_invalid_box(self):
        """Test ROI extraction with invalid bounding box."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        face_box = (600, 400, 100, 100)  # Outside frame bounds

        roi = self.detector.extract_roi(frame, face_box, "forehead")

        # Should handle gracefully
        assert roi is None or roi.size == 0

    def test_get_face_landmarks(self):
        """Test face landmarks extraction."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        face_box = (200, 150, 240, 180)

        landmarks = self.detector.get_face_landmarks(frame, face_box)

        assert "face_area" in landmarks
        assert "face_center" in landmarks
        assert "face_width" in landmarks
        assert "face_height" in landmarks
        assert "aspect_ratio" in landmarks

        assert landmarks["face_area"] == 240 * 180
        assert landmarks["face_center"] == (200 + 240//2, 150 + 180//2)


class TestSignalProcessor:
    """Test suite for SignalProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = SignalProcessor(fps=30.0, window_size=150)

    def test_init(self):
        """Test initialization."""
        assert self.processor.fps == 30.0
        assert self.processor.window_size == 150
        assert self.processor.min_hr == 40
        assert self.processor.max_hr == 180

    def test_extract_color_signals(self):
        """Test color signal extraction."""
        # Create mock ROI frames
        roi_frames = []
        for i in range(10):
            frame = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
            roi_frames.append(frame)

        signals = self.processor.extract_color_signals(roi_frames)

        assert "red" in signals
        assert "green" in signals
        assert "blue" in signals
        assert len(signals["red"]) == 10
        assert len(signals["green"]) == 10
        assert len(signals["blue"]) == 10

    def test_extract_color_signals_empty(self):
        """Test color signal extraction with empty input."""
        signals = self.processor.extract_color_signals([])

        assert len(signals["red"]) == 0
        assert len(signals["green"]) == 0
        assert len(signals["blue"]) == 0

    def test_preprocess_signal(self):
        """Test signal preprocessing."""
        # Create a simple test signal
        signal_data = np.sin(np.linspace(0, 4*np.pi, 150)) + 1.0

        processed = self.processor.preprocess_signal(signal_data)

        assert len(processed) == len(signal_data)
        # Signal should have DC removed
        assert abs(np.mean(processed)) < abs(np.mean(signal_data))

    def test_estimate_heart_rate(self):
        """Test heart rate estimation."""
        # Create a synthetic pulse signal at 75 BPM
        duration = 5.0  # seconds
        fs = self.processor.fps
        t = np.linspace(0, duration, int(fs * duration))
        heart_rate_hz = 75 / 60.0  # Convert BPM to Hz

        pulse_signal = np.sin(2 * np.pi * heart_rate_hz * t)

        estimated_hr, confidence = self.processor.estimate_heart_rate(pulse_signal)

        # Should be close to 75 BPM
        assert 70 <= estimated_hr <= 80
        assert 0 <= confidence <= 1

    def test_estimate_heart_rate_short_signal(self):
        """Test heart rate estimation with short signal."""
        short_signal = np.random.randn(50)  # Too short

        hr, confidence = self.processor.estimate_heart_rate(short_signal)

        assert hr == 0.0
        assert confidence == 0.0

    def test_detect_artifacts(self):
        """Test artifact detection."""
        # Create a test signal with known characteristics
        signal_data = np.random.randn(150)

        artifacts = self.processor.detect_artifacts(signal_data)

        assert "motion_artifacts" in artifacts
        assert "saturation" in artifacts
        assert "noise_level" in artifacts
        assert "signal_quality" in artifacts

        assert isinstance(artifacts["motion_artifacts"], bool)
        assert isinstance(artifacts["saturation"], bool)
        assert 0 <= artifacts["noise_level"] <= 1
        assert 0 <= artifacts["signal_quality"] <= 1


class TestRPPGAnalyzer:
    """Test suite for RPPGAnalyzer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = RPPGAnalyzer(fps=30.0, window_size=30)  # Smaller window for testing

    def test_init(self):
        """Test initialization."""
        assert self.analyzer.fps == 30.0
        assert self.analyzer.window_size == 30
        assert self.analyzer.roi_type == "forehead"
        assert self.analyzer.algorithm == "green"

    def test_process_frame_no_face(self):
        """Test frame processing when no face is detected."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        with patch.object(self.analyzer.face_detector, 'detect_face', return_value=None):
            result = self.analyzer.process_frame(frame)

            assert result["face_detected"] is False
            assert result["roi_extracted"] is False
            assert result["heart_rate"] == 0.0

    def test_process_frame_with_face(self):
        """Test frame processing with face detection."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        face_box = (200, 150, 240, 180)
        roi = np.ones((60, 120, 3), dtype=np.uint8) * 128

        with patch.object(self.analyzer.face_detector, 'detect_face', return_value=face_box):
            with patch.object(self.analyzer.face_detector, 'extract_roi', return_value=roi):
                with patch.object(self.analyzer.face_detector, 'get_face_landmarks',
                                return_value={"face_area": 43200}):

                    result = self.analyzer.process_frame(frame)

                    assert result["face_detected"] is True
                    assert result["roi_extracted"] is True
                    assert "face_landmarks" in result

    def test_process_video(self):
        """Test video processing."""
        # Create mock video frames
        frames = [np.ones((480, 640, 3), dtype=np.uint8) * (100 + i*10) for i in range(5)]

        with patch.object(self.analyzer, 'process_frame') as mock_process:
            mock_process.return_value = {
                "face_detected": True,
                "roi_extracted": True,
                "heart_rate": 75.0,
                "confidence": 0.8,
                "signal_quality": 0.7,
                "artifacts": {},
                "face_landmarks": {}
            }

            result = self.analyzer.process_video(frames)

            assert "mean_heart_rate" in result
            assert "face_detection_rate" in result
            assert "total_frames" in result
            assert result["total_frames"] == 5

    def test_reset(self):
        """Test analyzer reset."""
        # Add some data to buffers
        self.analyzer.frame_buffer = [np.ones((480, 640, 3), dtype=np.uint8)]
        self.analyzer.roi_buffer = [np.ones((60, 120, 3), dtype=np.uint8)]

        self.analyzer.reset()

        assert len(self.analyzer.frame_buffer) == 0
        assert len(self.analyzer.roi_buffer) == 0

    def test_configure(self):
        """Test configuration update."""
        new_config = {
            "fps": 25.0,
            "window_size": 100,
            "roi_type": "cheek",
            "algorithm": "chrom"
        }

        self.analyzer.configure(**new_config)

        assert self.analyzer.fps == 25.0
        assert self.analyzer.window_size == 100
        assert self.analyzer.roi_type == "cheek"
        assert self.analyzer.algorithm == "chrom"


if __name__ == "__main__":
    pytest.main([__file__])
