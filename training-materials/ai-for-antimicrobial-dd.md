---
description: Introductory 2h workshop to AI/ML tools for antimicrobial drug discovery
---

# AI for Antimicrobial DD

## Introduction

There is a plethora of AI/ML tools geared towards accelerating drug discovery. In this 2h problem-solving oriented activity, the participants will have the opportunity to understand the fundamental steps to couple AI/ML expertise into their pipelines, in a fully no-code manner!

<figure><img src="../.gitbook/assets/Screenshot 2024-05-21 at 05.28.34.png" alt=""><figcaption><p>AI/ML can be applied to all stages of the drug discovery pipeline</p></figcaption></figure>

## Materials

You will find all the materials needed in the following links:

* Workshop App
* Publications
* Guidance Document
* Presentation

## Hands-on activity

The participant is presented with the following problem statement:

> We are a laboratory specialised in antimicrobial research. We have received a library of compounds from a collaborator and we need to explore it and identify the best candidates.&#x20;

Some of the considerations to take into account:

* We can synthesise compounds but our throughput is 50 compounds per month
* We have a tight timeline (2 months) to provide the results
* Our collaborators are keen on exploring analogues of the molecules in their library as well
* The selected compounds need to meet the following criteria:&#x20;
  * Synthetically accessible in the laboratory&#x20;
  * Good ADME profile&#x20;
  * High activity against at least one pathogen in the WHO priority list

{% hint style="info" %}
Use the demo platform to filter out candidates and propose new molecules for experimental testing!
{% endhint %}

### Step 1: Train a bioactivity predictor

We will use a dataset presented in [Liu et al, 2023](https://pubmed.ncbi.nlm.nih.gov/37231267/) to train a simple QSAR model predicting bioactivity of small molecules against _A.baumannii,_ one of the WHO priority pathogens.&#x20;

&#x20;We are automatically performing a 5-fold cross-validation at model training time by dividing our dataset into train-test splits (80-20).

Try to answer the following questions:

* What is the experimental assay measuring?
* Are we training a classification or regression model with this data?
* What is the author's defined activity cut-off?
* What have we chosen as a cut-off for activity against _A.baumannii_?
* Is it a balanced dataset? Why or why not?
* What is the performance of the models at different cut-offs?
* How does our quick modelling compare to the author's work?

### Step 2: Rank candidates

Using the model we have just trained as well as auxiliary models available in the Ersilia Model Hub, rank and select a few candidates to proceed to the next steps.

In addition to the bioactivity predictor, we will use the Synthetic Accessibility (Ertl et al, 2009) and hERG cardiotoxicity (Jiménez-Luna et al, 2021).

Try to answer the following questions for each model:

* What type of model is it?
* What type of output does the model produce?
* What is a good threshold for keeping molecules?

### Step 3: Generate new candidates

Using the selected molecule in Step 2, play with the molecule generator implemented in the demo app. This is based on the MolMIM package ([Reidenbach et al, 2022](https://arxiv.org/abs/2208.09016)). MolMIM offers automated molecular generation optimising either for chemical beauty (QED) or SlogP.

Try to answer the following questions:

* Are there new chemical structures in the generated candidates?
* Do the generated candidates present better predicted biochemical profiles?
* What would your next steps be?

## Glossary of Terms:

Artificial intelligence (AI): An overarching term that refers to software that mimics human reasoning.

Machine learning (ML): A subset of AI that employs various statistical methods and computational algorithms to analyse patterns from datasets and to provide meaningful insights and predictions.

Classification model: A ML model that predicts probability that a molecule belongs to a certain class, i.e. the ‘1’ (active) class or ‘0’ (inactive) class.

Activity cut-off: The experimental value used to classify compounds into ‘active’ and ‘inactive’ categories.

Prediction interpretation: The output of a classification model is typically a prediction probability, between 0 and 1, that the compound belongs to the ‘1’ (active) class. The closer the prediction probability is to 1, the more confident the model is that the compound belongs to the ‘1’ (active) class.

Prediction threshold: The cut-off applied to the model prediction scores to binarize the compounds into predicted actives and predicted inactives.

AUROC/ROC-AUC: The area under the receiver-operating characteristic curve. The ROC curve is constructed through a comparison of model predictions to the ground-truth values by plotting the true-positive rate versus the false-positive rate. The area under the ROC curve is a metric of model predictive performance typically between 0.5 (random classifier) and 1.0 (perfect classifier).

Regression model: A ML model that predicts the exact continuous experimental output, e.g. the specific molar solubility of a compound.

Large-language model (LLM): A model that has been trained on a large corpus of textual data to interpret plain text prompts and respond appropriately.

Generative models: AI methods that synthesise new outputs often in response to a prompt. For example, these can take the form of chemical generators that propose new compounds or large-language models.

IC50: The half maximal inhibitory concentration measures the drug concentration at which 50% of a biological process is inhibited.

pIC50: The negative log transformation of IC50 ‘-log(IC50)’ scales a dataset to a more linear range of values, which is more amenable to ML modelling.

MIC50: The minimum inhibitory concentration is the lowest drug concentration that visibly inhibits at least 50% of microbial growth. This is a less precise measurement than IC50 and is typically used in the serial dilution assays for in vitro whole-cell activity measurements.

Synthetic accessibility: An estimated score that captures the difficulty in synthesising a compound.

Chemical analogue: A compound that shares the majority of chemical features to another compound, particularly the core, with only small structural modifications.

Chemical space: The ensemble of all possible chemical structures.\
