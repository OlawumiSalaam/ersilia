---
description: >-
  We present ChemSampler, a simple tool to sample molecules in a given region of
  the chemical space.
---

# Sampling the chemical space

{% hint style="danger" %}
This page is :construction\_worker: **work in progress** :construction\_worker:!
{% endhint %}

ChemSampler acts as a framework that fetches generative AI models from the Ersilia Model Hub and runs iterative rounds of generation to provide the user with a pool of new or sampled existing molecules for downstream filtering using bioactivity predictors and/or docking approaches.

## Basic structure

ChemSampler accepts one single molecule (<mark style="color:green;">seed\_smiles</mark>) as input. The seed smiles is passed to each one of the Ersilia Model Hub Generative models (<mark style="color:orange;">samplers</mark>) specified in the `params.json` file (see below). All results of this first round are collated in a single output .csv file, and a random sample of 100 molecules from the generated list is provided to the user for ease of evaluation.&#x20;

ChemSampler runs as many rounds as specified in the `params.json` file or until the maximum number of desired molecules has been achieved. In each round, ChemSampler will evaulate whether the <mark style="color:green;">seed\_smiles</mark> is still providing enough good candidates (new unique molecules) or whether a new <mark style="color:purple;">input\_smiles</mark> needs to be selected from the pool of generated molecules. The ranking of newly generated molecules is done by similarity search using <mark style="color:yellow;">molecular descriptors</mark> specified by the user. If the user is interested in small modifications of the seed\_smiles, 2D descriptors should be prioritized. On the contrary for scaffold hopping exercises, 3D and pharmacophore descriptors should be prioritized. The molecule most similar to the <mark style="color:green;">seed\_smiles</mark> according to the selected descriptors will be used as <mark style="color:purple;">input\_smiles</mark> for the next round. A schema is shown below:

<figure><img src="../.gitbook/assets/Screenshot from 2023-12-14 14-37-53.png" alt=""><figcaption><p>General schema of a round of ChemSampler generation</p></figcaption></figure>

### The parameters file

The parameters file is a `.json` file that allows the user to specify:

```json
{
    "seed_smiles": <origin smiles for the generative tool>,
    "keep_smiles": <smiles substructure to be preserved in generated candidates>,
    "avoid_smiles": <smiles substructure to be discarded in generated candidates>,
    "samplers": [ <list of ersilia identifiers for the samplers> ],
    "descriptors": [ <list of ersilia identifiers for the molecular descriptors> ],
    "num_samples": <maximum number of molecules generated>,
    "max_rounds": <maximum number of rounds>,
    "time_budget_sec": <maximum time spent per round>,
    "saturation_number": <number of new candidates required to continue sampling from the same input smiles>,
    "output_folder": <folder where results will be stored>
}
```

_\* If keep\_smiles or avoid\_smiles are specified, all molecules that do not fulfill either criteria will be removed, which potentially could lead to low number of generated candidates_

#### Input

A seed\_smiles, a list of samplers and a list of descriptors. All of those must be specified in the parameters file.

#### Output

* A list of generated/sampled molecules and its similarity to the seed\_smiles. Similarity is calculated using the molecular descriptors and either euclidean distances or tanimoto similarity.
* A info.json file where information about each round (how many molecules were generated, how many of those were new, which was the input smiles...) is stored
* A sample of 100 molecules randomly selected to be drawn for the user to evaluate the performance of each round

## Available Samplers



## Available molecular descriptors
