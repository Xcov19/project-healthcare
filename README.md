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
- [ ] Add fact entity and aggregate business logic
- [ ] Add unit tests against services
- [ ] Add services for patient and provider
- [ ] Add OpenAPI endpoints for services
- [ ] Add datastore integration to services
- [ ] Add API test suite for endpoints