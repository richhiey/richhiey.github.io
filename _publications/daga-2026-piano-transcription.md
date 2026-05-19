---
layout: page
title: Towards Compressed Transformers for Piano Transcription
eyebrow: DAGA 2026
subtitle: Contribution accepted to the Music Information Retrieval (MIR) 1 session.
date: 2026-03-26 09:20:00 +0100
summary: A DAGA 2026 contribution on compressing transformer-based piano transcription models for constrained environments.
link: https://pub.dega-akustik.de/DAGA_2026/konferenz-1953.html
link_label: Original DAGA publication
acceptance: Accepted contribution
presentation_type: Vortrag (strukturierte Sitzung)
session: Music Information Retrieval (MIR) 1
abstract_id: DAGA2026/505
doi: https://doi.org/10.71568/daga2026.505
manuscript_label: PDF-Download
authors:
  - Thomas Prätzlich
  - Richhiey Thomas
  - Sebastian Stober
---

Thomas Prätzlich, Richhiey Thomas, Sebastian Stober

## Abstract

Recently, the sequence-to-sequence transformer model for piano transcription (TPT) has shown state-of-the-art performance. However, its memory and compute requirements still limit its use in constrained environments such as mobile phones. To address these limitations, we explore model compression techniques for reducing memory and compute demands. First, we apply importance-based attention pruning to reduce the number of model weights. We compare individually and jointly pruning the model's attention components, and find the encoder's self-attention component to be most sensitive to pruning. Next, we fine-tune the pruned models with a knowledge distillation loss to recover performance lost during pruning. Finally, we apply dynamic weight quantization and evaluate its impact on model storage size and transcription metrics. With these compression techniques, the TPT model can be reduced by about 4x compared to the baseline without a drastic reduction in transcription performance.


## Acceptance details

- Accepted contribution
- Presentation: Vortrag (strukturierte Sitzung)
- Session: Music Information Retrieval (MIR) 1
- Day / Time: 26.03.2026, 09:20-09:40
- Abstract ID: DAGA2026/505
- DOI: [10.71568/daga2026.505](https://doi.org/10.71568/daga2026.505)
- Manuscript: [PDF-Download](https://pub.dega-akustik.de/DAGA_2026/konferenz-1953.html)
