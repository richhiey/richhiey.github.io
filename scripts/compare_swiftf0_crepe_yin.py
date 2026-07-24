#!/usr/bin/env python3
"""Conservative timing harness for SwiftF0, original CREPE, and librosa YIN.

This script measures the three package-level calls on the same mono WAV. It does
not claim benchmark accuracy metrics; labelled evaluation must align timestamps
and use the pinned pitch-benchmark metric implementation.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import librosa
import numpy as np


def version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def timed(fn, repeats: int) -> dict[str, object]:
    cold_start = time.perf_counter()
    fn()
    cold_ms = (time.perf_counter() - cold_start) * 1000
    for _ in range(3):
        fn()
    warm = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        warm.append((time.perf_counter() - start) * 1000)
    return {
        "cold_start_ms": cold_ms,
        "warm_median_ms": statistics.median(warm),
        "warm_p95_ms": float(np.percentile(warm, 95)),
        "warm_samples_ms": warm,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=10)
    args = parser.parse_args()

    try:
        import crepe
        from swift_f0 import SwiftF0
    except ImportError as exc:
        raise SystemExit(f"Install swift-f0 and crepe before running: {exc}") from exc

    audio, original_sr = librosa.load(args.audio, sr=None, mono=True)
    audio_16k = librosa.resample(audio.astype(np.float32), orig_sr=original_sr, target_sr=16000)
    swift = SwiftF0()

    def run_swift():
        return swift.detect(audio_16k, 16000)

    def run_crepe():
        return crepe.predict(audio_16k, 16000, model_capacity="full", step_size=10, center=True, viterbi=False)

    def run_yin():
        return librosa.yin(
            audio_16k,
            fmin=46.875,
            fmax=2093.75,
            sr=16000,
            frame_length=1024,
            hop_length=256,
        )

    result = {
        "audio": str(args.audio),
        "audio_seconds": len(audio_16k) / 16000,
        "original_sample_rate": original_sr,
        "comparison": {
            "swiftf0": timed(run_swift, args.repeats),
            "crepe_full": timed(run_crepe, args.repeats),
            "librosa_yin": timed(run_yin, args.repeats),
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "numpy": version("numpy"),
            "librosa": version("librosa"),
            "swift-f0": version("swift-f0"),
            "crepe": version("crepe"),
            "thread_policy": "not forced by this Python harness; record runtime configuration separately",
        },
        "notes": [
            "Timing excludes WAV decoding and the one shared resampling operation.",
            "Warm timing includes each package's own normal preprocessing and inference.",
            "This file does not calculate labelled accuracy metrics.",
            "YIN means librosa.yin, not pYIN or the authors' historical program.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
