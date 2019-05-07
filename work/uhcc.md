---
layout: work
type: work
published: true
image: images/uhcc.jpg
title: University of Hawaii Cancer Center
permalink: work/uhcc
date: 2019
labels:
  - Software Engineering
  - Machine Learning
  - Cancer Research
  - Breast Cancer
  - Deep Learning
  - Neural Networks
  
summary: From Nov 2018 to present, I worked at the University of Hawaii Cancer Center in the Shepherd Research Lab(SRL) as a PhD graduate research assistant.
---

__Responsibilities__

As a PhD Graduate Research Assistant under [John Shepherd](https://shepherdresearchlab.org/about/our-team/john-shepherd/) PhD, I conduct imaging research which is primarily focused on breast cancer. Our research group is focused on discovering novel imaging bio-markers to detect cancer and asses risk.  Machine and deep learning are big components of my research as it is a powerful tool for analysing high dimensionality data that is images.  My background in high performance computing and software engineering allows me to fully leverage our GPU clusters to rapidly build and train machine learning models.  


**Projects**

<div class="ui images">
  <img class="ui image medium right floated round image" src="../images/real_processed_sinogram.png">
</div>

- _Breast Thickness Tomosynthesis_ - Breast density is a biomarker that is associated with cancer risk.  Accurate point thickness measurments of the breast are necissary for calculating density.  We use nine views from a sinogram to solve and inverse problem and derive point thickness measurments.

    - I developed an unsupervised machine learning model using PCA to characterize sinograms resulting from breast of different thickness, widths, and densities.  
- _[3CB](https://3cb.shepherdresearchlab.org/)_ - 3 Compartment Breast of 3CB is a project that can render breast lesions specific to the three major components that make  up breast tissue.  These components include water, lipid, and protien and quantifying the amount of each component helps to assess cancer risk and need for biopsies.
    - For this project I refactored the existing 3D rendering code and plan to incorperate the breast thickness tomosynthesis algorithm to get accurate thicknesses and make up of breast lesions.    
- _Interval vs Screening Cancer Detection_ - Screening cancers are cancers detected from a screening mammogram.  Interval cancers are a case of breast cancers that found after a previous screening mammogram reported a negative finding.  We use deep learning and neural networks to search for signals in interval cancer cases to try and catch the cancers early and at the time of screening.
    - Our group is fortunate enough to work with the largest data set of it's kind for this project.  I helped with high throughput preprocessing and cleaning of our large image dataset .  I also research and exlpore of different deep learning techniques and models to acheive high sensetivity and specificity for interval cancer cases. 