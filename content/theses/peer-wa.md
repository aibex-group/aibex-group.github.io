# Writer Adaptation in Handwritten Text Recognition (HTR)

**Contact:** <a href="mailto:marco.peer@hefr.ch">Marco Peer</a>

## Overview
The digitization of historical documents requires accurate transcription of handwritten text. Variations in writing styles and deteriorated conditions make recognition challenging.  
This thesis explores **writer identification** and **writer-specific style extraction** to improve Handwritten Text Recognition (HTR). The goal is to enhance recognition accuracy by leveraging **writer-specific characteristics**.

<figure style="text-align: center;">
  <img src="/theses/peer-wa1.png" alt="Writer A" style="width:80%; margin-bottom: 10px;">
  <img src="/theses/peer-wa2.png" alt="Writer B" style="width:80%;">
  <figcaption>Figure 1: Two line images from two different writers of the Bullinger dataset [1]</figcaption>
</figure>

To evaluate the proposed writer adaptation techniques, benchmark datasets such as IAM or CVL, widely used in Handwritten Text Recognition (HTR) research, should be employed. Additionally, the evaluation will incorporate a historical dataset known for its challenges, such as the Bullinger Dataset [1]. The existing methodology for writer adaptation in HTR systems primarily relies on meta-learning techniques [2] or involves incorporating networks to extract writer styles [3]. 

## Objectives
- Review state-of-the-art writer adaptation methods in HTR  
- Implement and evaluate methods on IAM, CVL, and Bullinger datasets  
- Develop a writer adaptation algorithm for HTR  
- Compare results using CER/WER metrics  

## Methodology
1. **Literature Review** – Study meta-learning, style extractor networks, and diffusion-based approaches  
2. **Implementation** – Apply existing methods and develop a writer adaptation algorithm  
3. **Evaluation** – Benchmark on IAM, CVL, and Bullinger datasets  
4. **Reporting** – Final thesis, presentation, and optional publication  

## Skills Required
- Python programming  
- Deep learning (preferably PyTorch)  
- Interest in document analysis and historical handwriting  

## References
[1] A. Scius-Bertrand et al., *Bullinger Dataset for Writer Adaptation (BullingerDB)*, [Link](https://tc11.cvc.uab.es/datasets/BullingerDB_1)  
[2] A. Bhunia et al., *MetaHTR: Towards writer-adaptive handwritten text recognition*, CVPR, 2021  
[3] Z. Wang and J. Du, *Fast writer adaptation with style extractor network for handwritten text recognition*, Neural Networks, 2022  

Created: 01.09.2025
