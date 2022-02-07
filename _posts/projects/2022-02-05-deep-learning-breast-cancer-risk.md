---
layout: post
cover: assets/images/projects/deep_learning_breast_cancer_risk/AI_breast_cancer_risk.png
title: Artificial Intelligence Can See Breast Cancer Before it Happens 
date: 2022-02-05
categories: projects
author: Lambert
published: true
featured: false
permalink: /projects/deep-learning-breast-cancer-risk
comments: true
description: "Deep Learning Predicts Interval and Screening-detected Cancer from Screening Mammograms: A Case-Case-Control Study in 6369 Women"
summary: Deep Learning Predicts Interval and Screening-detected Cancer from Screening Mammograms, A Case-Case-Control Study in 6369 Women
labels:
    - breast cancer 
    - X-ray
    - mammography
    - radiology
    - risk
    - machine learning 
    - AI
    - artificial intelligence
    - deep learning
    - python
tags: breast cancer X-ray mammography radiology machine learning AI artificial intelligence deep learning risk
---

# Key Points #

* Our image base deep learning model identified __unique__ signals of screen-detected cancer risk
* Breast density is a better predictor of interval cancer risk
* This post is in direct response to the article entitled, [__“Deep Learning Predicts Interval and Screening-detected 
Cancer from Screening Mammograms: A Case-Case-Control Study in 6369 Women”__](https://pubs.rsna.org/doi/abs/10.1148/radiol.2021203758){:target="_blank"},
published in Radiology and presented at the [Radiological Society of North America (RSNA)](https://press.rsna.org/timssnet/media/pressreleases/14_pr_target.cfm?ID=2280){:target="_blank"} 
  
---  

# Contents #
* [Why is Risk Important](#head-why-risk)
* [Current Risk Solutions](#head-solution)
* [Our Contribution Towards the Risk Solution](#head-ai-modeling)
* [Surprising Results](#head-results)
* [What’s Next](#head-next)

The use of artificial intelligence (AI) and deep learning (DL) in the medical and healthcare field has been increasing 
at an astonishing rate. While the Health Insurance Portability and Accountability Act (HIPAA) is important for the 
protection of personal health information, it presented as the biggest barrier for gathering large data sets required 
for deep learning. Several strategies have been successfully implemented to gather lots of data for training medical AI 
systems without risking patient privacy. AI continues to have a significant impact on medical imaging and deep learning 
models are constantly being developed to look for anomalies such as bone fractures or possible cancer.

The introduction of breast cancer screening has helped to reduce cancer mortality rates in women as well as provide a 
consistent source of image data. Typically, women 40 years and older receive biannual or annual screening mammograms to 
check for any signs of cancer. Many have developed AI to detect and segment cancers within a mammogram yet, fewer have
developed image based deep learning models to predict risk. In the work being described, we developed a model to predict
an individual’s breast cancer risk; more specifically interval and screen-detected cancer risk.


## Why is Risk Important? <a name="head-why-risk"></a> ##
<center>
  <a name="img-stock"></a>
<img src="/assets/images/projects/deep_learning_breast_cancer_risk/breast_cancer_risk.jpg" width="85%" alt="artificial intelligence breast cancer">
<br>
</center>
<br> 

Predicting breast cancer risk is analogous to forecasting which is an innately hard problem in all fields of science. 
By comparison, accurately quantifying a patient's risk of cancer is more difficult than detecting the presence of cancer
through some diagnostic test like a mammogram. Understanding breast cancer risk and the many factors associated with it
is important for cancer prevention and monitoring strategies. The best way to reduce cancer mortality is to prevent 
cancer from developing in the first place and accurate assessments of risk are essential. 

There are three clinically relevant outcomes when evaluating risk within a screening population.  These outcomes include
screen-detected (case), interval (case), or no (control) cancer risk. A screen-detected cancer is a cancer that is found
as a result of a routine screening mammogram. In our study, we further defined it as a cancer that occurred within 12 
months after a positive screening mammogram. An interval cancer is a cancer that is found between the normal screening 
interval (biannual or annual) and was defined in our study as an invasive cancer that occurred within 12 months after 
a negative screening mammogram. Interval cancers are known to grow more rapidly and be more aggressive in biology. They 
are often found through palpation or self examination.

## Current Risk Solutions <a name="head-solution"></a> ##

The Gail, BRCAPRO, Tyrer-Cuzick, and Breast Cancer Surveillance Consortium (BCSC) risk models are examples of 
established models used clinically. They all use varying combinations of known breast cancer risk factors which can 
include age, body mass index (BMI), and/or breast density. Imaging is not directly used in clinical models and 
oftentimes only used to get better measurements of breast density. A few image based AI models have been published 
demonstrating comparable risk predictions performance. However, these AI models were constrained to a binary 
classification and did not include the three possible outcomes within a screening population.


## Our Contribution Towards the Risk Solution <a name="head-ai-modeling"></a> ##

Our dataset consisted of 6,369 women recruited from the Mayo Clinic and the University of California at San Francisco.
Four standard mammographic views which include the craniocaudal (CC) and mediolateral oblique (MLO) views for both the
left and right breast were acquired on each woman. Mammographic images were received in their raw or “for-processing” 
format with pixel ranges between 0 and 2<sup>14</sup>. Custom built software was used to filter the image into the 
“for-presentation” format that radiologists are used to reading. It is important to reiterate that the images used for 
our risk modeling were acquired at least 6 months prior to cancer diagnosis. Thus the images we use for modeling were 
negative and contained no visible cancers as determined by expert radiologists. 

Model development took place at the University of Hawaii Cancer Center. A self imposed blind was implemented to account 
for possible overfitting. The data was split into a train and hold-out test set and the test set was never sent to the 
University of Hawaii. We further split the training set into a train, validate, and test set for our initial model 
evelopment. Once we were confident in our modeling architecture and hyperparameters were optimized, the final model was
trained on the entire training set.  The final risk model was then sent to our collaborates to be evaluated on the
hold-out test set. The process was very kaggle-esque. 

<center>
  <a name="img-model"></a>
<img src="/assets/images/projects/deep_learning_breast_cancer_risk/deeplearning_netowrk.png" width="80%" alt="Deep Learning Architecture">
<br>
    <b>Figure 1:</b> Four parallel networks for each mammographic view
</center>
<br> 

The novelty of our deep learning model resulted from using four parallel networks to look at all imaging information 
simultaneously for prediction, seen in [Figure 1](#img-model). Other than density, imaging biomarkers of risk are underexplored and not well 
characterized. Although cancer may develop in only one side of the breast, we suspected signals of risk may be present 
throughout both the ipsilateral and contralateral breast. Each of the four networks was responsible for learning the 
information in one of the four mammographic views and so there was a LCC, RCC, LMLO, and RMLO network. Outputs from all 
networks were pooled and used to make final predictions of risk.

## Surprising Results! <a name="head-results"></a> ##

Using an objective versus else approach, we evaluated risk predictions using area under the receiver operating 
characteristic curve (AUC). Our model performed with an AUC of 0.66 when classifying controls verse everything else, 
0.63 when classifying screen-detected cancer verse everything else, and 0.71 when classifying interval cancer verse 
everything else. See [Figure 2](#img-auc)  Risk modeling is a hard problem and these results are on par, if not better, than current clinical 
risk models.

<center>
  <a name="img-auc"></a>
<img src="/assets/images/projects/deep_learning_breast_cancer_risk/ccc_auc.png" width="90%" alt="Deep learning risk prediction AUC performance">
<br>
    <b>Figure 2:</b> Final model performance on hold-out test set measured by area under the receiver operating characteristic curve (AUC) 
</center>
<br>

To further interrogate possible imaging signals of risk, we compared our AI models performance against conditional 
logistic regression models built using common clinical risk factors.  These risk factors included clinical and automated
Breast Imaging Reporting and Data System (BI-RADS), BMI, and dense volume.  Automated measurements were obtained using 
Volpara which is a clinically approved breast density software.  In the screen-detected cancer case, c-statistics 
improved when combining risk factors with deep learning, shown in [Figure 3](#img-risk-factor). This improvement indicated that deep learning was able to pick 
up on <u>imaging signals related to risk that are orthogonal or unique to clinical risk factors</u>. Although we 
hypothesized it, it was still surprising! In the interval cancer case, deep learning models were not able to outperform
models built on breast density alone. In other words, <u>breast density remains the most powerful predictor of interval
cancer risk</u>. This was even more surprising!! Breast density is a risk factor because dense tissue can obscure images
and mask possible lesions. Dense tissue may also be masking possible signals of risk and impairing our AI models performance.

<center>
  <a name="img-risk-factor"></a>
<img src="/assets/images/projects/deep_learning_breast_cancer_risk/deep_learning_performance.png" width="100%" alt="Deep learning vs clinical risk factors">
<br>
    <b>Figure 3:</b> Deep learning performance compared against clinical risk factor models
</center>
<br>

## What’s Next <a name="head-next"></a> ##

Disentangling the density signal away from possible interval cancer risk signals is a possible future direction of this 
research. There are more advanced AI techniques, such as adversarial approaches, that may be helpful for understanding 
the interplay between breast density, imaging, and interval cancer risk. Hawaii has a higher incidence of late stage 
cancer when compared to the rest of the United States. The mechanism is not yet known but many hypothesize that the 
unique enthic makeup of the population plays a role. Our success with deep learning in this study gives us confidence 
that predicting risk of late stage cancer is possible. We welcome comments, conversations, discussion, and collaboration 
on topics discussed here. Feel free to reach out and join the fight against cancer.


### Continuing the Discussion ###

* [__Read the paper__](https://pubs.rsna.org/doi/abs/10.1148/radiol.2021203758){:target="_blank"}
* [__Check out the github__](https://github.com/shepherd-lab/dl-mammography){:target="_blank"}
* [__Contact an author__](https://www.lambertleong.com/contact){:target="_blank"}
* [__Contact the lab__](https://shepherdresearchlab.org/about/our-team/){:target="_blank"}