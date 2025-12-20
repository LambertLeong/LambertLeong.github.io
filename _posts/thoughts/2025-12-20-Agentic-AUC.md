---
layout: post
cover: assets/images/essays/agent-auc/agentic_auc_cover2.png
title: Agents Under the Curve (AUC)
date: 2025-12-20
categories: thoughts
author: Lambert
published: true
featured: true
permalink: thoughts/agentic-AUC
comments: true
summary: Agentic AI systems are on the rise in healthcare, but most only output binary decisions. This post provides options to turn those decisions into continuous scores so we can still use AUC for fair model comparison.
description: Agentic AI systems are entering medical risk and detection pipelines, yet they usually output hard decisions instead of probabilities. Since AUC is still the standard metric for comparing models in medicine, we need practical ways to derive continuous scores from agentic workflows. This post walks through why AUC needs continuous values, how that clashes with binary agent outputs, and presents several concrete strategies for producing an AUC for agentic models.
labels:
  - AUC
  - ROC
  - agentic AI
  - medical AI
  - risk prediction
  - area under the curve
  - model evaluation
  - disease risk
  - binary classification
tags: AUC ROC agentic\ AI medical\ AI risk\ prediction area\ under\ the\ curve model\ evaluation disease\ risk binary\ classification
---

## TLDR ##
* Agentic AI systems in healthcare often output binary decisions such as disease or no disease, which by themselves cannot produce a meaningful AUC.  
* AUC is still the standard way to compare risk and detection models in medicine, and it requires continuous scores that let us rank patients by risk.  
* This post describes several practical strategies for converting agentic outputs into continuous scores so that AUC based comparisons with traditional models remain valid and fair.

---

## Contents ##
* [Agent and Area Under the Curve Disconnect](#head-intro)
* [Why AUC Matters and Why Binary Outputs Fail](#head-whyauc)
* [Comparison Table](#head-table)
* [Methods To Derive Continuous Scores](#head-methods)
* [Final Thoughts](#head-final)
* [More Relevant Resources](#resources)

---

## Agent and Area Under the Curve Disconnect <a name="head-intro"></a> ##

Agentic AI systems are becoming increasingly common as they lower the barrier to entry for AI solutions. They accomplish this by leveraging foundational models so that resources do not always need to be spent on training a custom model from the ground up or on multiple rounds of fine-tuning.

I noticed that roughly 20 - 25% of the papers at NeurIPS 2025 were focused on agentic solutions. Agents for medical applications are rising in parallel and gaining popularity. These systems include LLM driven pipelines, retrieval augmented agents, and multi step decision frameworks. They can synthesize heterogeneous data, reason step-by-step, and produce contextual recommendations or decisions.

Most of these systems are built to answer questions like “Does this patient have the disease” or “Should we order this test” instead of “What is the probability that this patient has the disease.” In other words, they tend to produce hard decisions and explanations, not calibrated probabilities.

In contrast, traditional medical risk and detection models are usually evaluated with the area under the receiver operating characteristic curve or AUC. AUC is deeply embedded in clinical prediction work and is the default metric for comparing models in many imaging, risk, and screening studies.

This creates a gap. If our new models are agentic and decision focused, but our evaluation standards are probability based, we need methods that connect the two. The rest of this post focuses on what AUC actually needs, why binary outputs are not enough, and how to derive continuous scores from agentic frameworks so that AUC remains usable.

---

## Why AUC Matters and Why Binary Outputs Fail <a name="head-whyauc"></a> ##

AUC is often considered the gold standard metric in medical applications because it handles the imbalance between cases and controls better than simple accuracy, especially in datasets that reflect real world prevalence.

Accuracy can be a misleading metric when disease prevalence is low. For example, breast cancer prevalence in a screening population is roughly 5 in 1000. A model that predicts “no cancer” for every case would still have very high accuracy, but the false negative rate would be unacceptably high. In a real clinical context, this is clearly a bad model, despite its accuracy.

AUC measures how well a model separates positive cases from negative cases. It does this by looking at a continuous score for each individual and asking how well these scores rank positives above negatives. This ranking based view is why AUC remains useful even when classes are highly imbalanced.

While I noticed great innovative work at the intersection of agents and health at NeurIPS, I did not see many papers that reported an AUC. I also did not see many that compared a new agentic approach to an existing or established conventional machine learning or deep learning model using standard metrics. Without this, it is difficult to calibrate and understand how much better these agentic solutions actually are, if at all.

Most current agentic outputs do not lend themselves naturally to obtaining AUCs. With this article, the goal is to propose methods to obtain AUC for agentic systems so that we can start a concrete conversation about performance gains compared to previous and existing solutions.

#### How AUC is computed ####

To fully understand the gap and appreciate attempts at a solution, we should review how AUCs are calculated.

Let

<ul>
  <li><i>y</i> &in; {0, 1} be the true label</li>
  <li><i>s</i> &in; &#8477; be the model score for each individual</li>
</ul>

The ROC curve is built by sweeping a threshold <i>t</i> across the full range of scores and computing

- Sensitivity at each threshold  
- Specificity at each threshold  

AUC can then be interpreted as

> The probability that a randomly selected positive case has a higher score than a randomly selected negative case.

This interpretation only makes sense if the scores contain enough granularity to induce a ranking across individuals. In practice, that means we need continuous or at least finely ordered values, not just zeros and ones.

#### Why binary agentic outputs break AUC ####

Agentic systems often output only a binary decision. For example:

- “disease” mapped to 1  
- “no disease” mapped to 0  

If these are the only possible outputs, then there are only two unique scores. When we sweep thresholds over this set, the ROC curve collapses to at most one nontrivial point plus the trivial endpoints. There is no rich set of thresholds and no meaningful ranking.

In this case, the AUC becomes either undefined or degenerate. It also cannot be fairly compared to AUC values from traditional models that output continuous probabilities.

<div style="text-align: center;">
  <a name="img-auc-collapse"></a>
  <img src="/assets/images/essays/agent-auc/degenerate_roc_watermarked.png" style="width: 69%;" alt="Diagram showing how binary outputs collapse the ROC curve compared to continuous scores">
  <br>
  <span style="font-style: italic; font-size: 0.9em;">Figure 1: Visualizing why binary outputs lead to ROC curve issues.</span>
</div>
<br>

To evaluate agentic solutions using AUC, we must create a continuous score that captures how strongly the agent believes that a case is positive.

#### What we need ####

To compute an AUC for an agentic system, we need a continuous score that reflects its underlying risk assessment, confidence, or ranking. The score does not have to be a perfectly calibrated probability. It only needs to provide an ordering across patients that is consistent with the agent’s internal notion of risk.

Below is a list of practical strategies for transforming agentic outputs into such scores.

---

## Methods To Derive Continuous Scores From Agentic Systems <a name="head-methods"></a> ##

1. Extract internal model log probabilities.  
2. Ask the agent to output an explicit probability.  
3. Use Monte Carlo repeated sampling to estimate a probability.  
4. Convert retrieval similarity scores into risk scores.  
5. Train a calibration model on top of agent outputs.  
6. Sweep a tunable threshold or configuration inside the agent to approximate an ROC curve.

### Comparison Table <a name="head-table"></a>

<style>
.comparison-table {
  overflow-x: auto;
  margin: 2rem 0;
}
.comparison-table table {
  width: 100%;
  border-collapse: collapse;
}
.comparison-table th,
.comparison-table td {
  padding: 12px;
  text-align: left;
  border: 1px solid #ddd;
  vertical-align: top;
}
.comparison-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}
</style>

<div class="comparison-table">
<table>
<thead>
<tr>
<th>Method</th>
<th>Pros</th>
<th>Cons</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Log probabilities</strong></td>
<td>Continuous, stable signal that aligns with model reasoning and ranking</td>
<td>Requires access to logits and can be sensitive to prompt format</td>
</tr>
<tr>
<td><strong>Explicit probability output</strong></td>
<td>Simple, intuitive, and easy to communicate to clinicians and reviewers</td>
<td>Calibration quality depends on prompting and model behavior</td>
</tr>
<tr>
<td><strong>Monte Carlo sampling</strong></td>
<td>Captures the agent's true decision uncertainty without internal access</td>
<td>Computationally more expensive and requires multiple runs per patient</td>
</tr>
<tr>
<td><strong>Retrieval similarity</strong></td>
<td>Ideal for retrieval-based systems and straightforward to compute</td>
<td>May not fully reflect downstream decision logic or overall reasoning</td>
</tr>
<tr>
<td><strong>Calibration model</strong></td>
<td>Converts structured or categorical outputs into smooth risk scores and can improve calibration</td>
<td>Requires labeled data and adds a secondary model to the pipeline</td>
</tr>
<tr>
<td><strong>Threshold sweeping</strong></td>
<td>Works even when the agent only exposes binary outputs and a tunable parameter</td>
<td>Produces an approximate AUC that depends on how the parameter affects decisions</td>
</tr>
</tbody>
</table>
</div>


In the next section, each method is described in more detail, including why it works, when it is most appropriate, and what limitations to keep in mind.

---

### Method 1. Extract internal model log probabilities <a name="head-m1"></a> ###

#### Concept ####

Many agentic systems rely on a large language model or other differentiable model internally. During decoding, these models compute token level log probabilities. Even if the final output is a binary label, the model still evaluates how likely each option is.

If the agent decides between “disease” and “no disease” as its final outcome, we can extract:

<ul>
  <li>log <i>p</i>(disease)</li>
  <li>log <i>p</i>(no disease)</li>
</ul>

and define a continuous score such as:

<div style="text-align: center; margin: 1em 0;">
  <i>s</i> = log <i>p</i>(disease) &minus; log <i>p</i>(no disease)
</div>

This score is higher when the model favors the disease label and lower when it favors the no disease label.

#### Why this works ####

- Log probabilities are continuous and provide a smooth ranking signal.  
- They directly encode the model’s preference between outcomes.  
- They are a natural fit for ROC analysis, since AUC only needs ranking, not perfect calibration.

#### Best for ####

- Agentic frameworks that are clearly LLM based.  
- Situations where you have access to token level log probabilities through the model or API.  
- Experiments where you care about precise ranking quality.

#### Caution ####

- Not all APIs expose log probabilities.  
- The values can be sensitive to prompt formatting and output template choices, so it is important to keep these consistent across patients and models.

---

### Method 2. Ask the agent to output a probability <a name="head-m2"></a> ###

#### Concept ####

If the agent already produces step by step reasoning, we can extend the final step to include an estimated probability. For example, you can instruct the system:

> After completing your reasoning, output a line of the form:  
> `risk_probability: <value between 0 and 1>`  
> that represents the probability that this patient has or will develop the disease.

The numeric value in this line becomes the continuous score.

#### Why this works ####

- It generates a direct continuous scalar output for each patient.  
- It does not require low level access to logits or internal layers.  
- It is easy to explain to clinicians, collaborators, or reviewers who expect a numeric probability.

#### Best for ####

- Evaluation pipelines where interpretability and communication are important.  
- Settings where you can modify prompts but not the underlying model internals.  
- Early stage experiments and prototypes.

#### Caution ####

- The returned probability may not be well calibrated without further adjustment.  
- Small prompt changes can shift the distribution of probabilities, so prompt design should be fixed before serious evaluation.

---

### Method 3. Use Monte Carlo repeated sampling <a name="head-m3"></a> ###

#### Concept ####

Many agentic systems use stochastic sampling when they reason, retrieve information, or generate text. This randomness can be exploited to estimate an empirical probability.

For each patient:

1. Run the agent on the same input N times.  
2. Count how many times it predicts disease.  
3. Define the score as

<div style="text-align: center; margin: 1em 0;">
  <i>s</i> = (number of disease predictions) / <i>N</i>
</div>

This frequency behaves like an estimated probability of disease according to the agent.

#### Why this works ####

- It turns discrete yes or no predictions into a continuous probability estimate.  
- It captures the agent’s internal uncertainty, as reflected in its sampling behavior.  
- It does not require log probabilities or special access to the model.

#### Best for ####

- Stochastic LLM agents that produce different outputs when you change the random seed or temperature.  
- Agentic pipelines that incorporate random choices in retrieval or planning.  
- Scenarios where you want a conceptually simple probability estimate.

#### Caution ####

- Running N repeated inferences per patient increases computation time.  
- The variance of the estimate decreases with N, so you need to choose N large enough for stability but small enough to stay efficient.

---

### Method 4. Convert retrieval similarity scores into risk scores <a name="head-m4"></a> ###

#### Concept ####

Retrieval augmented agents typically query a vector database of past patients, clinical notes, or imaging derived embeddings. The retrieval stage produces similarity scores between the current patient and stored exemplars.

If you have a set of high risk or positive exemplars, you can define a score such as

<div style="text-align: center; margin: 1em 0;">
  <i>s</i> = max<sub><i>j</i></sub> similarity(<i>x</i>, <i>e<sub>j</sub></i>)
</div>

where <i>e<sub>j</sub></i> indexes embeddings from known positive cases and similarity is something like cosine similarity.

The more similar the patient is to previously seen positive cases, the higher the score.

#### Why this works ####

- Similarity scores are naturally continuous and often well structured.  
- Retrieval quality tends to track disease patterns if the exemplar set is chosen carefully.  
- The scoring step exists even if the downstream agent logic makes only a binary decision.

#### Best for ####

- Retrieval-augmented-generation (RAG) agents.  
- Systems that are explicitly prototype based.  
- Situations where embedding and retrieval components are already well tuned.

#### Caution ####

- Retrieval similarity may capture only part of the reasoning that leads to the final decision.  
- Biases in the embedding space can distort the score distribution and should be monitored.

---

### Method 5. Train a calibration model on top of agent outputs <a name="head-m5"></a> ###

#### Concept ####

Some agentic systems output structured categories such as low, medium, or high risk, or generate explanations that follow a consistent template. These categorical or structured outputs can be converted to continuous scores using a small calibration model.

For example:

- Encode categories as features.  
- Optionally embed textual explanations into vectors.  
- Train logistic regression, isotonic regression, or another simple model to map those features to a risk probability.

The calibration model learns how to assign continuous scores based on how the agent’s outputs correlate with true labels.

#### Why this works ####

- It converts coarse or discrete outputs into smooth, usable scores.  
- It can improve calibration by aligning scores with observed outcome frequencies.  
- It is aligned with established practice, such as mapping BI-RADS categories to breast cancer risk.

#### Best for ####

- Agents that output risk categories, scores on an internal scale, or structured explanations.  
- Clinical workflows where calibrated probabilities are needed for decision support or shared decision making.  
- Settings where labeled outcome data is available for fitting the calibration model.

#### Caution ####

- This approach introduces a second model that must be documented and maintained.  
- It requires enough labeled data to train and validate the calibration step.

---

### Method 6. Sweep a tunable threshold or configuration inside the agent <a name="head-m6"></a> ###

#### Concept ####

Some agentic systems expose configuration parameters that control how aggressive or conservative they are. Examples include:

- A sensitivity or risk tolerance setting.  
- The number of retrieved documents.  
- The number of reasoning steps to perform before making a decision.  

If the agent remains strictly binary at each setting, you can treat the configuration parameter as a pseudo threshold:

1. Choose several parameter values that range from conservative to aggressive.  
2. For each value, run the agent on all patients and record sensitivity and specificity.  
3. Plot these operating points to form an approximate ROC curve.  
4. Compute the area under this curve as an approximate AUC.

#### Why this works ####

- It converts a rigid binary decision system into a collection of operating points.  
- The resulting curve can be interpreted similarly to a traditional ROC curve, although the x axis is controlled indirectly through the configuration parameter rather than a direct score threshold.  
- It is reminiscent of decision curve analysis, which also examines performance across a range of decision thresholds.

#### Best for ####

- Rule based or deterministic agents with tunable configuration parameters.  
- Systems where probabilities and logits are inaccessible.  
- Scenarios where you care about trade offs between sensitivity and specificity at different operating modes.

#### Caution ####

- The resulting AUC is approximate and based on parameter sweeps rather than direct score thresholds.  
- Interpretation depends on understanding how the parameter affects the underlying decision logic.

---

### Final Thoughts <a name="head-final"></a> ###

Agentic systems are becoming central to AI including medical use cases, but their tendency to output hard decisions conflicts with how we traditionally evaluate risk and detection models. AUC is still a standard reference point in many clinical and research settings, and AUC requires continuous scores that allow meaningful ranking of patients.

The methods in this post provide practical ways to bridge the gap. By extracting log probabilities, asking the agent for explicit probabilities, using repeated sampling, exploiting retrieval similarity, training a small calibration model, or sweeping configuration thresholds, we can construct continuous scores that respect the agent’s internal behavior and still support rigorous AUC based comparisons.

This keeps new agentic solutions grounded against established baselines and allows us to evaluate them using the same language and methods that clinicians, statisticians, and reviewers already understand. With an AUC, we can truly evaluate if the agentic system is adding value.

### Relevant Resources <a name="resources"></a> ###
- [Area Under the Curve and Beyond with Integrated Discrimination Improvement and Net Reclassification](https://www.lambertleong.com/thoughts/AUC-IDI-NRI)
- [Using AUC in Medicine with Deep Learning](https://www.lambertleong.com/projects/deep-learning-breast-cancer-risk)