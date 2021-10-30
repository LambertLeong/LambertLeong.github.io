---
layout: post
cover: assets/images/essays/auc_idi_nri/idi_example.png
title: Hashing Out the Differences
date: 2021-10-20
categories: thoughts
author: Lambert
published: false
featured: false
permalink: thoughts/hashing-duplicate-data
comments: true
summary: TODO
description: TODO
labels:
  - Hashing
tags: Hashing
---
## Contents ##
* [More Data More Problems](#data-duplicates)
* [What is Hashing](#hashing)
* [Use Case](#example)
* [Speed Test](#speed-test)
* [Limitations](#Limitations)
* [Near Match Near Neighbor](#nearest-neighbor)

---

## TLDR ##
* TODO 

---

### More Data More Problems <a name="data-duplicates"></a> ###

TODO
machine learning, AI, big data
### What is Hashing <a name="hashing"></a> ###

TODO
benefits, no need a nn or gpu

#### Example <a name="example"></a>  ####
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
TODO

### Speed Test <a name="speed-test"></a> ###

TODO


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
 
<a name="ref-leong" href="https://www.nature.com/articles/s43856-021-00024-0" target="_blank">[6]</a> Leong, L., Malkov, S., Drukker, K., Niell, B., Sadowski, P., Wolfgruber, T., ... & Shepherd, J., Dual-energy three
  compartment breast imaging (3CB) for novel compositional biomarkers to improve detection of malignant lesions, (2021).
  
  
