---
layout: post
title: "SwiftF0 vs. CREPE vs. YIN: A Scientific Comparison of Monophonic Pitch Detectors"
description: "A source-grounded comparison of SwiftF0, CREPE, and YIN: representations, accuracy metrics, runtime methodology, failure modes, and a browser integration case study."
date: 2026-07-24 09:00:00 +0200
research_post: true
---

SwiftF0, CREPE, and YIN solve the same deceptively difficult problem with three different engineering philosophies. SwiftF0 gives a compact neural network a frequency-domain representation. CREPE learns directly from waveform excerpts with a substantially larger convolutional model. YIN uses no training data at all: it searches for periodicity with a normalized difference function. This article compares what each method computes, what its output means, how to evaluate it fairly, and where each is likely to fail. PitchSteps appears at the end as a concrete browser integration case study rather than as the subject of the comparison.

The scientific boundary is important. Results attributed to a paper are paper-reported results. Facts about an implementation come from pinned source revisions. No new accuracy result is claimed here because a controlled labelled-dataset experiment was not completed for this publication.

## The problem: estimate F0, not the loudest peak

For a periodic voiced sound, the fundamental frequency is the repetition rate of the underlying excitation. A note at 220 Hz has a fundamental near 220 Hz and harmonics near 440, 660, 880 Hz, and so on. The strongest spectral peak is not necessarily the fundamental: the vocal tract, instrument resonances, microphone, and room can amplify a harmonic while leaving the true F0 comparatively weak. A robust detector therefore uses evidence across time and across harmonics.

“Monophonic” means that the algorithm assumes one dominant pitch at a time. It is a useful assumption for a vocal warm-up, but it is not a promise that the system will separate simultaneous voices, chords, or a vocal line over loud accompaniment.

Pitch is logarithmic. Relative error is usually expressed in cents:

<div class="research-equation" role="math" aria-label="Cents error equals 1200 times log base 2 of predicted frequency divided by true frequency">
  <var>e</var><sub>cents</sub> = 1200 log<sub>2</sub>
  <span class="research-equation__fraction"><span><var>f</var><sub>pred</sub></span><span><var>f</var><sub>true</sub></span></span>
</div>

Here, <var>f</var><sub>pred</sub> and <var>f</var><sub>true</sub> are predicted and reference frequencies in hertz. One semitone is 100 cents; an octave is 1,200 cents. For display, PitchSteps uses the standard equal-tempered conversion:

<div class="research-equation" role="math" aria-label="MIDI note equals 69 plus 12 times log base 2 of frequency divided by 440">
  MIDI = 69 + 12 log<sub>2</sub>
  <span class="research-equation__fraction"><span><var>f</var></span><span>440</span></span>
</div>

where <var>f</var> is frequency in hertz and 440 Hz is A4. The nearest integer MIDI value becomes the note name; the fractional difference is shown as cents.

## Three approaches to the same signal

<figure class="research-figure">
  <img src="/assets/images/swiftf0-comparison/architectures.svg" alt="Three pitch-estimation architectures: SwiftF0, CREPE, and YIN">
  <figcaption><strong>Figure 1.</strong> Original schematic of the three detector families. SwiftF0 and CREPE learn pitch representations from data; YIN derives a periodicity estimate directly from the signal. The outputs are comparable only after timestamp alignment and an explicit voicing policy.</figcaption>
</figure>

| Property | SwiftF0 | CREPE | YIN |
| --- | --- | --- | --- |
| Core representation | STFT-derived, selected spectral region | Raw 1,024-sample waveform | Time-domain difference function |
| Learned model | Compact 2-D CNN | Six-layer CNN, selectable capacity | None |
| Pitch output | Log-spaced pitch distribution decoded to Hz | 360 bins at 20 cents decoded to Hz | Period-lag minimum interpolated to Hz |
| Native cadence in inspected implementation | 256 samples / 16 ms at 16 kHz | 10 ms by default | Chosen by caller |
| Voicing evidence | Model confidence | Maximum activation | Normalized-difference depth / threshold |
| Principal appeal | Small neural model and fast CPU inference | Strong learned waveform representation | Transparent, dependency-light, no training |
| Important caveat | Paper benchmark is author-maintained | Runtime depends strongly on model capacity | Sensitive to thresholding, noise, and octave/subharmonic ambiguity |

This table describes mechanisms, not a ranking. A detector can be fast but poorly voiced, accurate on clean singing but fragile in noise, or stable after smoothing while making worse raw frame estimates.

## SwiftF0: spectral structure plus a compact CNN

The SwiftF0 paper describes a compact neural pitch detector whose input representation is derived from a short-time Fourier transform (STFT). The released implementation documents 16 kHz audio, a 1,024-sample Hann-windowed STFT frame, a 256-sample hop, a supported model range of 46.875–2,093.75 Hz, and a default voicing threshold of 0.9. At 16 kHz, the frame spans 64 ms, the hop is 16 ms, and the linear frequency spacing is 15.625 Hz.

The paper retains STFT bins 3 through 134: 132 bins rather than all 513 non-negative-frequency bins, a reported 74% reduction. Five same-padded 5×5 convolutional layers use 8, 16, 32, 64, and 1 feature maps. A one-dimensional projection maps the 132 linear-frequency positions to 200 logarithmic pitch bins, approximately 33.1 cents apart. The paper reports 95,842 trainable parameters.

In the published Python package, the STFT-side processing is represented by the exported ONNX model and the package decodes `pitch_hz` and `confidence`. The caller supplies waveform samples; it does not need to compute an STFT itself. That distinction matters when reasoning about CPU cost and where preprocessing physically executes.

The model treats pitch estimation as a distribution over logarithmically spaced pitch positions rather than as an unconstrained linear regression. Training combines categorical cross-entropy with an L1 term in log-frequency space. At inference, the maximum-scoring bin defines a local window of ±9 bins; a normalized weighted average produces continuous F0, while probability mass inside that window becomes the confidence score. Interpolation can beat the 33.1-cent bin spacing, but “confidence” is still model evidence—not automatically a calibrated probability.

## CREPE: learning directly from the waveform

CREPE also operates at 16 kHz and consumes 1,024-sample waveform excerpts, but its learned representation is directly time-domain. The original implementation uses a six-layer convolutional network, a 360-way output covering six octaves at 20-cent spacing, and a local weighted decoding step. Its default output cadence is 10 ms, and its API can optionally apply Viterbi smoothing. Model capacity can be selected from tiny through full.

Neither representation is inherently superior. Frequency-domain input supplies a useful inductive bias for harmonic structure and can reduce the amount of raw signal the network must learn to organize. Raw-waveform input gives the network access to phase and fine temporal structure without a hand-designed transform. Accuracy, robustness, and speed depend on training data, architecture, implementation, and operating conditions—not on the representation label alone.

## YIN: periodicity without a learned model

YIN, introduced by de Cheveigné and Kawahara in 2002, starts from a time-domain difference function. For each candidate lag <var>τ</var>, it compares a signal with a delayed copy:

<div class="research-equation" role="math" aria-label="Difference at lag tau is the sum over j of the squared difference between x j and x j plus tau">
  <var>d</var><sub>t</sub>(<var>τ</var>) =
  <span class="research-equation__sum">Σ</span><sub>j</sub>
  (<var>x</var><sub>j</sub> − <var>x</var><sub>j+τ</sub>)<sup>2</sup>
</div>

A periodic signal produces minima when the lag corresponds to its period. YIN then applies cumulative-mean normalization, searches below a threshold, and interpolates around a selected minimum. The estimated frequency is <var>f</var><sub>0</sub> = <var>f</var><sub>s</sub> / <var>τ</var>, where <var>f</var><sub>s</sub> is the sample rate.

This design is interpretable and has no model download, training-set dependence, or neural-runtime startup. It is not “free,” however: a direct difference function is computationally substantial, its threshold is consequential, and noisy or spectrally ambiguous signals can create competing minima. Half-period and double-period choices lead to octave errors. YIN’s threshold-derived score is also not directly interchangeable with neural confidence.

The PitchSteps YIN implementation is a useful concrete example but not a canonical reproduction of every stage in the 2002 paper. It computes the squared difference and cumulative-mean normalized difference, selects thresholded local minima, applies parabolic interpolation, and returns 1 − <var>d</var>′(<var>τ</var>) as a confidence-like value. The app adds its own voicing and temporal filters afterward.

## What the published evidence does—and does not—show

The SwiftF0 paper reports approximately 132.6 ms to process five seconds and a roughly 42.42× CPU speed-up over the CREPE implementation tested in that paper. These are paper-reported results under that experiment’s implementation, hardware, and protocol. They are not universal constants and they say nothing directly about browser WASM performance.

<figure class="research-figure">
  <img src="/assets/images/swiftf0-comparison/author-reported-results.svg" alt="Author-reported noisy-condition accuracy and CPU runtime">
  <figcaption><strong>Figure 2.</strong> Values reported in the SwiftF0 paper, not reproduced in this article. Accuracy is averaged over Vocadito, Bach10-mf0-synth, and a held-out SpeechSynth set after adding CHiME-Home noise at 10 dB SNR. The paper’s “CREPE” runtime uses TorchCREPE, while the paper’s classical comparison is pYIN—not plain YIN. Runtime is average processing time for a five-second file on the authors’ CPU setup.</figcaption>
</figure>

The paper’s 10 dB-SNR table reports a 91.80% six-component harmonic mean for SwiftF0, 78.97% for its CREPE implementation, and 79.99% for pYIN. Its CPU table reports 132.6 ms, 5,508.3 ms, and 1,420.6 ms respectively for five seconds of audio. These figures are informative within the paper’s protocol. They do **not** establish how original TensorFlow CREPE or plain YIN would perform in the same setup.

The current `pitch-benchmark` repository is a later, changing codebase with its own datasets, dependency revisions, resampling and alignment logic, and speed protocol. Its results should not be merged with the paper table. It is also maintained by the SwiftF0 author: valuable primary evidence, but not an independent benchmark.

The original CREPE paper reports accuracy and noise-robustness experiments for its own model and comparison set. The original YIN paper reports error-rate improvements under its test conditions. Cross-paper winner selection is invalid because the datasets, metrics, signal conditions, implementations, and hardware differ. The defensible comparison is structural until all three are run in one pinned harness on the same data.

## Errors are musical, not merely numerical

<figure class="research-figure">
  <img src="/assets/images/swiftf0-comparison/pitch-errors.svg" alt="Pitch errors and their metric consequences">
  <figcaption><strong>Figure 3.</strong> Cents place frequency errors on a musical logarithmic scale. Raw Chroma Accuracy can count an octave error as correct because it ignores octave placement; Raw Pitch Accuracy cannot.</figcaption>
</figure>

<div class="comparison-explorer" id="cents-explorer">
  <div class="comparison-explorer__header">
    <div>
      <span class="comparison-explorer__eyebrow">Interactive explainer</span>
      <h3>Move an estimate away from A4</h3>
    </div>
    <output id="cents-value" for="cents-slider">+0 cents</output>
  </div>
  <label for="cents-slider">Prediction error</label>
  <input id="cents-slider" type="range" min="-1200" max="1200" value="0" step="1">
  <div class="comparison-explorer__axis" aria-hidden="true">
    <span>−1 octave</span><span>A4 · 440 Hz</span><span>+1 octave</span>
  </div>
  <div class="comparison-explorer__readout">
    <div><span>Predicted F0</span><strong id="predicted-frequency">440.00 Hz</strong></div>
    <div><span>±50¢ RPA test</span><strong id="rpa-status" class="is-pass">pass</strong></div>
    <div><span>Chroma match</span><strong id="rca-status" class="is-pass">pass</strong></div>
    <div><span>Error class</span><strong id="error-class">correct</strong></div>
  </div>
  <p>At ±1,200 cents the frequency doubles or halves. Chroma still matches “A,” even though the octave is wrong.</p>
</div>

<script>
(() => {
  const root = document.getElementById("cents-explorer");
  if (!root) return;
  const slider = root.querySelector("#cents-slider");
  const centsOut = root.querySelector("#cents-value");
  const frequencyOut = root.querySelector("#predicted-frequency");
  const rpaOut = root.querySelector("#rpa-status");
  const rcaOut = root.querySelector("#rca-status");
  const classOut = root.querySelector("#error-class");
  const setStatus = (element, passes) => {
    element.textContent = passes ? "pass" : "fail";
    element.className = passes ? "is-pass" : "is-fail";
  };
  const update = () => {
    const cents = Number(slider.value);
    const frequency = 440 * Math.pow(2, cents / 1200);
    const chromaDistance = Math.min(Math.abs(cents % 1200), 1200 - Math.abs(cents % 1200));
    centsOut.textContent = `${cents >= 0 ? "+" : ""}${cents} cents`;
    frequencyOut.textContent = `${frequency.toFixed(2)} Hz`;
    setStatus(rpaOut, Math.abs(cents) < 50);
    setStatus(rcaOut, chromaDistance < 50);
    classOut.textContent =
      cents === 0 ? "correct" :
      Math.abs(cents) >= 1100 ? "octave-scale" :
      Math.abs(cents) >= 200 ? "gross error" :
      Math.abs(cents) >= 50 ? "pitch error" : "fine error";
  };
  slider.addEventListener("input", update);
  update();
})();
</script>

A useful evaluation needs several metrics:

* **Voicing precision** asks how often predicted voiced frames really are voiced. It can look good if a detector is overly conservative.
* **Voicing recall** asks how much true voiced material is recovered. It can look good if the detector calls almost everything voiced.
* **Voicing F1** balances those two, but does not measure pitch accuracy.
* **Raw Pitch Accuracy (RPA)** measures the share of reference-voiced frames estimated within a declared cents tolerance, commonly 50 cents. The exact implementation determines how voicing errors enter.
* **Raw Chroma Accuracy (RCA)** removes octave number before comparison. It can hide C4-versus-C5 errors.
* **Absolute cents error** describes tuning error on aligned voiced frames. A median can hide rare catastrophic jumps.
* **Octave-error or gross-error rate** exposes failures hidden by a typical-error statistic.

No single number answers “which detector is best?” A vocal tuner may value low octave-error rate and stable voicing; transcription may care about note boundaries; embedded use may impose a hard real-time and memory budget.

## A reproducible three-way experiment

<figure class="research-figure">
  <img src="/assets/images/swiftf0-comparison/benchmark-protocol.svg" alt="Benchmark protocol for SwiftF0, CREPE, and YIN">
  <figcaption><strong>Figure 4.</strong> Comparison protocol used by the included harness and proposed labelled evaluation. Resampling, model loading, threshold selection, frame alignment, and timing boundaries are controlled explicitly.</figcaption>
</figure>

For runtime, each system must receive the same mono signal. Neural models should be loaded once, warmed up, and timed repeatedly. Cold start and warm inference are separate product questions. Report median and p95, not a single run, and state the CPU, operating system, package versions, thread count, model capacity, and execution provider.

For accuracy, predictions must be aligned by timestamps rather than array index. CREPE defaults to 10 ms output, SwiftF0 to 16 ms, and YIN’s hop is configurable. Thresholds should be documented defaults or selected on a separate validation set—not tuned on the test set.

The included [`compare_swiftf0_crepe_yin.py`](https://github.com/richhiey/richhiey.github.io/blob/master/scripts/compare_swiftf0_crepe_yin.py) performs a same-file timing comparison using SwiftF0, original CREPE-full, and `librosa.yin`. That YIN label is deliberate: it is a maintained implementation of the algorithm, not the authors’ historical program and not pYIN. The script excludes shared WAV loading/resampling from warm timing and records environment metadata.

This publication does not include a filled results table. The necessary optional ML dependencies and a controlled labelled dataset were not run for this deployment. A blank or invented “local benchmark” would be less scientific than stating that boundary clearly.

## Case study: the PitchSteps browser integration

The inspected PitchSteps revision is [`ac0279b`](https://github.com/richhiey/pitchsteps/tree/ac0279b97f116d546465144d16c7deb2ddee6e72), retrieved 24 July 2026. The app is a React + TypeScript + Vite application using `onnxruntime-web` 1.27.x. The model and WASM runtime are bundled as `public/model.onnx` and `public/ort-wasm-simd-threaded.wasm`.

The runtime path is `getUserMedia → AudioWorklet → mono batches → Web Worker → 16 kHz resampling → SwiftF0 ONNX or YIN → voicing and temporal filters → MIDI/note/cents display`.

This is not an inference from the project description. It follows the source:

* `src/audio/AudioEngine.ts` creates the interactive `AudioContext`, registers the worklet, starts a module Web Worker, and transfers sample buffers to it.
* `src/audio-worklet/microphone-processor.js` averages all input channels to mono, emits 2,048-sample batches, and reports RMS, peak, and clipping state.
* `src/workers/pitch.worker.ts` linearly resamples incoming data to 16 kHz. For SwiftF0 it accumulates a 4,096-sample window, runs inference, advances by half a window (2,048 samples), and timestamps returned frames using the model hop of 256 samples.
* `src/pitch/detectors/SwiftF0Detector.ts` loads `/model.onnx` through `onnxruntime-web/wasm`, sets `numThreads = 1`, disables the proxy path, and maps the model’s `pitch_hz` and `confidence` outputs.
* `src/workers/workerProtocol.ts` configures PitchSteps with an application range of 80–1,000 Hz and a confidence threshold of 0.72. These are PitchSteps policy values, not SwiftF0’s package defaults.

The worker then adds application-level decisions. Low-level audio below −60 dBFS, clipped blocks, out-of-range estimates, and low-confidence estimates can be marked unvoiced. `CandidateTracker` accepts changes within 700 cents immediately but requires three consistent observations for a larger jump; `MedianPitchFilter` uses five frames. These choices can make the display calmer without changing the neural model’s raw output. A stable-looking tuner is therefore not the same thing as a more accurate detector.

## Latency: context is not the same as delay

At 16 kHz, SwiftF0’s 1,024-sample analysis frame is 64 ms and its 256-sample hop is 16 ms. PitchSteps accumulates 4,096 samples before an ONNX call, but emits the model’s returned frames from that window and then advances the buffer by 2,048 samples. The configured worklet batch is 2,048 samples at the browser’s input rate. The end-to-end experience also includes resampling, worker scheduling, WASM inference, filtering, React rendering, and device/browser buffering.

```text
Configured/calculated: 16 kHz analysis rate, 64 ms model frame, 16 ms model hop
Configured: 2,048-sample worklet batches; 4,096-sample SwiftF0 inference window
Configured: one WASM thread; five-frame median display filter
Unknown without target-device measurement: microphone and browser buffering,
  worker queue delay, ONNX runtime time, render delay, and total perceived latency
```

The correct measurement is a timestamped, device-specific experiment, not the STFT window length copied into a latency claim.

## Minimal adapters

The shared output shape makes alignment and metric code easier to review:

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class PitchTrack:
    timestamps_s: np.ndarray
    frequency_hz: np.ndarray
    confidence: np.ndarray
    voiced: np.ndarray
```

For SwiftF0’s Python package, the minimal path is:

```python
import librosa
from swift_f0 import SwiftF0

audio, sr = librosa.load("voice.wav", sr=None, mono=True)
track = SwiftF0().detect(audio, sr)
print(track.timestamps[:3], track.pitch_hz[:3], track.confidence[:3], track.voiced[:3])
```

For CREPE’s original package:

```python
import librosa, crepe

audio, sr = librosa.load("voice.wav", sr=None, mono=True)
time, frequency, confidence, activation = crepe.predict(
    audio, sr, model_capacity="full", step_size=10, center=True, viterbi=False
)
voiced = confidence >= 0.5  # Example policy; do not call this calibrated.
```

For a maintained YIN implementation:

```python
frequency = librosa.yin(
    audio, fmin=46.875, fmax=2093.75, sr=sr,
    frame_length=1024, hop_length=256
)
timestamps = librosa.times_like(frequency, sr=sr, hop_length=256)
```

These examples intentionally retain each package’s normal preprocessing and output cadence. A serious evaluation must then timestamp-align the tracks and document any threshold selection on a validation set rather than tuning on the test set.

## Limitations and what this integration does not prove

SwiftF0’s supported range does not guarantee equal accuracy at its boundaries. Performance can change with microphone frequency response, room reverberation, breath noise, consonants, note attacks, vibrato, weak fundamentals, missing fundamentals, and accompaniment. The model is monophonic, and the PitchSteps UI further restricts accepted estimates to 80–1,000 Hz for its exercise design.

The browser path is also different from offline Python use. It depends on the browser’s sample rate, a simple linear resampler, WASM execution, device thermal behavior, and AudioWorklet/Worker support. The current source bundles the model locally and sends PCM to a local worker; it does not show a microphone upload path. That supports a local-first design claim for this revision, but it does not make the system immune to normal web asset requests or prove privacy properties beyond the inspected code.

PitchSteps demonstrates a practical integration—not that SwiftF0 is universally best, not that it is 42× faster in a browser, and not that post-processing can recover errors the detector never produced. YIN’s availability as a fallback also does not establish equivalence: the two paths have different inference windows, score semantics, and computational behavior.

## Reproduction and references

The source versions used for this post are recorded in [`docs/swiftf0-evidence-ledger.md`](https://github.com/richhiey/richhiey.github.io/blob/master/docs/swiftf0-evidence-ledger.md) and the experiment protocol is in [`docs/swiftf0-methodology.md`](https://github.com/richhiey/richhiey.github.io/blob/master/docs/swiftf0-methodology.md). The intended setup is:

```bash
python -m venv .venv
. .venv/bin/activate
pip install swift-f0 crepe librosa soundfile numpy
python scripts/compare_swiftf0_crepe_yin.py voice.wav \
  --output results/swiftf0-crepe-yin-comparison.json
```

Primary references:

1. Nieradzik, L. “SwiftF0: Fast and Accurate Monophonic Pitch Detection.” [arXiv:2508.18440](https://arxiv.org/abs/2508.18440).
2. [SwiftF0 source, commit `64700fc`](https://github.com/lars76/swift-f0/tree/64700fce8ef39c2970814bf427ac1d75a2f20d72).
3. [Pitch benchmark, commit `87982db`](https://github.com/lars76/pitch-benchmark/tree/87982db236ac7fd05bf2cda4ed39331bafecb7fc).
4. Kim, J. W., Salamon, J., Li, P., and Bello, J. P. “CREPE: A Convolutional Representation for Pitch Estimation.” [arXiv:1802.06182](https://arxiv.org/abs/1802.06182).
5. [Original CREPE implementation, commit `c9b71ce`](https://github.com/marl/crepe/tree/c9b71ce61491454125a0693f584f7244f29d9884).
6. de Cheveigné, A. and Kawahara, H. “YIN, a fundamental frequency estimator for speech and music.” *JASA* 111(4), 2002. [PubMed record](https://pubmed.ncbi.nlm.nih.gov/12002874/).
7. [PitchSteps source, commit `ac0279b`](https://github.com/richhiey/pitchsteps/tree/ac0279b97f116d546465144d16c7deb2ddee6e72).
