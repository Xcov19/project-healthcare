# Project Healthcare (xcov19)

Built using modified project template for [BlackSheep](https://github.com/Neoteroi/BlackSheep)
web framework to start Web APIs.

The project structure adheres blacksheep's 
domain and infrastructure segregation philosophy. It naturally fits the 
domain driven design philosophy using ports and adapters pattern so 
expect slight shift towards domain models and services structure.

## Getting started

### For Linux and Mac

1. create a Poetry virtual environment using python version in `pyproject.toml`
2. `poetry install --no-root`
3. Run in development environment: 
`poetry run python3 -m xcov19.dev`

TODOs:


- [ ] Add standard documentation in README.md
- [ ] Strategic roadmap
- [ ] CONTRIBUTING.md file
- [ ] Updating README.md: A contributor must know what the high level UML / block level diagram of this ecosystem looks like to understand the context. 
- [ ] Add routes logic
- [ ] Add domain entity and aggregate business logic
- [ ] Add unit tests against services
- [ ] Containerization 
- [ ] Adding fast and long running test pipeline in github CI for PRs: All unit tests are to be marked fast. All automated Integration and Automation tests are long running.
- [ ] CI/CD: Building and hosting staged and prod instance. I have shortlisted on few easy to deploy PaaS. We earlier used GCP but have moved away from al major cloud platforms.
- [ ] Add services for patient and provider
- [ ] Add OpenAPI endpoints for services
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
