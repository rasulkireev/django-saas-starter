
# {{ cookiecutter.project_name }}

## Getting Started

All the information on how to run, develop and update your new application can be found in the documentation.

1. Update the name of the `.env.example` to `.env`

To start you'll need to run these commands:
1. `poetry install`
2. `poetry run python makemigrations`
3. `make serve` : Make sure you have a Docker Engine running. I recommend OrbStack.

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

## Notes
- Don't forget to update the site domain and name on the Admin Panel.
