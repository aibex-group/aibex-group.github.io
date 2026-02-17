# Adaptive Multi-Loss Balancing for Offline Handwritten Text Recognition

**Contact:** <a href="mailto:arthur.neto@unifr.ch">Arthur F. S. Neto</a>

<figure style="text-align: center;">
  <img src="/theses/neto-multiloss-htr.png" style="width:100%">
  <figcaption>Figure 1: Sample images from the IAM, RIMES, Saint Gall, and Washington datasets.</figcaption>
</figure>

## Overview

Offline Handwritten Text Recognition (HTR) aims to automatically convert scanned handwritten documents into digital text. Modern HTR systems typically use an encoder-decoder architecture trained with the Connectionist Temporal Classification (CTC) loss [1]. Recent research has introduced an auxiliary CTC loss applied at the encoder level, which is optimized with the decoder CTC loss during training. This auxiliary loss improves gradient flow and stabilizes learning, particularly in the early encoder layers [2].

In previous work, the contribution of the encoder CTC loss is controlled by a fixed weighting factor (for example, 0.1), which does not adapt to variations in dataset size or characteristics [3]. However, empirical evidence suggests that the optimal encoder-decoder loss balance depends on dataset size. Smaller datasets such as Saint Gall or Washington benefit from a stronger encoder loss contribution, whereas larger datasets like IAM or RIMES tend to perform better with a smaller encoder influence. A fixed weighting strategy may therefore limit model performance across different data volumes.

This thesis proposes an adaptive multi-loss balancing strategy to dynamically adjust the relative contribution of the encoder and decoder CTC losses in Offline HTR models. By adapting the loss balance according to dataset characteristics, the method aims to improve training stability and recognition accuracy. Experiments will be conducted using the HTR-Flor baseline model and evaluated on IAM, RIMES, Saint Gall, and Washington datasets.

---

## Objectives

- Review CTC-based HTR systems and multi-loss training strategies
- Reproduce baseline results using fixed encoder CTC loss weighting
- Propose and implement an adaptive multi-loss balancing strategy
- Evaluate performance across IAM, RIMES, Saint Gall, and Washington datasets
- Compare results using Character Error Rate (CER) and Word Error Rate (WER)

---

## Methodology

1. **Literature Review** - Study multi-loss balancing approaches and auxiliary CTC learning
2. **Baseline** - Implement model with decoder CTC only and fixed encoder CTC weighting
3. **Dynamic Loss Strategy** - Develop and integrate a dynamic loss balancing mechanism
4. **Evaluation** - Benchmark performance on IAM, RIMES, Saint Gall, and Washington datasets
5. **Reporting** - Prepare the final thesis manuscript, presentation, and optional publication

---

## Skills Required

- Python programming
- Deep learning (TensorFlow, PyTorch)
- Interest in pattern recognition, and document analysis

---

## References

[1] A. F. S. Neto, B. L. D. Bezerra, A. H. Toselli, E. B. Lima, HTR-Flor: A Deep Learning System for Offline Handwritten Text Recognition, 33rd SIBGRAPI Conference, Porto de Galinhas, Brazil, 2020, pp. 54-61, doi:10.1109/SIBGRAPI51738.2020.00016.

[2] M. Peer, A. Scius-Bertrand, A. Fischer, CTC Transcription Alignment of the Bullinger Letters: Automatic Improvement of Annotation Quality, Proc. 2nd Int. Workshop on Computer Vision Systems for Document Analysis and Recognition (VisionDocs), 2025, pp. 1-10.

[3] G. Retsinas, G. Sfikas, B. Gatos, C. Nikou, Best Practices for a Handwritten Text Recognition System, in S. Uchida, E. Barney, V. Eglin (eds), Document Analysis Systems, DAS 2022, Lecture Notes in Computer Science, vol. 13237, Springer, Cham, 2022, doi:10.1007/978-3-031-06555-2_17.

Created: 16.02.2026
