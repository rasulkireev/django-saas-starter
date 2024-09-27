
# {{ cookiecutter.project_name }}

## Getting Started

All the information on how to run, develop and update your new application can be found in the documentation.

To start you'll need to runb these 2 commands:
1. `poetry export -f requirements.txt --output requirements.txt --without-hashes`
2. `make serve` : Make sure you have a Docker Engine running. I recommend OrbStack.

## Deployment

1. Create 4 apps on CapRover.
  - `{{ cookiecutter.project_slug }}`
  - `{{ cookiecutter.project_slug }}-workers`
  - `{{ cookiecutter.project_slug }}-postgres`
  - `{{ cookiecutter.project_slug }}-redis`

2. Create a new CapRover app token for:
   - `{{ cookiecutter.project_slug }}`
   - `{{ cookiecutter.project_slug }}-workers`

3. Add Environment Variables to those same apps from `.env`.

4. Create a new GitHub Actions secret with the following:
   - `CAPROVER_SERVER`
   - `CAPROVER_APP_TOKEN`
   - `WORKERS_APP_TOKEN`
   - `REGISTRY_TOKEN`

5. Then just push main branch.
