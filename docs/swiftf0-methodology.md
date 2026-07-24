# SwiftF0–CREPE–YIN comparison methodology

This protocol is intentionally conservative. It is a recipe for a future local comparison, not a claim that the comparison has already been run.

1. Pin the SwiftF0, CREPE, benchmark, and YIN implementation revisions listed in the article.
2. Use the same mono WAV input for all three systems. Resample once to 16 kHz before invoking each API, or let every API perform the same documented resampling path.
3. Load both neural models once. Record cold-start time separately, run at least three warm-up calls for all detectors, then collect repeated warm timings and report median and p95.
4. Keep CREPE capacity, centering, hop, Viterbi setting, SwiftF0 threshold, YIN frame/hop/threshold settings, Python version, OS, CPU, thread count, and execution provider in the JSON metadata.
5. Align output tracks by timestamps, not array index. Use the benchmark repository’s metric definitions when running a labelled dataset.
6. Select voicing thresholds from documented defaults or a validation split. Never tune thresholds on the test split.
7. Report voiced precision/recall/F1, raw pitch accuracy with its cents tolerance, raw chroma accuracy, absolute cents error, octave or gross-error rate, and any aggregate harmonic mean separately.

The current portfolio deployment does not include a result file with fabricated values. A result should be committed only after the command has completed successfully and the machine and dependency metadata have been reviewed.
