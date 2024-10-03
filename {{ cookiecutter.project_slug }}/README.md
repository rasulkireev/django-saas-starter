
# {{ cookiecutter.project_name }}

## Getting Started

All the information on how to run, develop and update your new application can be found in the documentation.

1. Update the name of the `.env.example` to `.env`

To start you'll need to run these commands:
1. `poetry install`
2. `poetry run python makemigrations`
3. `make serve` : Make sure you have a Docker Engine running. I recommend OrbStack.

{% if cookiecutter.use_stripe == 'y' -%}
## Stripe
- For local. When you run make serve for the first time, a stripe-cli container will be created. Looks at the logs for this container and at the top you will see a webhook secret generated. Copy this and add it to your `.env` file.

- Make sure to add secrets in the .env file and in the admin panel: /admin/djstripe/apikey/

- When creating a webhook in the admin, specify the latest version from here https://stripe.com/docs/api/versioning

- Create your products in stripe (monthly, annual and one-time, for example), then sync them via `make stripe-sync` command.

- Current (`user-settings.html` and `pricing.html`) template assumes you have 3 products: monthly, annual and one-time.
  I haven't found a reliable way to programmatcialy set this template. When you have created your products in Stripe and synced them, update the template with the correct plan id.
{% endif %}

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
