---
description: >-
  This pages provides a deep dive into the structure of the model template for
  new model incorporation
---

# Model Template

## Anatomy of the Ersilia Model Template

Each model in the Ersilia Model Hub is contained within an individual GitHub repository. Each model repository is created using the [**Ersilia Model Template**](https://github.com/ersilia-os/eos-template) upon approval of the Model Request issue. When the new repository is created, please fork it and work on modifying the template from your own user. Open a pull request when the model is ready.

{% hint style="danger" %}
When you have finished the model incorporation, please delete the fork from your own GitHub user. This will prevent abuses of the Git-LFS quota and outdated versions of the models.
{% endhint %}

Below, we describe the main files you will find in the newly created model repository. Note that some of them are automatically updated and you do not have to modify them, like the `README.MD.`

### The `eos` identifier

Each model in the Ersilia Model Hub has an Ersilia Open Source (EOS) identifier. This identifier determines the name of the GitHub repository containing the model:

```
https://github.com/ersilia-os/[EOS_IDENTIFIER]
```

The `eos` identifier follows this regular expression: `eos[1-9][a-z0-9]{3}`. That is:

* The `eos` prefix, plus...
* one digit  (`1-9`) (the `0` is reserved for test models), plus...
* three alphanumeric (`a-z` and `0-9`) characters.

{% hint style="success" %}
`eos` identifiers are automatically assigned at repository creation. Please do not modify them.
{% endhint %}

### The `metadata.yml` file

The `metadata.yml` file is where all the model information can be found. This is the only place where you should modify or update the model description, interpretation etc. The Airtable backend, the browsable Model Hub and the README file will automatically be updated from the `metadata.yml` upon merge of the Pull Request.&#x20;

The YAML fields are constrained by certain parameters. If they do not adhere to the minimal quality standards, the Pull Request will be rejected and an explanatory message will be available on the GitHub Action. Below we try to provide a comprehensive overview of the metadata accepted:

**Identifier:** the `eos` identifier described above. It will be automatically filled in. _Do not modify._

**Slug:** a one-word or multi-word (linked by a hypen) human-readable identifier, stored as a string, to be used as an alternative to the EOS ID. It will be filled in from the Model Request issue. it can be modified afterwards.

**Title:** a self-descriptive model title (less than 70 characters)

**Description**: minimum information about model type, results and the training dataset. We require that all models have a description of minimum 200 characters.

{% hint style="info" %}
Some contributors may find it difficult to come up with a good description for the model. You can find some inspiration in [Semantic Scholar](https://semanticscholar.org). This portal provides an AI-based **TL;DR** short description of many indexed papers.&#x20;
{% endhint %}

**Task**: the ML task performed by the model. This field is typically a list, with one ore more than one entries. The only accepted [tasks](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/task.txt) are: `Regression`, `Classification`, `Generative`, `Representation`, `Similarity`, `Clustering` and `Dimensionality reduction`.

**Mode**: [mode](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/mode.txt) of training of the models: `Pretrained` (the checkpoints were downloaded directly from a third party), `Retrained` (the model was trained again using the same or a new dataset), `In-house` (if the model has been developed from scratch by Ersilia's contributors) or `Online` (if the model sends queries to an external server). This field is a string.

**Input:** data format required by the model. Most chemistry related models, for example, will require compounds as input. Currently, the only accepted [inputs](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/input.txt) by Ersilia are `Compound`, `Protein` or `Text`. This field is a list containing one or more entries. At present Ersilia only works with models with Compound inputs.

**Input Shape:** [format](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/input\_shape.txt) of the input data. It can be `Single` (one compound), `Pair` (for example, two compounds), a `List`, a `Pair of Lists` or a `List of Lists`. Please note this refers to the _minimum_ shape for the model to work. If a model predicts, for example, the antimalarial potential of a small molecule, the input shape is `Single`, regardless of the fact that you can pass several compounds in a list.

**Output:** description of the model [result](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/output.txt). It is important to choose the right description. Is the model providing a probability? Is it a score? Is it a new compound? The only accepted output formats are: `Boolean`, `Compound`, `Descriptor`, `Distance`, `Experimental value`, `Image`, `Other value`, `Probability`, `Protein`, `Score`, `Text`. This field is a list with one or more acceptable values.

**Output Type:** the only accepted output [types](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/output\_type.txt) are `String`, `Float` or `Integer`. More than one type can be added as a list if necessary. This field is typically a list with one or more acceptable values.

**Output Shape:** similar to the input shape, in what format is the endpoint returned? The only accepted output [shapes](https://github.com/ersilia-os/ersilia/blob/master/ersilia/hub/content/metadata/output\_shape.txt) are: `Single`, `List`, `Flexible List`, `Matrix` or `Serializable Object`. This field is a string with only a single accepted value.

**Interpretation:** provide a brief description of how to interpret the model results. For example, in the case of a binary classification model for antimalarial activity based on experimental IC50, indicate the experimental settings (time of incubation, strain of parasite...) and the selected cut-off for the classification.

**Tag:** labels to facilitate model search. For example, a model that predicts activity against malaria could have _P.falciparum_ as tag. This field is a list with one or more accepted values since models can have more than one tag. Select between one and five relevant from the following categories:

* Disease: `AIDS`, `Alzheimer`, `Cancer`, `Cardiotoxicity`, `Cytotoxicity`, `COVID19`, `Dengue`, `Malaria`, `Neglected tropical disease`, `Schistosomiasis`, `Tuberculosis`.
* Organism: `A.baumannii`, `E.coli`, `E.faecium`, `HBV`, `HIV`, `Human`, `K.pneumoniae`, `Mouse`, `M.tuberculosis`, `P.aeruginosa`, `P.falciparum`, `Rat`, `Sars-CoV-2`,  `S.aureus`, `ESKAPE`.
* Target: `BACE`, `CYP450`, `GPCR`, `hERG`.&#x20;
* Experiment: `Fraction bound`, `IC50`, `Half-life`, `LogD`, `LogP`, `LogS`, `MIC90`, `Molecular weight`, `Papp`, `pKa`.
* Application: `ADME`, `Antimicrobial activity`, `Antiviral activity`, `Bioactivity profile`, `Lipophilicity`, `Metabolism`, `Microsomal stability`, `Natural product`, `Price`, `Quantum properties`, `Side effects`, `Solubility`, `Synthetic accessibility`, `Target identification`, `Therapeutic indication`, `Toxicity`.
* Dataset: `ChEMBL`, `DrugBank`, `MoleculeNet`, `Tox21`, `ToxCast`, `ZINC`, `TDCommons`.
* Chemoinformatics: `Chemical graph model`, `Chemical language model`, `Chemical notation`, `Chemical synthesis`, `Compound generation`, `Descriptor`, `Drug-likeness`, `Embedding`, `Fingerprint`, `Similarity`.

**Publication:** link to the original publication. Please refer to the journal page whenever possible, instead of Pubmed, Researchgate or other secondary webs. This field is a string with only one accepted value.

**Source Code:** link to the original code repository of the model. If this is an in-house model, please add here the link of the ML package used to train the model. This field is a string with only one accepted value.

**License:** the License of the original code. We have included the following OS licences: `MIT`, `GPL-3.0`, `LGPL-3.0`, `AGPL-3.0`, `Apache-2.0`, `BSD-2.0`, `BSD-3.0`, `Mozilla`, `CC`. You can also select `Proprietary or` `Non-commercial` if the authors have included their own license notice (for example restricting commercial usage). If the code was released without a license, please add `None` in this field. Make sure to abide by requirements of the original license when re-licensing or sub-licensing third-party author code (such as adding the license file together with the original code). This field is a string with only one accepted value.

{% hint style="info" %}
If the predetermined fields are not sufficient for your use case, you can open a pull request to include new ones to our [repository](https://github.com/ersilia-os/ersilia/tree/master/ersilia/hub/content/metadata). Please do so only if strictly necessary (for example, if a disease is not already in the Tag field).

Ersilia maintainers will review and approve / reject PRs for additions to the existing lists of approved items.
{% endhint %}

{% hint style="danger" %}
Note that these fields are filled in as Python strings, therefore misspellings or lower / uppercases will affect their recognition as valid values.
{% endhint %}

### The [`README`](https://github.com/ersilia-os/eos-template/blob/main/README.md) file

The `README.md` file is where we give basic information about the model. It reads from the metadata.json file and it will be automatically updated thanks to a GitHub Action once the Pull Request is approved.

Please do not modify it manually.

### The [`LICENSE`](https://github.com/ersilia-os/eos-template/blob/main/LICENSE) file

By default, all code written in contribution to Ersilia should be licensed under a [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html). The main `LICENSE` file of the repository, therefore, will be a GPLv3 as specified by [GitHub.](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository)

However, the license notices for code developed by **third parties** must be kept in the respective folders where the third-party code is found.

### The [`install.yml`](https://github.com/ersilia-os/eos-template/blob/main/install.yml) file

Ersilia uses an `install.yml` file to specify installation instructions. The YAML syntax is used because it is easy to read and maintain. This file specifies which Python version to use to build a conda environment, or a Docker image for the model.&#x20;

This dependency configuration file has two top level keys, namely, `python`, and `commands.` They dependencies are to be specified in the following manner:

* `python` key expects a string value denoting a python version (eg `"3.10"`)
* `commands` key expects a list of values, each of which is a list on its own, denoting the dependencies required by the model. Currently, dependencies  from`pip` and `conda` are supported.
* `pip` dependencies are expected to be three element lists in the format `["pip", "library", "version"]`
* `conda` dependencies are expected to be four element lists in the format `["conda", "library", "version", "channel"]`, where channel is the conda channel to install the required library.
* When the model is run from source, Ersilia always defaults to creating a conda environment for the model to provide isolation. However, when the model is Dockerized, whether conda is used in that process depends entirely on there being conda dependencies in this file.&#x20;

The `install.yml` available in the Ersilia Model Template is the following:

{% code title="install.yml" %}
```docker
python: "3.10"
commands:
    - ["pip", "rdkit-pypi", "2022.3.1b1"]
    - ["conda", "pandas", "1.3.5", "default"]
```
{% endcode %}

In this case, when running the model from source, a Conda environment will be used to isolate the model. Additionally, a conda environment will also be used inside the Docker image of the mode. This example demonstrates an installation instructions for an environment using Python 3.10.

In this example, the `rdkit-pypi==2022.3.1b1` will be installed using `pip`, while `pandas=1.3.5` will be installed using `conda` through the default package channel on conda.

The `install.yml` file can contain as many commands as necessary. Please limit the packages to the bare minimum required, sometimes models have additional packages for extra functionalities that are not required to run the model. It is good practice to trim to the minimum the package dependencies to avoid conflicts. Always pin the version of the package to make sure it is always reproducible.

{% hint style="warning" %}
The `install.yml file` contains the installation instructions of the model. Therefore, the content of this file can be very variable, since each model will have its own dependencies.
{% endhint %}

### The [`model`](https://github.com/ersilia-os/eos-template/tree/main/model) folder

The `model` folder is the most important one. It contains two sub-folders:

* `framework`: In this folder, we keep all the necessary code to run the model (assuming dependencies are already installed).
* `checkpoints`: In this folder, we store the model data (pretrained model parameters, scaling data, etc).

{% hint style="danger" %}
The `model` folder **should not** contain anything other than the `framework` and `checkpoints` subfolder. When the Ersilia CLI eventually fetches the model, it does a reorganization of the code and the only subfolders it keeps are these two. Any other file or folder at the `model/` directory level will be overlooked.
{% endhint %}

{% hint style="info" %}
Often, the separation between `framework` and `checkpoints` is not easy to determine. Sometimes, models obtained from third parties have model data embedded within the code or as part of the repository. In these cases, it is perfectly fine to keep model data in the `framework` subfolder, and leave the `checkpoints` subfolder empty.
{% endhint %}

The `framework` subfolder contains at least one Bash file, named `run.sh`. This file will run as follows:

```bash
bash run.sh [FRAMEWORK_DIR] [DATA_FILE] [OUTPUT_FILE]
```

Unless strictly necessary, the `run.sh` file should accept three and only three arguments, namely `FRAMEWORK_DIR`, `DATA_FILE` and `OUTPUT_FILE`. In the current template, we provide the following example:

{% code title="run.sh" %}
```bash
python $1/code/main.py -i $2 -o $3
```
{% endcode %}

In this case, a Python file located in the `[FRAMEWORK_DIR]/code` folder is executed, taking as input (`-i`) the `DATA_FILE` and giving as output (`-o`) the `OUTPUT_FILE`.

To understand this further, we now need to inspect the step `main.py` file in the step above, in more detail. The current template proposes the following script:&#x20;

{% code title="code/main.py" %}
```python
# imports
import os
import csv
import joblib
import sys
from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# checkpoints directory
checkpoints_dir = os.path.abspath(os.path.join(root, "..", "..", "checkpoints"))

# read checkpoints (here, simply an integer number: 42)
ckpt = joblib.load(os.path.join(checkpoints_dir, "checkpoints.joblib"))

# model to be run (here, calculate the Molecular Weight and add ckpt (42) to it)
def my_model(smiles_list, ckpt):
    return [MolWt(Chem.MolFromSmiles(smi))+ckpt for smi in smiles_list]
    
# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    smiles_list = [r[0] for r in reader]
    
# run model
outputs = my_model(smiles_list, ckpt)

# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["value"]) # header
    for o in outputs:
        writer.writerow([o])
```
{% endcode %}

In this case, the model simply calculates the molecular weight and adds a number to it.

The important steps of the script are:

1. Load model parameters.
2. Read input file.
3. Run predictions using the input file and the model parameters.
4. Write the output.

Most of the work of the model contributor will be to work on this or similar scripts. In the template, we provide a dummy model (i.e. add a fixed value to the molecular weight). This dummy model can can be already defined within the script (`my_model`). However, in real world cases, the model will most likely be loaded from a third party Python library, or from a (cloned) repository placed in the same directory.

To summarize, in the template, we provide a structure that follows this logic:

1. The `run.sh` script executes the Python `main.py` script.
2. The `main.py` script:
   * Defines the model code.
   * Loads parameters from `checkpoints`.
   * Reads an input file containing SMILES (with header).
   * Runs a model that calculates molecular weight and adds an integer defined by the parameters.
   * Writes an output file containing one column corresponding to the output value (with a header).

{% hint style="info" %}
In the template, the example provided is very simple. Depending on the model being incorporated, the logic may be different. For example, many third party models already contain a command-line option, with a specific syntax. In these cases, you may want to write scripts to adapt the input and the output, and then execute the model as-is.

Each script will be one `main.py` file, we can create as many as necessary and rename them appropriately (see below for examples)
{% endhint %}

### The `.gitattributes` file

We use Git LFS to store large files (over 100 MB). Typically, these files are model parameters. Files to be stored in Git LFS should be specified in the `.gitattributes` file. The current file will store in Git LFS all files in `csv`, `h5`, `joblib`, `pkl`, `pt` and `tsv` format.

```
*.csv filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.joblib filter=lfs diff=lfs merge=lfs -text
*.pkl filter=lfs diff=lfs merge=lfs -text
```
