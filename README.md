![XCoV19](https://substackcdn.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16a2fa6-d7dd-4fce-8c1d-2c3c0c63b8a6_435x435.png)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Xcov19/project-healthcare)
[<img src="https://substackcdn.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16a2fa6-d7dd-4fce-8c1d-2c3c0c63b8a6_435x435.png" alt="Newsletter" height="32" />](https://xcov19.dev)

_Repo metadata_

[![Staged CI](https://github.com/Xcov19/project-healthcare/workflows/Staged%20CI/badge.svg)](https://github.com/Xcov19/project-healthcare/actions?query=workflow:"Staged+CI")
[![GitHub tag](https://img.shields.io/github/tag/Xcov19/project-healthcare?include_prereleases=&sort=semver&color=blue)](https://github.com/Xcov19/project-healthcare/releases/)
[![License](https://img.shields.io/badge/License-LGPL--2.1-blue)](#license)
[![issues - project-healthcare](https://img.shields.io/github/issues/Xcov19/project-healthcare)](https://github.com/Xcov19/project-healthcare/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Xcov19/project-healthcare)](https://github.com/Xcov19/project-healthcare/pulls)

## What is it
![xcov19_demo_ezgif-3-0edbb84875](https://github.com/user-attachments/assets/438e2e2c-a40f-49fc-84b0-20037acf22d6)


## Documentation

<div align="center">

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](/docs/ "Go to project documentation")

</div>


## License

Released under [LGPL-2.1](/LICENSE) by [@Xcov19](https://github.com/Xcov19).

# Project Healthcare (xcov19)

Project Healthcare, from hereon called the brokering service, is a set of upstream OpenAPI specification to extend any patient facing user interface looking to integrate to location-aware consultation and diagnostics facilities near them by:

1. Exposing a diagnosis API to capture patient symptoms.
2. Exposing geolocation API to caputure patient's location and offer nearby facilities to take action on based on their diagnosis and location.

## Extensible and Open

Unlock advanced healthcare integration without the enterprise price tag. Connect systems, personalize care, and reach underserved communities with ease.
Built using modified project template for [BlackSheep](https://github.com/Neoteroi/BlackSheep)
web framework to start Web APIs, the project structure adheres blacksheep's domain and infrastructure segregation philosophy. It naturally fits the 
domain driven design philosophy using ports and adapters pattern so expect slight shift towards domain models and services structure.

The specification follows a sandwich service model i.e. it requires one or more upstream producer services and one downstream consumer service as follows:

1. The patient facing application, known from hereon as the downstream consumer service, calls the diagnosis and geolocation API.
2. The brokering service stores transient diagnosis request and enqueues them to upstream provider service that should return records of facilities and their specialties based on the diagnosis.
3. The brokering service returns the records of matching facilities to the downstream consumer service.

## Revolutionizing Healthcare Integration for Communities

All-in-one, affordable, and scalable health integration platform tailored for small to medium-sized businesses (SMBs) and rural healthcare providing Advanced Integration, Personalized Care and Scalable Solutions.

| **Feature**                                      | **Healthcare Infrastructure Service**  | **Competitors**                |
|--------------------------------------------------|------------|--------------------------------|
| **Remote Patient Monitoring**              | ✔          | Limited/None                   |
| **EHR/EMR Integration**                          | ✔          | ✔ (Enterprise solutions)       |
| **Data Normalization, Anonymization and Aggregation**           | ✔          | Limited/None                   |
| **Rural Healthcare First**                      | ✔          | ✔ (Limited focus)              |
| **Personalized Patient Journeys and Engagement** | ✔          | Limited/None                   |
| **Developer-Friendly APIs**                      | ✔          | ✔ (Enterprise solutions only)  |
| **Cost**                                         | Freemium to Affordable | High Enterprise Pricing        |

### What Sets Us Apart?

Unlike other platforms, HIS combines advanced features in one solution, delivering exceptional healthcare services without the complexity or high costs.

## Getting started

### For Linux and Mac

1. create a Poetry virtual environment using python version in `pyproject.toml`
2. `poetry install --no-root --with=dev`
3. Run in development environment: `make run`

### For IDX

1. `poetry use env python3.12`
2. `make run`

### Deploy

To test the instance on render, set the following environment variables:

```bash
PYTHON_VERSION=3.12.4
PORT=44777
```

### Sandbox for reference
A reference instance exists on [![Render](https://gist.github.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/SERVICE-animated.svg)](https://project-healthcare.onrender.com/docs)

See [Deploy](#deploy) to spin up your own instance.

## Contributing
See [CONTRIBUTING](/CONTRIBUTING.md)

## Project Management 

See [Projects](https://github.com/Xcov19/project-healthcare/projects?query=is%3Aopen)

### TODOs:

- [x] Add standard documentation in README.md
- [ ] Add Getting Started · Learn the Basics,  Community and Support links. A contributor must know what the high level UML / block level diagram of this ecosystem looks like.
- [ ] Strategic roadmap
- [x] CONTRIBUTING.md file
- [x] Add routes logic
- [x] Add domain entity and aggregate business logic
- [ ] Add unit tests against services
- [ ] Containerization 
- [ ] Adding fast and long running test pipeline in github CI for PRs: All unit tests are to be marked fast. All automated Integration and Automation tests are long running.
- [x] CI/CD: Building and hosting staged and prod instance. I have shortlisted on few easy to deploy PaaS. We earlier used GCP but have moved away from al major cloud platforms.
- [ ] Add services for patient and provider
- [x] Add OpenAPI endpoints for services
- [ ] Add datastore integration to services
- [ ] Add API test suite for endpoints


## Background

85% of the world's population is in the Emerging Market, of which the majority of single nationality is in India with >700Mn+ smartphone users. Still, as of 2021, we ranked at the very top in the number of neglected tropical diseases cases requiring treatment that included Malaria, Dengue, Chikungunya amongst others:
![image info](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b5d3239-953e-48cd-9ba7-ba99d13b5d4f_3400x2943.png)


Despite technological advancements and introduction of PM-JAY:

1. 70% of the Indian healthcare being private, ~70% out of them run on pen and paper and are technically challenged in adapting to the fast changing digital infra landscape thus impeding the ease of operations for OPD and in-patient registration, triage and treatment.
2. 43% of Indian population including financially underprivileged sections of our society lack basic healthcare awareness. There is a huge demographic divide that dictates the quality of medical care and consultation in our country that can be availed. This is despite technological advancements and India positioning itself as a welfare state. (The Out of Pocket expenditure for the middle class has significantly risen but that is not in the scope of this topic.)
3. Additionally, UN Sustainability Goals scores India somewhere in the lower bounds of 60-80 out of 100 in terms of healthcare serviceability index.(UN SDG 3.8.1)

With alot of avenues today in the identity, payments, and data ecosystem pioneered by NPCI and further extended by Bekn protocol, governed by FIDE, in OCEN, ONDC and Open Mobility space, National health authority too has been working on Unified Healthcare Interface for sometime building the Indian Health Stack integrating turn-key healthtech private solutions with ABDM.

Just like many applications being built on top of this layer for the identify, mobility, ecommerce & trade and fintech segments, there are 2 use cases to build an opensource commons platform upon Bharat Health Stack:

- Solve unnecessary resource utilisation: Fix disproportionate allocation of resource constraints faced due to operational inefficiency across healthcare facilities.
- Reduce wait times for dissatisfied patients: Provide reduced wait times for consultation and out-patient services for at-risk patients by fixing inconsistent distribution of patient influx. This happens because patients are not aware of all the possible options (Think zomato of healthcare)

A public and open solution to these use cases makes sense because:

1. Much of the government's ABDM components are built in the open
2. Many proponents of OSS have been building such systems such as Healthstack system in Bangladesh.
3. By building out an opensource version, it makes sense to verify, audit and get feedback faster, build faster and better, aligned to the common's need.
4. And truly be transparent.

<hr />

_**Powered and Supported generously by**_

#### [DigitalOcean](https://www.digitalocean.com/)
Previously supported as [Hollie’s Hub for Good](https://www.digitalocean.com/community/pages/hollies-hub-for-good) project

![DO_Powered_by_Badge_blue](https://github.com/user-attachments/assets/cf5115cd-b38e-4c74-a9f3-cb4a0edf95f0)

#### [Helpful Engineering](https://helpfulengineering.org/)
![Helpful Engineering](https://helpfulengineering.org/wp-content/uploads/2021/08/HelpfulEngineering_textmark.svg)

#### [Code 4 GovTech](https://www.codeforgovtech.in/)
![Logo_v1205_3](https://github.com/user-attachments/assets/c304523c-7e78-4642-8c1f-b8cff2334892)

#### [My Health Connect Society](https://www.myhealthconnect.in)
![Logo_MyHealthConnect_v2](https://github.com/user-attachments/assets/6fc6df71-682c-4efe-b1b1-cc21811ec250)

