# Structural Generation of HVAC Plans with the Assistance of Large Language Models

**Contact:** <a href="mailto:michael.jungo@unifr.ch">Michael Jungo</a>

<figure style="text-align: center;">
  <img src="/theses/jungo-hvac-generation-plan.png" alt="HVAC Plan Excerpt" style="width:90%;">
  <figcaption>Figure 1: Excerpt from an HVAC plan</figcaption>
</figure>

## Overview

Heating, Ventilation and Air Conditioning (HVAC) systems require extensive planning to ensure that they function
correctly and efficiently before they can be installed into a building. The resulting HVAC plans are complex technical
drawings with a variety of symbols, sometimes with small visual differences, which are connected by fairly inconspicuous
lines to indicate the flow of the water or air, respectively. These plans are not accompanied by an underlying
machine-readable representation, i.e. the visual plan is the source of truth, therefore locating and identifying the
symbols and their connections are crucial for the analysis of any given plan.

A large annotated dataset is needed to train detection models effectively, but since the annotation process of such
complex plans is tremendously time consuming, we focus on generating high quality synthetic plans that resemble the real
plans as closely as possible.

Unlike in commonly used generative image generation methods, such as diffusion models, where the location of
the generated content cannot easily be extracted, we are interested in a structural generation, such that the underlying
structure of the plan, e.g. a graph, is generated and then converted to an image.

Having a structural representation of the plan opens up the possibilities to incorporate Large Language Models (LLMs),
either by assisting in the generation of realistic layouts, or by providing a chat interface where the user can generate
a new plan with natural language and iteratively change existing plans.


## Objectives

- Review state-of-the-art methods for the generation of technical drawings.
- Implement a rendering method of a plan from a structural representation which allows extracting the position of the symbols.
- Apply LLMs to generate or modify plans through natural language.

## Methodology

1. **Literature Review** - Study rendering methods and generation of structured output.
2. **Rendering Implementation** - Create an image from any structured representation.
3. **Generation** - Explore generation techniques with the help of LLMs.
4. **Evaluation** - Determine the quality of the synthetic plans, such as by evaluating the improvement of an existing
   symbol detection approach.
5. **Reporting** - Final thesis, presentation and optional publication.

## Skills to be Acquired

- Turn a structural representation into an image while preserving the location of the elements.
- Prompting LLMs for a structured output.

Created: 03.11.2025
