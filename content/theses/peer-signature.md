# Semi-Automatic Extraction and Comparison of Signature Stroke Paths

**Contact:** <a href="mailto:marco.peer@unifr.ch">Marco Peer</a>

Note: The thesis is in collaboration with Zurich Forensic Science Institute.

## Overview
In forensic handwriting examination, comparisons are typically based on the visual inspection of handwritten samples. However, representing signatures as vector-based stroke paths could enable additional quantitative analyses of writing shapes.

Signatures on paper can be digitised as images, but extracting the underlying writing trajectories remains challenging. Converting handwriting into SVG paths allows strokes to be represented as sequences of coordinates.

These coordinates can subsequently be transformed into x-y series, enabling the application of similarity measures such as **Dynamic Time Warping (DTW)** or related algorithms for shape comparison (Figure 1).

<figure style="text-align: center;">
  <img src="/theses/signature.png" style="width:80%;">
  <figcaption>Figure 1. Example of a DTW-alignment between two signatures.</figcaption>
</figure>


This master’s thesis investigates methods to convert paper-based signatures into SVG stroke paths and explores algorithms for automatic form comparison of handwriting shapes.

## Objectives
- Review existing approaches for stroke extraction from handwritten images  
- Develop or evaluate tools that convert signatures into SVG path representations  
- Investigate semi-automatic workflows that allow experts to refine extracted stroke paths  
- Transform SVG paths into coordinate sequences suitable for algorithmic comparison  
- Evaluate similarity measures such as **Dynamic Time Warping (DTW)** and related methods  
- Assess the usefulness of such tools as support systems for forensic handwriting examiners  


## Methodology
- **Literature Review:** Survey methods for stroke extraction, vectorisation, and handwriting comparison  
- **Stroke Path Extraction:** Implement or evaluate algorithms that convert scanned signatures into SVG paths  
- **Semi-Automatic Refinement:** Explore workflows where experts can correct or refine extracted stroke paths  
- **Coordinate Transformation:** Convert SVG paths into ordered x–y coordinate sequences  
- **Shape Comparison:** Apply algorithms such as DTW or other approaches to measure shape similarity  
- **Evaluation:** Assess the usefulness and limitations of the proposed workflow  
- **Reporting:** Document results in the master’s thesis and final presentation  


## Skills Required
- Programming skills  
- Basic knowledge of statistics  
- Interest in AI and handwriting examination  

Created: 02.04.2026
