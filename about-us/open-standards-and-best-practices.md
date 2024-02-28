---
description: This page describes Ersilia's Open Standards and Best Practices Principles
---

# Open Standards and Best Practices

## Open Standards

We follow [DPG Alliance tips for Open Standards](https://github.com/DPGAlliance/publicgoods-candidates/blob/main/help-center/open-standards.md). Below is a summary and proof of adherence to these standards.

| Concept                                                   | Comment                                                                                                                                                                                                                                                                      | Proof of Adherence                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Accessibility, Security, Authentication and Authorization | Ersilia uses GitHub primarily. Accessibility, security and authentication/authorization is therefore reliant on GitHub solutions. We use DependaBot to monitor package dependencies and identify security liabilities. GitHub Secrets are used intensively in our workflows. | See our [GitHub profile](https://github.com/ersilia-os) for more information. A summary of our GitHub security usage can be found [here](https://github.com/ersilia-os/ersilia/security).                                                                                                                                                                                                                                            |
| Internationalization                                      | UTF-8 encodings is used in our scripts, most of them written in Python. Code is formatted with Black.                                                                                                                                                                        | You can see our main codebase [here](https://github.com/ersilia-os/ersilia).                                                                                                                                                                                                                                                                                                                                                         |
| Application Programming Interfaces (APIs)                 | OpenAPI, especially via Swagger UI as facilitated by BentoML.                                                                                                                                                                                                                | Check one of our deployed models [here](https://eos80ch-m365k.ondigitalocean.app/).                                                                                                                                                                                                                                                                                                                                                  |
| Data Exchange and Configuration Formats                   | We primarily use YAML, JSON, CSV and TOML formats.                                                                                                                                                                                                                           | [Setup file](https://github.com/ersilia-os/ersilia/blob/master/pyproject.toml) in TOML format. [Metadata file](https://github.com/ersilia-os/eos3b5e/blob/main/metadata.json) in JSON. [Workflow file](https://github.com/ersilia-os/ersilia/blob/master/.github/workflows/pr\_check.yml) in YAML. [Data file](https://github.com/ersilia-os/pharmacogx-embeddings/blob/main/data/chemical\_descriptors/drug\_molecules.csv) in CSV. |
| Standard Content Formats and Multimedia                   | Content and multimedia are not our main assets. Internally, we store documents and media files with standard formats.                                                                                                                                                        | An example of a one-pager in PDF format can be found [here](https://drive.google.com/file/d/1Xxgpjh3gCQdD\_MqEDxweJIPY\_1JGKSIN/view?usp=sharing). We store videos in MP4 format, and upload them to [Youtube](https://www.youtube.com/channel/UCeioZf4Qj4hWi3O5Ta2k-xQ).                                                                                                                                                            |

## Best Practices and Principles

We follow [DPG Alliance tips for Best Practices and Principles](https://github.com/DPGAlliance/publicgoods-candidates/blob/main/help-center/best-practices.md). Below is a summary and proof of adherence to these principles.



| Concept                                       | Comment                            | Proof of Adherence |
| --------------------------------------------- | ---------------------------------- | ------------------ |
| ICT4D                                         | Principles for Digital Development |                    |
| User stories                                  |                                    |                    |
| Change management and version control         |                                    |                    |
| Test driven development using automated tests |                                    |                    |
| CI/CD                                         |                                    |                    |
| Code review                                   |                                    |                    |
| Agile development                             |                                    |                    |
| Modularity and Maintainability                |                                    |                    |
| Reusability and Extensibility                 |                                    |                    |
| Component based architecture                  |                                    |                    |
| Cloud Computing                               |                                    |                    |
| AI/ML                                         |                                    |                    |
| User Interface and User Experience (UI/UX)    |                                    |                    |
| Coding Styles and Standards                   |                                    |                    |
| Open Source                                   |                                    |                    |
| Data Principles                               | FAIR Data Principles               |                    |
