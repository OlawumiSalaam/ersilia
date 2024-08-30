---
description: 4-day workshop on the use of AI for Drug Discovery
---

# AI2050 - AI for Drug Discovery

## Course overview

Each day is organised in four main activities:

* Keynote Lectures: a presentation by H3D and Ersilia mentors and invited speakers, introducing key concepts that we will put into practice during the day
* Skills Workshop: a hands-on training where the course facilitators will walk the participants through a specific ML exercise
* Breakout: participants will be divided in small groups to complete an exercise related to the skills workshop
* Group Discussion: each group will give a short (10 min) presentation on their breakout activity.

### Course Contents <a href="#course-contents" id="course-contents"></a>

| Activity           | Session 1                       | Session 2                      | Session 3                      | Session 4                      |
| ------------------ | ------------------------------- | ------------------------------ | ------------------------------ | ------------------------------ |
| Keynote            | Slides                          | Slides                         | Slides                         | Slides                         |
| Skills development | <p>App<br>Slides<br>Menti: </p> | <p>App<br>Slides<br>Menti:</p> | <p>App<br>Slides<br>Menti:</p> | <p>App<br>Slides<br>Menti:</p> |
| Breakout           | <p>App</p><p>Guide</p>          | <p>App</p><p>Guide</p>         | <p>App<br>Guide</p>            |                                |

## Important links

In case you need further information to follow the course, be sure to check the following:

* Ersilia Model Hub: list of all [available models](https://ersilia.io/model-hub)
* Ersilia Model Hub: [self-service](https://github.com/ersilia-os/ersilia-self-service) on GitHub (requires a GitHub account)
* Ersilia Model Hub: [local installation](../ersilia-model-hub/antibiotic-activity-prediction.md) documentation (only expert users)
* Publications referred to during the workshop

## Breakout Sessions

### Breakout session day 1



### Breakout session day 2

A virtual screening cascade allows us to mimic in the computer some of the experimental steps we must do to identify new drug leads. By filtering out molecules with predicted low activities, or undesired side effects, we can lower the cost and time to find new drug candidates. Ideally, we can build virtual screening cascades based off our own data, but for many assays we do not have readily available experimental data. In these situations, we can leverage models developed by third parties and apply them to our problem.

{% hint style="warning" %}
Virtual screening cascades are not meant to substitute experimental testing, but act as a decision-making support tool
{% endhint %}

#### A.baumannii activity prediction <a href="#mmv-malaria-box" id="mmv-malaria-box"></a>

In this activity, we will replicate the work described in Liu et al, 2023, where they build an ML model to identify novel _A.baumannii_ inhibitors and use it to filter the [Drug Repurposing Hub](https://www.broadinstitute.org/drug-repurposing-hub).&#x20;

During the skills development session, we have done a deep dive into ML model building using the _A.baumannii_ model as an example. Now, you have to download the list of compounds available in the Drug Repurposing Hub and continue the "virtual secreening" similar to the original author's work. To that end, we suggest running predictions against A.baumannii activity and a few accessory models available through Ersilia to select the best candidates. In short, the steps to follow are:

1. Download the Drug Repurposing Hub data from this link
2. Look at the Ersilia Model Hub models available online (select Online in the left menu of the website)
3. Select which models would be relevant to your exercise and why, and take notes on model interpretation, expected results, priority level etc.
4. Run predictions for the Drug Repurposing Hub molecules using the selected models.&#x20;
5. Select the best molecule candidates based on your defined filters of activity, ADME properties and other considerations

#### Models <a href="#models" id="models"></a>

In order to limit the exercise, please limit your screening to the following models:

* A.baumannii Activity: eos3804
* General Antibiotic Activity: eos4e40
* Cardiotoxicity (hERG): eos43at
* Synthetic Accessibility: eos9ei3
* ADME properties: eos7d58
* Natural Product Likeness: eos9yui

It is best to select only a few models but really understand how to use them rather than running predictions for all the models but not knowing how to interpret the outcomes.

For each model, think about the following questions:

* What type of model is it (classification or regression)?
* What is the training dataset? (refer to the original publication listed above)
* What is the interpretation of the model outcome?
* What cut-off, if any, we should use for that particular model?

In addition, think about the following concepts:

* Does the outcome of the model make sense? (i.e, malaria activity is predicted high for most molecules since it is a library optimized for malaria activity). If it does not make sense, perhaps we have the wrong interpretation of the model output
* Is the cut-off I have selected too stringent (i.e, I am losing too many molecules and I should be more permissive?)
* Is this model very relevant for the current dataset (i.e, is malaria activity equally important as natural product likeness?)

**Molecule selection**

Use the predicted values to select the 10 molecules that you would take for experimental testing if you had to choose. To that end, you can think of:

* What are the most important activities you want to optimize
* What are strict no-go points
* What are activities that are easiest to optimize at lead stage

Finally, prepare a short presentation for the rest of the participants. This should cover:

* Which models did you choose and why
* What selection strategy did you decide
* Which were your selected molecules

### Breakout session day 3

