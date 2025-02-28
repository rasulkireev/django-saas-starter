
# {{ cookiecutter.project_name }}

## Getting Started

All the information on how to run, develop and update your new application can be found in the documentation.

1. Update the name of the `.env.example` to `.env` and update relevant variables.

To start you'll need to run these commands:
1. `poetry install`
2. `poetry export -f requirements.txt --output requirements.txt --without-hashes`
3. `poetry run python manage.py makemigrations`
4. `make serve` : Make sure you have a Docker Engine running. I recommend OrbStack.

## Next steps
- When everything is running, go to http://localhost:8000/ to check if the backend is running.
  - If you get an error about manifest.json, just restart containers by doing Ctrl+C in the terminal and `make serve` again.
- You can sign up via regular signup. The first user will be made admin and superuser.
- Go to http://localhost:8000/admin/ and update Site info (http://localhost:8000/admin/sites/site/1/change/) to
  - localhost:8000 (if you are developing locally, and real domain when you are in prod)
  - Your project name


{% if cookiecutter.use_stripe == 'y' -%}
## Stripe
- For local. When you run make serve for the first time, a stripe-cli container will be created.
Looks at the logs for this container and at the top you will see a webhook secret generated.
Copy this and add it to your `.env` file.

The following notes are applicable only after you got the app running locally via `make serve`:
- Add Test and Prod Secret keys in the admin panel: http://localhost:8000/admin/djstripe/apikey/
(djstripe will figure out if they are live or test keys automatically)
- Create a webhook in Django admin panel: http://localhost:8000/admin/djstripe/webhookendpoint/
  - you can't use localhost as the domain for the webhook, so use something like `https://statushen.xyz/webhook/` or a real one if you have it. It doesn't matter for local.
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
- If you made changes to tasks, you need to restart the worker container with `make restart-worker`.
- If you will need to use from `pgvector` don't forget to run `CREATE EXTENSION vector;` in your db, before running any migrations with `VectorFields`
