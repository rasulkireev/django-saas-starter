<p align="center">
  <img src="#" width="230" alt="{{ cookiecutter.project_name }} Logo">
</p>

<!--  -->
<div align="center">
  <b>{{ cookiecutter.project_name }}</b>
  <b>{{ cookiecutter.project_description }}</b>
</div>

***

## Overview

- Add info about your project here

***

## TOC

- [Overview](#overview)
- [TOC](#toc)
- [Deployment](#deployment)
  - [Render](#render)
  - [Docker Compose](#docker-compose)
  - [Pure Python / Django deployment](#pure-python--django-deployment)
  - [Custom Deployment on Caprover](#custom-deployment-on-caprover)
- [Local Development](#local-development)
- [Stripe Setup](#stripe-setup)
  - [Configure Stripe](#configure-stripe)
  - [Test Webhooks Locally](#test-webhooks-locally)

***

## Deployment

### Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo={{ cookiecutter.repo_url }})

**Note:** This should work out of the box with Render's free tier if you provide the AI API keys. Here's what you need to know about the limitations:

- **Worker Service Limitation**: The worker service is not a dedicated worker type (those are only available on paid plans). For the free tier, I had to use a web service through a small hack, but it works fine for most use cases.

- **Memory Constraints**: The free web service has a 512 MB RAM limit, which can cause issues with **automated background tasks only**. When you add a project, it runs a suite of background tasks to analyze your website, generate articles, keywords, and other content. These automated processes can hit memory limits and potentially cause failures.

- **Manual Tasks Work Fine**: However, if you perform tasks manually (like generating a single article), these typically use the web service instead of the worker and should work reliably since it's one request at a time.

- **Upgrade Recommendation**: If you do upgrade to a paid plan, use the actual worker service instead of the web service workaround for better automated task reliability.

**Reality Check**: The website functionality should be usable on the free tier - you'll only pay for API costs. Manual operations work fine, but automated background tasks (especially when adding multiple projects) may occasionally fail due to memory constraints. It's not super comfortable for heavy automated use, but perfectly functional for manual content generation.

If you know of any other services like Render that allow deployment via a button and provide free Redis, Postgres, and web services, please let me know in the [Issues]({{ cookiecutter.repo_url }}/issues) section. I can try to create deployments for those. Bear in mind that free services are usually not large enough to run this application reliably.


### Docker Compose

This should also be pretty streamlined. On your server you can create a folder in which you will have 2 files:

1. `.env`

Copy the contents of `.env.example` into `.env` and update all the necessary values.

2. `docker-compose-prod.yml`

Copy the contents of `docker-compose-prod.yml` into `docker-compose-prod.yml` and run the suggested command from the top of the `docker-compose-prod.yml` file.

How you are going to expose the backend container is up to you. I usually do it via Nginx Reverse Proxy with `http://{{ cookiecutter.project_slug }}-backend-1:80` UPSTREAM_HTTP_ADDRESS.


### Pure Python / Django deployment

Not recommended due to not being too safe for production and not being tested by me.

If you are not into Docker or Render and just wanto to run this via regular commands you will need to have 5 processes running:
- `python manage.py collectstatic --noinput && python manage.py migrate && gunicorn ${PROJECT_NAME}.wsgi:application --bind 0.0.0.0:80 --workers 3 --threads 2`
- `python manage.py qcluster`
- `npm install && npm run start`
- `postgres`
- `redis`

You'd still need to make sure .env has correct values.

### Custom Deployment on Caprover

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

6. Github Workflow in this repo should take care of the rest.

## Local Development

1. Update the name of the `.env.example` to `.env` and update relevant variables.
2. Run `uv sync`
3. Run `uv run python manage.py makemigrations`
4. Run `make serve`
5. Run `make restart-worker` just in case, it sometimes has troubles connecting to REDIS on first deployment.


{% if cookiecutter.use_stripe == 'y' -%}
## Stripe Setup

This app uses Stripe Checkout for purchases and the Billing Portal for subscription management.

### Configure Stripe

- Set the following in `.env`:
  - `STRIPE_SECRET_KEY`
  - `STRIPE_PUBLISHABLE_KEY` (optional, only needed for client-side Stripe.js)
  - `STRIPE_WEBHOOK_SECRET`
  - `STRIPE_PRICE_ID_MONTHLY`
  - `STRIPE_PRICE_ID_YEARLY`
  - `WEBHOOK_UUID` (optional, used to gate webhook URLs)
- Enable the Billing Portal in the Stripe Dashboard and allow subscription updates and cancellations.
- Create a webhook endpoint in the Stripe Dashboard:
  - URL: `https://<your-domain>/stripe/webhook/<WEBHOOK_UUID>/` (or `/stripe/webhook/` if no UUID)
  - Events: `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `checkout.session.completed`

### Test Webhooks Locally

- Use the Stripe CLI container (see `docker-compose-local.yml`) to forward webhooks:
  - `docker compose -f docker-compose-local.yml run --rm stripe listen --forward-to http://backend:8000/stripe/webhook/${WEBHOOK_UUID}/`
- Trigger a test event:
  - `docker compose -f docker-compose-local.yml run --rm stripe trigger customer.subscription.created`
{% endif %}