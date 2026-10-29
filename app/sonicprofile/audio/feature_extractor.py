"""Lightweight real-time acoustic feature extraction for SonicProfile.

Input: mono float audio at the configured sample rate.
Output: latest frame's RMS, spectral centroid, rolloff and 24 Bark-band energies.
This is signal analysis only; it does not identify a song or predict a genre.
"""
from __future__ import annotations

import numpy as np


def hz_to_bark(freq_hz: np.ndarray) -> np.ndarray:
    """Traunmüller-style approximate conversion from Hz to Bark."""
    f = np.asarray(freq_hz, dtype=np.float64)
    return 13.0 * np.arctan(0.00076 * f) + 3.5 * np.arctan((f / 7500.0) ** 2)


class RealtimeFeatureExtractor:
    def __init__(
        self,
        sample_rate: int = 44100,
        frame_ms: float = 25.0,
        hop_ms: float = 10.0,
        num_bands: int = 24,
    ):
        self.sample_rate = int(sample_rate)
        self.frame_size = max(2, round(self.sample_rate * frame_ms / 1000.0))
        self.hop_size = max(1, round(self.sample_rate * hop_ms / 1000.0))
        self.num_bands = int(num_bands)
        self._buffer = np.empty(0, dtype=np.float32)
        self._window = np.hanning(self.frame_size).astype(np.float64)
        self._freqs = np.fft.rfftfreq(self.frame_size, d=1.0 / self.sample_rate)
        self._bark = hz_to_bark(self._freqs)
        self._band_edges = np.linspace(0.0, float(hz_to_bark(np.array([self.sample_rate / 2]))[0]), self.num_bands + 1)
        self._last = self._empty_result()

    def _empty_result(self):
        return {
            "rms": 0.0,
            "centroid_hz": 0.0,
            "rolloff_hz": 0.0,
            "bark_bands": [0.0] * self.num_bands,
        }

    def process(self, mono_samples: np.ndarray) -> dict:
        """Consume one audio block and return the most recent complete frame's features."""
        samples = np.asarray(mono_samples, dtype=np.float32).reshape(-1)
        if samples.size == 0:
            return self._last
        self._buffer = np.concatenate((self._buffer, samples))
        latest = None
        while self._buffer.size >= self.frame_size:
            frame = self._buffer[:self.frame_size].astype(np.float64, copy=False)
            self._buffer = self._buffer[self.hop_size:]
            latest = self._analyze_frame(frame)
        if latest is not None:
            self._last = latest
        return self._last

    def _analyze_frame(self, frame: np.ndarray) -> dict:
        centered = frame - np.mean(frame)
        rms = float(np.sqrt(np.mean(centered * centered)))
        windowed = centered * self._window
        magnitude = np.abs(np.fft.rfft(windowed))
        power = magnitude * magnitude
        total_power = float(np.sum(power))
        magnitude_sum = float(np.sum(magnitude))

        if magnitude_sum > 1e-12:
            centroid = float(np.sum(self._freqs * magnitude) / magnitude_sum)
        else:
            centroid = 0.0

        if total_power > 1e-12:
            cumulative = np.cumsum(power)
            index = int(np.searchsorted(cumulative, 0.85 * total_power))
            rolloff = float(self._freqs[min(index, len(self._freqs) - 1)])
        else:
            rolloff = 0.0

        bark_energy = np.zeros(self.num_bands, dtype=np.float64)
        for i in range(self.num_bands):
            if i == self.num_bands - 1:
                mask = (self._bark >= self._band_edges[i]) & (self._bark <= self._band_edges[i + 1])
            else:
                mask = (self._bark >= self._band_edges[i]) & (self._bark < self._band_edges[i + 1])
            if np.any(mask):
                bark_energy[i] = np.sqrt(np.mean(power[mask])) if np.any(power[mask]) else 0.0

        max_energy = float(np.max(bark_energy)) if bark_energy.size else 0.0
        normalized = bark_energy / max_energy if max_energy > 1e-12 else bark_energy
        return {
            "rms": rms,
            "centroid_hz": centroid,
            "rolloff_hz": rolloff,
            "bark_bands": np.clip(normalized, 0.0, 1.0).astype(float).tolist(),
        }
