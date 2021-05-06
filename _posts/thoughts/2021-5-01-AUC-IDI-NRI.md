---
layout: post
cover: assets/images/essays/auc_idi_nri/sunset_girl.jpg
title:  Area Under the Curve and Beyond
date: 2021-05-01
categories: thoughts
author: Lambert
published: true
featured: true
permalink: thoughts/AUC-IDI-NRI
comments: true
summary: Doctors and data scientist, here is an intro to IDI and NRI with a Python coded example. AUCs may not always be enough and this post allows you to go beyond the curve
description: Doctors and data scientist, here is an intro to IDI and NRI with a Python coded example. AUCs may not always be enough and this post allows you to go beyond the curve
labels:
  - AUC
  - IDI
  - NRI
  - Python
  - Data Science
  - area under the curve
  - ROC
  - Integrated discrimination improvement
  - net reclassification index
  - breast cancer
tags: AUC IDI NRI Python Data Science area under the curve ROC Integrated discrimination improvement net reclassification index breast cancer
---
## Contents ##
* [AUC](#head-auc)
* [Breast Cacner Example](#head-bc)
* [Issues with AUC](#head-issue)
* [Beyond the Curve](#head-beyond)
* [NRI](#head-nri)
* [IDI](#head-idi)
* [Final Thoughts](#head-final)

---

## TLDR ##
* **AUC** is a good starting metric when comparing the performance of two models but it does not always tell the who story 
* **NRI** looks at the new models ability to correctly reclassify event and nonevents and should be used alongside AUC
* **IDI** quantifies improvement of discrimination curve slopes and plotting it can provide information AUC alone does not afford.
* [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4741253.svg)](https://doi.org/10.5281/zenodo.4741253){:target="_blank"}

---

### Area Under the Curve (AUC) <a name="head-auc"></a> ###

In machine learning and diagnostic medicine the area under the receiver operating characteristic (ROC) curve or AUC
is a common metric used to evaluate the predictive performance of a model or diagnostic test. New models are often 
bench marked, using AUCs, against established models. Comparing AUCs of new and old models to evaluate  improvement is a
 good place to start however, many end their analysis here and believe simply reporting a higher AUC is 
sufficient. AUC can be misleading as it gives equal weight to the full range of sensitivity and specificity values even 
though a limited range, or specific threshold, may be of practical interest. In this article, we show how to fully 
interigate new and improved model performance, beyond simple AUC comparisons, as to provide a more comprehensive 
understanding of improvements within the context of a given problem. We also present a coded example in Python to
 demonstrate the concepts we present.

### Example: Breast Cancer <a name="head-bc"></a> ###

Code for the following example can be found at [github](https://github.com/LambertLeong/AUC_NRI_IDI_python_functions). 

Breast cancer is the leading cause of cancer death in women world wide. Early detection has helped to lower the mortality
rate and the earlier a malignancy is identified, the more likely a patient is to survive.  As such, great effort has
been allocated to developing predictive models to identify cancer.  In this example we use extracted imaging features
to build models to predict malignancy probability. We use data from the 
[Diagnostic Wisconsin Breast Cancer Database](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)){:target="_blank"}
[[1](#ref-uci)] housed at the UCI Machine Learning Repository.

As mentioned previously, AUC gives equal weight to all thresholds but this may not be practical in the context of 
breast cancer diagnosis. The
 [Breast Imaging Reporting and Data System or (BI-RADS)](https://www.cancer.org/cancer/breast-cancer/screening-tests-and-early-detection/mammograms/understanding-your-mammogram-report.html){:target="_blank"} 
 [[2](#ref-birads)].
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
#### Issues with Comparing Models AUCs <a name="head-issue"></a> ###
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
We run the following to generate AUC plots.
```python:
plot_auc(y_test.values,test_ref_pred[:,1],test_new_pred[:,1],n_bootstraps=100)
```
<center>
    <a name="auc_plot"></a>
  <img src="/assets/images/essays/auc_idi_nri/auc_ci_example.png" width="70%" alt="breast models AUC with confidence intervals">
<br>
  	Figure 1: AUC curves with confidence intervals calculated using bootstrapping
</center>
<br>

Mean curves and the 95% confidence interval in [Figure 1.](#auc_plot) were calculated via 100 rounds of bootstrapping, see code above. The reference (blue curve)
and new model (orange curve) produce similar AUC at 0.99 and 0.99, respectively. The confidence interval is slightly narrower
for the new model. Overall, it is difficult to draw any meaningful conclusion from these AUC curves and it would appear
that the new model with additional features did little to nothing to model malignancy predictions.

## Beyond the Area Under the Curve <a name="head-beyond"></a> ##

We present two additional metrics which are commonly used to asses the impact of new features or biomarkers on a model.
These metrics include the net reclassification index (NRI) and the integrated discrimination improvement (IDI) [[3](#ref-pencina)]. These 
two metrics will help in understanding the actual differences in the two models that may not be obvious in [Figure 1.](#auc_plot)

### Net Reclassification Index (NRI) <a name="head-nri"></a> ###

The NRI is derived by summing the number of NRI<sub>events</sub> and NRI<sub>nonevents</sub>.  In our example, events
 are synonymous to patients with cancer or maligancies and NRI<sub>nonevents</sub> are synonymous to patients who
 do have benign findings. The NRI<sub>events</sub> is the net proportion of patients with events reassigned to a higher 
 risk category and the NRI<sub>nonevents</sub> is the number of patients without events reassigned to a lower risk category [[4](#ref-pencina2)].
 We compute the NRI using the following Python functions.
 
 ```python:
def check_cat(prob,thresholds):
    cat=0
    for i,v in enumerate(thresholds):
        if prob>v:
            cat=i
    return cat

def make_cat_matrix(ref, new, indices, thresholds):
    num_cats=len(thresholds)
    mat=np.zeros((num_cats,num_cats))
    for i in indices:
        row,col=check_cat(ref[i],thresholds),check_cat(new[i],thresholds)
        mat[row,col]+=1
    return mat
        
def nri(y_truth,y_ref, y_new,risk_thresholds):
    event_index = np.where(y_truth==1)[0]
    nonevent_index = np.where(y_truth==0)[0]
    event_mat=make_cat_matrix(y_ref,y_new,event_index,risk_thresholds)
    nonevent_mat=make_cat_matrix(y_ref,y_new,nonevent_index,risk_thresholds)
    events_up, events_down = event_mat[0,1:].sum()+event_mat[1,2:].sum()+event_mat[2,3:].sum(),event_mat[1,:1].sum()+event_mat[2,:2].sum()+event_mat[3,:3].sum()
    nonevents_up, nonevents_down = nonevent_mat[0,1:].sum()+nonevent_mat[1,2:].sum()+nonevent_mat[2,3:].sum(),nonevent_mat[1,:1].sum()+nonevent_mat[2,:2].sum()+nonevent_mat[3,:3].sum()
    nri_events = (events_up/len(event_index))-(events_down/len(event_index))
    nri_nonevents = (nonevents_down/len(nonevent_index))-(nonevents_up/len(nonevent_index))
    return nri_events, nri_nonevents, nri_events + nri_nonevents 
 ```

We input both the reference and new models predictions into the NRI function to calculate the events, nonevents, and total NRI.

```python:
print(nri(y_test.values,test_ref_pred[:,1],test_new_pred[:,1],[0.02,0.1,0.5,0.95]))
```
The output from the code above is:
 ```$bash:
0.1642857142857143, 0.125, 0.2892857142857143 
```

It is tempting to state that "the new model reclassified 29% of the patients when compared to the reference model" however,
this would not be an accurate statement nor interpretation of NRI.  Since the NRI is the sum of the proportion of events 
and not events it is possible to have an NRI of 2 or 200%. A more correct interpretation would be to state that the new 
model correctly classified 16% more cancer cases and 13% more benigns when compared to the reference.

The NRI show us that adding more features to the new model reclassified both malignant and non-malignant patients.  This
information could not be concluded alone and may have incorrectly led people to think the models were the same. In a clinical
setting, the new model would have found more cancers which could potentially save more lives. Also, finding more benigns
would translate to less stress for an individual and potentially sparing them from having and invasive procedure like a biopsy.

Category free or cfNRI is a newer metric and tracks overall movement of event and nonevents, irrespective of class.
For our breast cancer example, the American College of Radiology (ACR) has distinct BI-RADS classes and therefore do not
find the need to calculate the cfNRI. We provide coded functions to calculate cfNRIs below in the instance that a may
server you problem.

```python:
def track_movement(ref,new, indices):
    up, down = 0,0
    for i in indices:
        ref_val, new_val = ref[i],new[i]
        if ref_val<new_val:
            up+=1
        elif ref_val>new_val:
            down+=1
    return up, down

def category_free_nri(y_truth,y_ref, y_new):
    event_index = np.where(y_truth==1)[0]
    nonevent_index = np.where(y_truth==0)[0]
    events_up, events_down = track_movement(y_ref, y_new,event_index)
    nonevents_up, nonevents_down = track_movement(y_ref, y_new,nonevent_index)
    nri_events = (events_up/len(event_index))-(events_down/len(event_index))
    nri_nonevents = (nonevents_down/len(nonevent_index))-(nonevents_up/len(nonevent_index))
    #print(events_up, events_down, len(event_index), nonevents_up, nonevents_down, len(nonevent_index), nri_events, nri_nonevents, nri_events+nri_nonevents)
    return nri_events, nri_nonevents, nri_events + nri_nonevents 
```    

### Integrate Discrimination Index (IDI) <a name="head-idi"></a> ###

The IDI is a measure in the change of the discrimination slopes and shows the impact of new biomarkers on a binary predictive
model.  The IDI is the sum of the integrated sensitivity (IS) and integrated specificity (IP) and like NRI, it separates
out events and nonevents or in this case cancers and benigns. We use the following code to calculate and plot the IDI curves [[5](#ref-pickering)].

```python:
def area_between_curves(y1,y2):
    diff = y1 - y2 # calculate difference
    posPart = np.maximum(diff, 0) 
    negPart = -np.minimum(diff, 0) 
    posArea = np.trapz(posPart)
    negArea = np.trapz(negPart)
    return posArea,negArea,posArea-negArea

def plot_idi(y_truth, ref_model, new_model, save=False): 
    ref_fpr, ref_tpr, ref_thresholds = metrics.roc_curve(y_truth, ref_model)
    new_fpr, new_tpr, new_thresholds = metrics.roc_curve(y_truth, new_model)
    base, mean_tprs, mean_fprs=bootstrap_results( y_truth, new_model,100)
    base2, mean_tprs2, mean_fprs2=bootstrap_results( y_truth, ref_model,100)
    is_pos,is_neg, idi_event=area_between_curves(mean_tprs,mean_tprs2)
    ip_pos,ip_neg, idi_nonevent=area_between_curves(mean_fprs2,mean_fprs)
    print('IS positive', round(is_pos,2),'IS negative',round(is_neg,2),'IDI events',round(idi_event,2))
    print('IP positive', round(ip_pos,2),'IP negative',round(ip_neg,2),'IDI nonevents',round(idi_nonevent,2))
    print('IDI =',round(idi_event+idi_nonevent,2))
    plt.figure(figsize=(10, 10))
    ax=plt.axes()
    lw = 2
    plt.plot(base, mean_tprs, 'black', alpha = 0.5, label='Events New (New)' )
    plt.plot(base, mean_fprs, 'red', alpha = 0.5, label='Nonevents New (New)')
    plt.plot(base2, mean_tprs2, 'black', alpha = 0.7, linestyle='--',label='Events Reference (Ref)' )
    plt.plot(base2, mean_fprs2, 'red', alpha = 0.7,  linestyle='--', label='Nonevents Reference (Ref)')
    plt.fill_between(base, mean_tprs,mean_tprs2, color='black',alpha = 0.1, label='Integrated Sensitivity (area = %0.2f)'%idi_event)
    plt.fill_between(base, mean_fprs,mean_fprs2, color='red', alpha = 0.1, label='Integrated Specificity (area = %0.2f)'%idi_nonevent)
    
    #''' #TODO: comment out if not for breast birads
    ### BIRADS Thresholds ###
    plt.axvline(x=0.02,color='darkorange',linestyle='--',alpha=.5,label='BI-RADS 3/4a Border (2%)')
    plt.axvline(x=0.10,color='green',linestyle='--',alpha=.5,label='BI-RADS 4a/4b Border (10%)')
    plt.axvline(x=0.5,color='blue',linestyle='--',alpha=.5,label='BI-RADS 4b/4c Border (50%)')
    plt.axvline(x=0.95,color='purple',linestyle='--',alpha=.5,label='BI-RADS 4c/5 Border (95%)')
    def nri_annotation(plt, threshold):
        x_pos = base[threshold]
        x_offset=0.02
        x_offset2=x_offset
        text_y_offset=0.01
        text_y_offset2=text_y_offset
        if threshold==2:
            text_y_offset=0.04
            text_y_offset2=0.04
            x_offset2=0.05
            print(x_pos+x_offset, (np.mean([mean_tprs2[threshold], mean_tprs[threshold]])+text_y_offset),
                    x_pos, (np.mean([mean_tprs2[threshold], mean_tprs[threshold]])))
        text_y_events=np.mean([mean_tprs2[threshold], mean_tprs[threshold]])+text_y_offset
        text_y_nonevents=np.mean([mean_fprs[threshold], mean_fprs2[threshold]])+text_y_offset2
        plt.annotate('', xy=(x_pos+0.02, mean_tprs2[threshold+1]), xycoords='data', xytext=(x_pos+0.02, 
                            mean_tprs[threshold]), textcoords='data', arrowprops={'arrowstyle': '|-|'})
        plt.annotate('NRI$_{events}$ = %0.2f'%(mean_tprs[threshold]-mean_tprs2[threshold]), 
                     xy=(x_pos+x_offset, text_y_events), xycoords='data',
                     xytext=(x_pos+x_offset, text_y_events),
                     textcoords='offset points', fontsize=15)
        plt.annotate('', xy=(x_pos+0.02, mean_fprs[threshold]), xycoords='data', xytext=(x_pos+0.02, 
                             mean_fprs2[threshold]), textcoords='data', arrowprops=dict(arrowstyle= '|-|',color='r'))
        plt.annotate('NRI$_{nonevents}$ = %0.2f'%(mean_fprs2[threshold]-mean_fprs[threshold]), 
                     xy=(x_pos+x_offset2, text_y_nonevents), xycoords='data',
                     xytext=(x_pos+x_offset2, text_y_nonevents), 
                     textcoords='offset points', fontsize=15)
        print('Threshold =',round(x_pos,2),'NRI events =',round(mean_tprs[threshold]-mean_tprs2[threshold],4),
              'NRI nonevents =',round(mean_fprs2[threshold]-mean_fprs[threshold],4),'Total =',
              round((mean_tprs[threshold]-mean_tprs2[threshold])+(mean_fprs2[threshold]-mean_fprs[threshold]),4))
    nri_annotation(plt,2)
    nri_annotation(plt,10)
    nri_annotation(plt,50)
    nri_annotation(plt,95)
    #'''
    plt.xlim([0.0, 1.10])
    plt.ylim([0.0, 1.10])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Calculated Risk', fontsize=18)
    plt.ylabel('Sensitivity (black), 1 - Specificity (red)', fontsize=18)
    plt.legend(loc="upper right", fontsize=11)
    plt.legend(loc=0, fontsize=11,  bbox_to_anchor=(0,0,1.2,.9))
    plt.gca().set_aspect('equal', adjustable='box')
    #if save:
    #    plt.savefig('idi_curve.png',dpi=300, bbox_inches='tight')
    look=95
    plt.show()
```
We run the following command to generate the graph in [Figure 2.](#idi_plot)
```python:
plot_idi(y_test.values,test_ref_pred[:,1],test_new_pred[:,1])
```
Output:
```$bash
IS positive 3.58 IS negative 0.16 IDI events 3.42
IP positive 4.61 IP negative 0.04 IDI nonevents 4.57
IDI = 7.98
0.04 1.04 0.02 1.0
Threshold = 0.02 NRI events = 0.0 NRI nonevents = 0.2762 Total = 0.2762
Threshold = 0.1 NRI events = -0.008 NRI nonevents = 0.1002 Total = 0.0922
Threshold = 0.5 NRI events = 0.0215 NRI nonevents = 0.0317 Total = 0.0532
Threshold = 0.95 NRI events = 0.1389 NRI nonevents = -0.0136 Total = 0.1252
```

<center>
    <a name="idi_plot"></a>
  <img src="/assets/images/essays/auc_idi_nri/idi_example.png" width="90%" alt="Integrated Discrimination Improvement (IDI) index python plots">
<br>
  	Figure 2: IDI curve with calculated NRI at each class or BI-RADS border
</center>
<br>
The dashed and solid curves represent the reference and new model respectively. In the ideal case, the solid black line would
be moved to the upper right indicating the most improvement to sensitivity and the red line would be lowered to the bottom
right indicating the most improved specificity.  The area between the black and red curves equate to the IS and IP and the total
sum of the black and red area equates to the IDI. IDI provides more information that the AUC curves especially with respects to the 
orange dashed vertical line or the BI-RADS 3/4a border. At this border, the IS or red area is large which indicates that the 
new model was able to better predict benigns. This border is particularly interesting because it is recommended that all
patients with BI-RADS 4 or greater receive biopsies [[6](#ref-leong)]. The large area at the 3/4a border shows that adding new features to the new 
model increase specificity and potentially prevented 28% more people (NRI<sub>nonevents</sub>=0.28) from being unnecessarily biopsied.  

## Final Thoughts <a name="head-final"></a> ##
AUC is a good metric but does not provide all the information needed for a comprehensive analysis of the impact of new biomarkers and
models.  The NRI and IDI should be used to complement AUC findings and interpretations. As a data scientist and cancer
researcher who uses Python, it was difficult to find functions and code snippets that computed and plotted NRI and IDI.
This was my motivation for posting this and I hope that my code can help other in their research, discoveries, and pursuit of 
better health care solutions. 

### References ###

<a name="ref-uci" href="https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)" target="_blank">[1]</a> 
Dua, D. and Graff, C, (2019), Irvine, CA: University of California, School of Information and Computer Science, UCI Machine Learning Repository [http://archive.ics.uci.edu/ml].

<a name="ref-birads" href="https://www.cancer.org/cancer/breast-cancer/screening-tests-and-early-detection/mammograms/understanding-your-mammogram-report.html" target="_blank">[2]</a> 
Understanding mammogram reports: Mammogram results. (n.d.). Retrieved May 06, 2021, from https://www.cancer.org/cancer/breast-cancer/screening-tests-and-early-detection/mammograms/understanding-your-mammogram-report.html

<a name="ref-pencina" href="https://onlinelibrary.wiley.com/doi/abs/10.1002/sim.2929" target="_blank">[3]</a> Pencina, M. J., D'Agostino Sr, R. B., D'Agostino Jr, R. B., & Vasan, R. S., Evaluating the added
 predictive ability of a new marker: from area under the ROC curve to reclassification and beyond, 
 (2008), Statistics in medicine, 27(2), 157-172.

<a name="ref-pencina2" href="https://onlinelibrary.wiley.com/doi/abs/10.1002/sim.4085" target="_blank">[4]</a> Pencina, M. J., D'Agostino Sr, R. B., & Steyerberg, E. W., Extensions of net reclassification improvement 
calculations to measure usefulness of new biomarkers, (2011), Statistics in medicine, 30(1), 11-21.

<a name="ref-pickering" href="https://cjasn.asnjournals.org/content/7/8/1355" target="_blank">[5]</a> Pickering, J. W., & Endre, Z. H., New metrics for assessing diagnostic potential of candidate biomarkers,
 (2012), Clinical Journal of the American Society of Nephrology, 7(8), 1355-1364.
 
<a name="ref-leong" href="https://www.researchsquare.com/article/rs-292446/v1" target="_blank">[6]</a> Leong, L., Malkov, S., Drukker, K., Niell, B., Sadowski, P., Wolfgruber, T., ... & Shepherd, J., Dual-energy three
  compartment breast imaging (3CB) for novel compositional biomarkers to improve detection of malignant lesions, (2021).
  
  