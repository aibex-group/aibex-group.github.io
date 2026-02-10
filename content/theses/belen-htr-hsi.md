# Enhancing Handwritten Text Recognition in Historical Documents Using Spectral Imaging

**Contact:** <a href="mailto:ana.lopezbaldomero@unifr.ch">Ana B. López Baldomero</a>

## Overview
Many historical documents are difficult to transcribe due to different types of degradation, where conventional RGB imaging is often insufficient [1]. This master's thesis focuses on the generation and use of **synthetic hyperspectral (HSI) and multispectral (MSI) data for handwritten text recognition (HTR)**. By transforming existing annotated RGB document datasets into synthetic spectral data, the thesis evaluates whether spectral information can improve HTR performance compared to RGB approaches.

<figure style="display: flex; justify-content: center; gap: 10px;">
  <img src="/theses/hyperdoc_docs.png" width="60%">
  <figcaption>Figure 1: False RGB images of historical documents extracted from the HYPERDOC dataset [2].</figcaption>
</figure>

## Objectives
- Review state-of-the-art
- Generate synthetic HSI and MSI data from annotated RGB datasets
- Adapt an existing HTR model to spectral data
- Compare HTR performance across RGB, MSI, and HSI modalities

## Methodology
1. **Literature Review** - Spectral imaging basics and HTR models
2. **Synthetic Data Generation** - Unmixing-based [3] generation of HSI from annotated RGB datasets
3. **Model Adaptation** - Train an HTR model with RGB, MSI, and HSI inputs
4. **Evaluation** - Quantitative comparison using standard HTR metrics 
5. **Reporting** - Final thesis, presentation, and optional publication  

## Skills Required
- Python programming  
- Deep learning
- Interest in document analysis, historical handwritting and spectral imaging

## References
[1] L. Pardo et al., *Advanced imaging to recover illegible text in historic documents. The challenge of past chemical treatments for ink enhancement*, Journal of Cultural Heritage, 2024.

[2] A. B. López-Baldomero et al., *Hyperspectral dataset of historical documents (HYPERDOC)*, Scientific Data, 2025.

[3] E. M. Valero et al., *Unmixing and pigment identification using visible and short-wavelength infrared: Reflectance vs logarithm reflectance hyperspaces*, Journal of Cultural Heritage, 2023.

Created: 01.02.2026
