# SwiftF0 architecture evidence ledger

Retrieved 2026-07-24. This ledger distinguishes source-backed facts from interpretation and unrun experiments.

| Claim | Evidence type | Source | Commit/file/line | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| SwiftF0 accepts 16 kHz audio and documents 1024-sample frames and 256-sample hops | Repository-documented behavior | `lars76/swift-f0` | `64700fc`, `swift_f0/core.py:24-40` | High | The paper is the conceptual primary source; package source supplies the implementation detail. |
| SwiftF0 model range is 46.875–2093.75 Hz and default confidence threshold is 0.9 | Repository-documented behavior | `lars76/swift-f0` | `64700fc`, `swift_f0/core.py:47-53` | High | Package defaults, not PitchSteps policy. |
| SwiftF0 uses 132 selected STFT bins, five 5×5 2-D convolutional layers, 200 logarithmic pitch bins, and 95,842 parameters | Paper-described architecture | SwiftF0 paper | arXiv `2508.18440v1`, §§3.2–3.3 | High | The paper reports approximately 33.1 cents per output bin before continuous decoding. |
| SwiftF0 combines classification and log-frequency L1 loss, then decodes a local ±9-bin expected value | Paper-described method | SwiftF0 paper | arXiv `2508.18440v1`, §§3.4–3.5 | High | Local probability mass is used as confidence. |
| PitchSteps loads local ONNX with ONNX Runtime Web WASM, one thread | PitchSteps-specific behavior | `richhiey/pitchsteps` | `ac0279b`, `src/pitch/detectors/SwiftF0Detector.ts:1-45` | High | `onnxruntime-web/wasm`; execution provider is `wasm`. |
| PitchSteps averages channels to mono and batches 2048 samples in an AudioWorklet | PitchSteps-specific behavior | `richhiey/pitchsteps` | `ac0279b`, `src/audio-worklet/microphone-processor.js:8-49` | High | AudioWorklet posts transferable Float32Array buffers. |
| PitchSteps linearly resamples to 16 kHz and uses 4096-sample windows, advancing 2048 samples | PitchSteps-specific behavior | `richhiey/pitchsteps` | `ac0279b`, `src/workers/pitch.worker.ts:78-116` | High | Timestamp decoding uses the 256-sample SwiftF0 hop. |
| PitchSteps uses 80–1000 Hz and confidence threshold 0.72 by default | PitchSteps-specific behavior | `richhiey/pitchsteps` | `ac0279b`, `src/workers/workerProtocol.ts:16-28` | High | These are app configuration values. |
| PitchSteps applies level, clipping, range, confidence, continuity, and median filtering | PitchSteps-specific behavior | `richhiey/pitchsteps` | `ac0279b`, `src/workers/pitch.worker.ts:118-148`; `src/pitch/voicing/VoicingEstimator.ts`; `src/pitch/smoothing/*` | High | UI stability is not equivalent to detector accuracy. |
| CREPE uses raw waveform input, 360 bins, and 10 ms default output cadence | Repository-documented behavior | `marl/crepe` | `c9b71ce`, `crepe/core.py:58-71,156-212,258-270` | High | Original package reference implementation. |
| SwiftF0 paper reports ~132.6 ms / 5 s and ~42.42× CPU speed-up | Paper-reported result | SwiftF0 paper | arXiv `2508.18440`, paper benchmark section | Medium | Not independently reproduced here; benchmark context must accompany the numbers. |
| SwiftF0 ONNX returns aligned `pitch_hz` and `confidence` arrays | Repository-documented behavior | `lars76/swift-f0` | `64700fc`, `swift_f0/core.py:131-169` | High | Voicing and timestamps are computed by the Python wrapper. |
| Package timestamps use `(frame × 256 + 127.5) / 16000` | Repository-documented behavior | `lars76/swift-f0` | `64700fc`, `swift_f0/core.py:185-203` | High | Offset accounts for symmetric STFT padding. |
| Default voiced output uses confidence, lower-frequency, and upper-frequency tests | Repository-documented behavior | `lars76/swift-f0` | `64700fc`, `swift_f0/core.py:171-184` | High | Wrapper policy; confidence is not claimed to be calibrated. |
| This post contains no locally reproduced accuracy or runtime result | Local experiment status | This portfolio repository | Article text | High | Paper-reported values remain explicitly labelled. |
