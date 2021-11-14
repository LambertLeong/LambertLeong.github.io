---
layout: post
cover: assets/images/projects/nature_commsmed_3cb_icad/heatmap_3cb_breast_lesions.png
title: Compositional Breast Cancer Imaging with Artificial Intelligence 
date: 2021-11-13
categories: projects
author: Lambert
published: false
featured: false
permalink: /projects/compositional-breast-cancer-ai
comments: true
description: "Compositional breast cancer imageing with artificial intelligence "
summary: Compositional breast cancer imageing with artificial intelligence .
labels:
    - breast cancer
    - X-ray
    - mammography
    - radiology
    - CAD
    - machine learning 
    - AI
    - artificial intelligence
    - deep learning
tags: breast cancer X-ray mammography radiology CAD machine learning AI artificial intelligence deep learning
---

# TLDR #

* This post is in direct response to the article entitled, [“Dual-energy three-compartment breast imaging for compositional
biomarkers to improve detection of malignant lesions”](https://www.nature.com/articles/s43856-021-00024-0){:target="_blank"}.
* Compositional breast imaging allows for the discovery of novel biomarkers of cancer
* Compositional information is diagnostically relevant and could help improve cancer detection thus reducing the number of 
  unneeded biopsies.

---  

# Contents #
* [Current Breast Cancer Imaging Technologies](#head-breast-imaging)
* [The Biopsy Problem](#head-biopsy)
* [What is Compositional Imaging](#head-compositional-imaging)
* [How Can Composition Help](#head-composition)
* [The Role of Artificial Intelligence ](#head-ai)
* [What is Next for 3CB](#head-next)

## Current Breast Cancer Imaging Technologies <a name="head-breast-imaging"></a> ##

As of today (2021) breast cancer is the leading cause of cancer mortality in women, worldwide. There are several 
treatment options such as surgical removal, chemotherapy, and radiation however, it is only a part of the solution. 
Finding and identifying cancers early is just as important, if not more, than the treatments themselves.

Imaging has had a tremendous impact on reducing cancer mortality. Mammography, an X-ray based imaging technique, is the
primary imaging technology for breast cancer and it allows clinicians to see the underlying tissues and structures.
Within the last decade, digital breast tomosynthesis (DBT) has become the standard of care and this imaging technique 
results in a three dimensional (3D) X-ray image while standard mammography provides a 2D image.

<center>
  <a name="TODO"></a>
<img src="/assets/images/projects/nature_commsmed_3cb_icad/CAD_delineations.png" width="50%" alt="TODO">
<br>
    Figure X: TODO
</center>

Images acquired from standard mammography or DBT are reviewed by radiologists who look for suspicious lesions and 
calcifications. Calcifications in breast tissue are not uncommon and sometimes indicate cancer or a risk of developing
cancer.  Computer-aided detection or CAD software has been developed and approved by the food and drug administration 
(FDA) to help assist clinicians with the process of screening images for cancer.  Recent advances in artificial 
intelligence (AI) has led to drastic improvements in CAD and even the development of AI based CAD software.

## The Biopsy Problem <a name="head-biopsy"></a> ##

So with all these great advances in breast imaging technology the fight against cancer should be easier right? The
simple answer is yes but there is a slight problem. While it is true that imaging has helped to identify more cancers 
and reduce mortality rates, there is still the issue of false positive biopsies. When a lesion is deemed suspicious on
imaging, it is biopsied. A biopsy is an invasive procedure in which a tissue sample of the suspicious lesion is taken 
from a woman's breast to be viewed under a microscope. A false positive biopsy means that the pathologist did not find 
any signs of cancer in the tissue and the lesion seen on imaging is benign or non-cancerous. Essentially, false 
positives lead to unnecessary invasive biopsies and can be detrimental to a person's physical and mental health. 
This problem exists in part because imaging has become more sensitive and many more lesions can be seen. However, 
specificity has not improved enough meaning it is still difficult to tell a cancerous lesion from a non-cancerous lesion.

## What is Compositional Imaging <a name="head-compositional-imaging"></a> ##

Three compartment breast (3CB) imaging is a dual-energy X-ray technique that produces images or maps of the different 
tissue types within an imaged breast. The 3CB technique was inspired by dual-energy X-ray absorptiometry (DXA) which is
commonly used to evaluate bone density and body composition. With 3CB, two images are taken in quick succession. One
image is at a low energy, equivalent to a standard mammogram, and the other image is taken at a higher energy. X-rays 
at different energies will have different behaviors when passing through different tissues and the contrasts between the
high and low energy X-ray images are used to derive the specific tissue types. The 3CB imaging technique helps to 
visualize and quantify the amount of lipid, water, and protein in the breast.

<center>
  <a name="TODO"></a>
<img src="/assets/images/projects/nature_commsmed_3cb_icad/invasive_breast_cancer_3cb.png" width="90%" alt="TODO">
<br>
    Figure X: TODO
</center>
<br>

It should be noted that higher energy X-rays used in 3CB are safe and the level of radiation is nothing to be concerned 
with. In fact, 3CB imaging requires only 2 images while standard DBT images require about 7 to 9 images, depending on 
the system. Therefore, the level of additional radiation resulting from the 3CB technique is comparable, if not lower, 
than a DBT image sequence. To further insist on the safety of 3CB, contrast enhanced mammography (CEM) uses a nearly 
identical imaging protocol in which high and low energy images are acquired. CEM is also approved by the FDA and may be
overall more risky than 3CB since the contrast agent used in CEM could provoke a bad reaction in anaphylaxis.

## How Can Composition Help <a name="head-composition"></a> ##

It has been known that composition is important with respect to breast cancer.  Breast density is a powerful risk factor
and density often results from high fibroglandular tissue or protein. Others have studied breast cancer lesions at a
cellular/molecular level and discovered that invasive lesion types tend to consume or metabolize lipids. It is 
hypothesized that the mechanism for this behavior was due to the aggressive growth nature of invasive breast lesions. 
Lipids or fats are an energy source and aggressive tumors will consume whatever they can to fuel their rapid growth.  
As a result, we found that we could pick up on a signal that characterized malignant lesion types. This signal consisted
of cancerous lesions having lower fat or lipid content when compared to the surrounding regions.

<center>
  <a name="TODO"></a>
<img src="/assets/images/projects/nature_commsmed_3cb_icad/lesion_compositional_signatures.png" width="90%" alt="TODO">
<br>
    Figure X: TODO
</center>
<br>

## The Role of Artificial Intelligence  <a name="head-ai"></a> ##

To demonstrate the utility of our 3CB compositional imaging we used AI to see if the compositional difference between 
cancerous and non-cancerous lesions could be learned.  We also wanted to see how the compositional information derived 
from the 3CB technique adds useful diagnostic information to existing clinical paradigms.  We used CAD as our baseline 
and we wanted to see if AI with 3CB could outperform CAD.

<center>
  <a name="TODO"></a>
<img src="/assets/images/projects/nature_commsmed_3cb_icad/cad_vs_deeplearnin_auroc.png" width="90%" alt="TODO">
<br>
    Figure X: TODO
</center>
<br>

As you can see from our area under the receiver operating characteristic curves (AUC) that the AI+3CB+CAD model 
outperformed CAD alone. This indicates that composition is important and offers additional information not captured 
solely by CAD. In other words, CAD and radiologists with standard mammography use shape, texture, and morphometry 
information for identifying cancer. 3CB offers that same information as well as composition which has proven to be 
beneficial.  The integrated discrimination improvement (IDI) plot shows that the improved performance is manly due to a
reduction in false positives.  As discussed before, there is a biopsy problem and reducing false positives using 3CB 
composition could reduce unnecessary biopsies and ameliorate the problem.

<center>
  <a name="TODO"></a>
<img src="/assets/images/projects/nature_commsmed_3cb_icad/idi_nri_birads_curve.png" width="90%" alt="TODO">
<br>
    Figure X: TODO
</center>
<br>

## What is Next for 3CB <a name="head-next"></a> ##

We are continuing our work and research on 3CB by adapting the protocol to work with CEM machines 
[1R01CA257652-01A1](https://reporter.nih.gov/search/kYOrRhTpeUyu0DUhEhlo_g/project-details/10316696#description){:target="_blank"}.
Using existing contrast enhanced mammography machines approved by FDA for our 3CB imaging would help accelerate the 
adoption of the technology.
