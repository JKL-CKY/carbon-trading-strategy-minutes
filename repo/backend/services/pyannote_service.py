import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class PyannoteService:
    def __init__(self):
        self.auth_token = os.getenv("PYANNOTE_AUTH_TOKEN", "")
        self._pipeline = None
        logger.info("PyannoteService initialized")

    def _load_pipeline(self):
        if self._pipeline is None:
            try:
                from pyannote.audio import Pipeline
                self._pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=self.auth_token
                )
                logger.info("Pyannote pipeline loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load Pyannote pipeline: {e}. Using mock mode.")
                self._pipeline = None
        return self._pipeline

    def diarize(self, audio_path: str) -> List[Dict[str, Any]]:
        pipeline = self._load_pipeline()

        if pipeline is None:
            return self._mock_diarize(audio_path)

        diarization = pipeline(audio_path)

        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })

        return speaker_segments

    def _mock_diarize(self, audio_path: str) -> List[Dict[str, Any]]:
        mock_segments = [
            {"start": 0.0, "end": 15.5, "speaker": "SPEAKER_00"},
            {"start": 15.5, "end": 32.0, "speaker": "SPEAKER_01"},
            {"start": 32.0, "end": 48.5, "speaker": "SPEAKER_02"},
            {"start": 48.5, "end": 65.0, "speaker": "SPEAKER_00"},
            {"start": 65.0, "end": 82.0, "speaker": "SPEAKER_01"},
            {"start": 82.0, "end": 98.0, "speaker": "SPEAKER_02"},
            {"start": 98.0, "end": 115.0, "speaker": "SPEAKER_00"},
        ]

        return mock_segments
