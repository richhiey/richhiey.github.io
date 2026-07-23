---
layout: page
title: Pitchsteps
eyebrow: Browser-based pitch coach
subtitle: A private, local-first vocal warm-up tool for building a steadier, more confident voice.
date: 2026-07-23 00:00:00 +0200
summary: VocalWarmup turns pitch practice into a focused browser session with guided notes, live pitch tracking, and note-by-note feedback.
link: https://pitchsteps.vercel.app/
link_label: Try Pitchsteps
---

## Overview

Pitchsteps is a browser-based vocal warm-up app built to help singers start with a steadier, more confident voice. The experience guides a user through short ascending and descending exercises, plays reference tones, listens through the microphone, and shows how closely each note matches the target.

Audio stays on the device: the app analyzes microphone input locally in the browser rather than sending recordings to a server. That makes the tool lightweight and private enough for quick practice sessions.

## What I built

- Guided warm-ups with selectable exercises, starting note, tempo, and guide volume.
- Real-time pitch detection with microphone selection, calibration, and detector fallbacks.
- A live pitch trail that makes the target note and the performed note easy to compare.
- Session scoring with note-level accuracy, stability, voiced coverage, and pitch-direction feedback.
- Optional local recording playback for reviewing a completed exercise.

The app is built with React, TypeScript, Vite, Web Audio APIs, and `onnxruntime-web`. The code is organized around separate audio, exercise, pitch, scoring, visualization, and state-management layers so the real-time experience remains testable and easy to extend.

## Why it matters

Pitch practice can be hard to evaluate without a teacher or recording setup. Pitchsteps makes the feedback loop immediate: hear the target, sing it, see the pitch trail, and get a concrete result to work from. The goal is not to replace a vocal coach, but to make consistent, low-friction practice easier to begin.

## Links

- [Live app](https://pitchsteps.vercel.app/)
- [Source code on GitHub](https://github.com/richhiey/pitchsteps)
