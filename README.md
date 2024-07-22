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