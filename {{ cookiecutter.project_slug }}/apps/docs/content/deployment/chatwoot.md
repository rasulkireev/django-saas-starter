---
title: Chatwoot Support Chat
description: Configure the optional Chatwoot website widget for support, feedback, bug reports, and feature requests.
keywords: {{ cookiecutter.project_name }}, Chatwoot, support chat, feedback, customer support
author: {{ cookiecutter.author_name }}
---

Chatwoot support chat is included because this project was generated with `use_chatwoot = y`.

The feature is still runtime-opt-in: the widget only appears when both `CHATWOOT_BASE_URL` and `CHATWOOT_WEBSITE_TOKEN` are set in the Django web app environment.

## What gets installed

- A Django context processor: `apps.core.context_processors.chatwoot_config`
- A template include: `frontend/templates/components/chatwoot.html`
- Includes in the app and landing base templates
- Optional authenticated-user identification via `window.$chatwoot.setUser(...)`
- Optional HMAC Identity Validation via `CHATWOOT_HMAC_SECRET`

## Self-hosted Chatwoot setup

Use this path if you run Chatwoot yourself, for example on CapRover.

1. Open your Chatwoot dashboard, for example `https://chatwoot.yourdomain.com`.
2. Go to **Settings → Inboxes**.
3. Click **Add Inbox** / **New Inbox**.
4. Choose **Website**.
5. Name the inbox after this app, for example `{{ cookiecutter.project_name }}`.
6. Add your production site domain when Chatwoot asks for the website domain.
7. Finish setup.
8. Open the inbox settings/configuration and copy the `websiteToken` from the install snippet.

Set:

```env
CHATWOOT_BASE_URL=https://chatwoot.yourdomain.com
CHATWOOT_WEBSITE_TOKEN=<websiteToken from the Website inbox>
```

Do not paste the full `<script>...</script>` snippet into Django templates. This starter already includes the widget loader; it only needs the base URL and token.

## Chatwoot Cloud setup

Use the same Website inbox flow in Chatwoot Cloud.

Set:

```env
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_WEBSITE_TOKEN=<websiteToken from the Website inbox>
```

If your Chatwoot Cloud workspace uses a region-specific or custom domain, use the base URL from the snippet Chatwoot gives you.

## Identity Validation / HMAC

For authenticated SaaS apps, enable Identity Validation so users cannot impersonate each other in Chatwoot conversations.

1. In Chatwoot, open **Settings → Inboxes → your Website inbox**.
2. Go to **Settings → Configuration → Identity Validation**.
3. Enable/copy the HMAC token.
4. Set it as:

```env
CHATWOOT_HMAC_SECRET=<identity validation HMAC token>
```

This app signs the authenticated Django user's primary key as the Chatwoot identifier. It also sends their email and display name.

If you enable Identity Validation in Chatwoot but forget `CHATWOOT_HMAC_SECRET`, the widget may load but authenticated identity can fail. Either set the correct secret or disable Identity Validation in Chatwoot.

## Deployment checklist

1. Add env vars to the Django web app/container:
   - `CHATWOOT_BASE_URL`
   - `CHATWOOT_WEBSITE_TOKEN`
   - `CHATWOOT_HMAC_SECRET` if Identity Validation is enabled
2. Restart/redeploy the web app after changing env vars.
3. Open a page that uses `base_app.html` or `base_landing.html`.
4. Confirm the Chatwoot bubble appears in the bottom-right corner.
5. For logged-in users, start a conversation and confirm Chatwoot shows the user's email/name.

## Common gotchas

- **Wrong app/container:** Adding env vars only to a worker process will not show the widget. They must be present on the process rendering Django pages.
- **No restart after env changes:** Django reads settings at process startup. Restart/redeploy after changing env vars.
- **Token ellipsis:** Do not paste a shortened token like `abc…xyz`. Paste the full `websiteToken` from Chatwoot.
- **Base URL mismatch:** Use the same base URL shown in Chatwoot's snippet. Self-hosted examples look like `https://chatwoot.yourdomain.com`; Chatwoot Cloud commonly uses `https://app.chatwoot.com`.
- **Identity Validation mismatch:** If Chatwoot has Identity Validation enabled, `CHATWOOT_HMAC_SECRET` must match that exact inbox's token.
- **Ad blockers / browser privacy tools:** Some extensions block chat widgets. Check the browser console/network tab for blocked `sdk.js` requests.
- **CSP/security headers:** If you add a strict Content Security Policy later, allow scripts/connections/frames for your Chatwoot base URL.

## Disabling Chatwoot

Unset either value and restart the web app:

```env
CHATWOOT_BASE_URL=
CHATWOOT_WEBSITE_TOKEN=
```

The template include stays installed, but it renders nothing unless both values are configured.
