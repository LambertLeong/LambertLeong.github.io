---
layout: post
cover: assets/images/essays/rsna/rsna_stairs.jpg
title:  Area Under the Curve and Beyond
date: 2021-05-01
categories: thoughts
author: Lambert
published: false
featured: false
permalink: thoughts/AUC-IDI-NRI
comments: true
description: 
labels:
  - 
---

## TLDR ##
* AUC ...
* IDI ...
* NRI ...

### Area Under the Curve (AUC) ###

In machine learning and diagnostic medicine the area under the receiver operating characteristic (ROC) curve or AUC
is a common metric used to evaluate the predictive performance of a model or diagnostic test. New models are often 
bench marked, using AUCs, against established models. Comparing AUCs of new and old models to evaluate  improvement is a
 good place to start however, many end their analysis here and believe simply reporting a higher AUC is 
sufficient. AUC can be misleading as it gives equal weight to the full range of sensitivity and specificity values even 
though a limited range, or specific threshold, may be of practical interest. In this article, we show how to fully 
interigate new and improved model performance, beyond simple AUC comparisons, as to provide a more comprehensive 
understanding of improvements within the context of a given problem. We also present a coded example in Python to
 demonstrate the concepts we present.

### Example: Breast Cancer ###

Breast cancer is the leading cause of cancer death in women world wide. Early detection has helped to lower the mortality
rate and the earlier a malignancy is identified, the more likely a patient is to survive.  As such, great effort has
been allocated to developing predictive models to identify cancer.  In this example we use extracted imaging features
to build models to predict malignancy probability. We use data from the 
[Diagnostic Wisconsin Breast Cancer Database](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)){:target="_blank"}
housed at the UCI Machine Learning Repository.

As mentioned previously, AUC gives equal weight to all thresholds but this may not be practical in the context of 
breast cancer diagnosis. The [Breast Imaging Reporting and Data System or (BI-RADS)](https://www.cancer.org/cancer/breast-cancer/screening-tests-and-early-detection/mammograms/understanding-your-mammogram-report.html)
provides a course of action for a given probability of malignancy.  In short, if the probability of maligancy is greater
than 2%, a biopsy is recommended. Biopsies are invasive procedures can be physically and mentally detrimental to patients.
A new breast model would ideally be better at identifying cancers (sensitivity increase) and reducing false positives (specificity increase),
preferably below 2% to avoid invasive and unnecessary biopsies.

#### Example Set up ####
```python:
# Import Modules #
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_auc_score
```
After we import the necessary modules, we load the breast cancer data set and split the data into a train and test set.
Note, normally it is best practice to also create a validation set but for the sake of this example we will stick with
just a training and test set.
```python:
# Import data # 
data = load_breast_cancer()
# Create DataFrame and Split Data
df = pd.DataFrame(data=data['data'],columns=data['feature_names'])
df['label']=data['target']
x_train, x_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df.iloc[:,-1], test_size=0.40, random_state=123)

```
For the sake of this example, we will pretend that our reference/bench mark model was built on breast imaging features
pertaining to texture, concave points, smoothness, fractal dimension, and compactness. We will also pretend that the new
 model uses additional imaging biomarkers/features which pertain to  radius, perimeter, area, symmetry, and concavity. 
 In total, the reference model is built using a total of 15 features while the new model is built using 30 features (15 
 features used by the original model and 15 new features). The following code snippet creates to two sets of features.
```python:
ref_feat, new_feat = [],[]
for i in data['feature_names']:
    if 'fractal' in i or 'smoothness' in i or 'texture' in i or 'concave' in i or 'compactness' in i:
        ref_feat+=[i]
```
#### Modeling ####
We create a reference or "ref model" with 15 features and the "new model" with all 30 features.
```python:
# init models
ref_model = RandomForestClassifier()#max_depth=5, n_estimators=100, verbose=1,random_state=0)
new_model = RandomForestClassifier()#max_depth=5, n_estimators=100, verbose=1,random_state=0)
# fit models to train data
ref_model.fit(x_train[ref_feat], y_train)
new_model.fit(x_train[new_feat], y_train)
# make predictions on test data
test_ref_pred=ref_model.predict_proba(x_test[ref_feat])
test_new_pred=new_model.predict_proba(x_test[new_feat])
```
#### Comparing Models AUCs ###
We previously mentioned that comparing AUCs is a good starting point. We do that here to get an idea of how the new model
performed with respect to our reference model. We use the following custom function to visualize confidence intervals (CI).
```python:
def get_auc_ci(y_truth, y_pred,num_bootstraps = 1000):
    n_bootstraps = num_bootstraps
    rng_seed = 42  # control reproducibility
    bootstrapped_scores = []
    y_pred=y_pred
    y_true=y_truth
    rng = np.random.RandomState(rng_seed)
    tprs=[]
    aucs=[]
    base_fpr = np.linspace(0, 1, 101)
    for i in range(n_bootstraps):
        # bootstrap by sampling with replacement on the prediction indices
        indices = rng.randint(0, len(y_pred), len(y_pred))
        if len(np.unique(y_true[indices])) < 2:
            # We need at least one positive and one negative sample for ROC AUC
            continue
        score = roc_auc_score(y_true[indices], y_pred[indices])
        bootstrapped_scores.append(score)
        fpr, tpr, _ = metrics.roc_curve(y_true[indices],y_pred[indices])
        roc_auc = metrics.auc(fpr, tpr)
        aucs.append(roc_auc)
        tpr = np.interp(base_fpr, fpr, tpr)
        tpr[0] = 0.0
        tprs.append(tpr)
    tprs = np.array(tprs)
    mean_tprs = tprs.mean(axis=0)
    std = tprs.std(axis=0)
    mean_auc = metrics.auc(base_fpr, mean_tprs)
    std_auc = np.std(aucs)
    tprs_upper = np.minimum(mean_tprs + std*2, 1)
    tprs_lower = mean_tprs - std*2
    return base_fpr, mean_tprs, tprs_lower, tprs_upper, mean_auc, std_auc

def plot_auc(truth, reference_model, new_model,n_bootstraps=1000, save=False):
    y_truth = truth
    ref_model = reference_model
    new_model = new_model
    ref_fpr, ref_tpr, ref_thresholds = metrics.roc_curve(y_truth, ref_model)
    new_fpr, new_tpr, new_thresholds = metrics.roc_curve(y_truth, new_model)
    ref_auc, new_auc = metrics.auc(ref_fpr, ref_tpr), metrics.auc(new_fpr, new_tpr)
    print('ref auc =',ref_auc, '\newn auc = ', new_auc)   
    base_fpr_ref, mean_tprs_ref, tprs_lower_ref, tprs_upper_ref, mean_auc_ref, std_auc_ref=get_auc_ci(y_truth, ref_model,n_bootstraps)
    base_fpr_new, mean_tprs_new, tprs_lower_new, tprs_upper_new, mean_auc_new, std_auc_new=get_auc_ci(y_truth, new_model,n_bootstraps)
    plt.figure(figsize=(8, 8))
    lw = 2
    plt.plot(ref_fpr, ref_tpr, color='blue',
             lw=lw, label='Reference raw ROC (AUC = %0.2f)' % ref_auc, linestyle='--')
    plt.plot(base_fpr_ref, mean_tprs_ref, 'b', alpha = 0.8, label=r'Reference mean ROC (AUC=%0.2f, CI=%0.2f-%0.2f)' % (mean_auc_ref, (mean_auc_ref-2*std_auc_ref),(mean_auc_ref+2*std_auc_ref)),)
    plt.fill_between(base_fpr_ref, tprs_lower_ref, tprs_upper_ref, color = 'b', alpha = 0.2)
    plt.plot(new_fpr, new_tpr, color='darkorange',
             lw=lw, label='New raw ROC (AUC = %0.2f)' % new_auc, linestyle='--')
    plt.plot(base_fpr_new, mean_tprs_new, 'darkorange', alpha = 0.8, label=r'New mean ROC (AUC=%0.2f, CI=%0.2f-%0.2f)' % (mean_auc_new,(mean_auc_new-2*std_auc_new),(mean_auc_new+2*std_auc_new)),)
    plt.fill_between(base_fpr_new, tprs_lower_new, tprs_upper_new, color = 'darkorange', alpha = 0.2)
    plt.plot([0, 1], [0, 1], color='gray', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('1 - Specificity', fontsize=18)
    plt.ylabel('Sensitivity', fontsize=18)
    plt.legend(loc="lower right", fontsize=13)
    plt.gca().set_aspect('equal', adjustable='box')
```
We run the following to generate plots
```python:
plot_auc(y_test.values,test_ref_pred[:,1],test_new_pred[:,1],n_bootstraps=100)
```
<center>
    <a name="auc_plot"></a>
  <img src="/assets/images/essays/auc_idi_nri/auc_ci_example.png" width="50%" alt="breast models AUC with confidence intervals">
<br>
  	Figure 1: AUC curves with confidence intervals calculated using bootstrapping
</center>

## Beyond the AUC ##

[Figure 1.](#auc_plot) 

### Net Reclassification Index (NRI) ###

### Integrate Discrimination Index (IDI)

<br>
