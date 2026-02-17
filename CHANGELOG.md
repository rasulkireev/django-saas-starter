# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

**Added** for new features.
**Changed** for changes in existing functionality.
**Deprecated** for soon-to-be removed features.
**Removed** for now removed features.
**Fixed** for any bug fixes.
**Security** in case of vulnerabilities.


## [Unreleased]
### Added
- Added CLAUDE.md with repo + template architecture notes and common commands for AI coding agents
- Added Docs Section
- Added Password Reset functinoality
- Added banner model to make it easy to create banners for specific Referrers.
- Added EmailSent model to keep track of all the emails sent to users.
- Privacy Policy and Terms of Service Links
- Healthcheck API endpoint
- Custom 404 error page with modern design
- Add FAQs to landing page
- npm lint command

### Changed
- All landing pages are now in `pages` app
- use simple text if mjml is not setup
- updated dj-stripe and stripe versions
- default timeout for tassk to be around an hour
- moved all apps to apps directory
- move `core` and `pages` apps into `apps` directory.
- remove djstripe. only use strip for payments
- Use psycopg-binary instead of psycopg2-binary
- If use_stripe is no. then make sure to remove everything
- Use uv instead of poetry for pakage management.
  - No need for requirements.txt file

### Fixed
- Healthcheck endpoint now returns boolean `healthy` (instead of string statuses) for simpler monitoring integrations
- Various imports
- App Config labels
- No need for custom 404 view
- Cookiecutter `package.json` now renders valid JSON when `use_mjml = n` (removed dangling comma in dependencies)
- Production Gunicorn command no longer uses `--reload` in `deployment/entrypoint.sh`
- Cookiecutter base templates now include dark-mode aware header/nav/mobile/footer styling classes
- Cookiecutter auth templates now include dark-mode friendly contrast updates
- Cookiecutter settings template and confirm-email warning banner now include dark-mode friendly contrast updates
- Cookiecutter auth templates (`login`, `signup`, `password_reset`) now include dark-mode friendly text/input/border styling

## [0.0.5] - 2025-10-23
### Added
- support for self hosted mjml server
- MJML email templates for allauth (signup and email confirmation):

### Changed
- landing page and home page are now different pages
- added admin panel page for info and test triggers
- user-settings now has a single button for all the forms on the page
- stling of the upgrade flow
- moved the blog and api logic to a separate app
- use pg 18 for local db

### Removed
- test_mjml function and template (replaced with proper allauth email templates)
- unused imports from core/views.py (HttpResponse, render_to_string, strip_tags, EmailMultiAlternatives)

## [0.0.4] - 2025-10-12
### Changed
- how sentry will capture logs

## [0.0.4] - 2025-09-26
### Added
- New context_processor which figures out which social apps you have installed
- New context_processor which figures out if user is a paying customer
- render deployment configuration

### Updated
- .env.example file with better instructions and more options
- S3 is now optional
- README with better deployment instructions
- apps.py to run POSTHOG if API key is available
- tasks to only run if relevant env vars are present
- settings file to work with new deployment options
- docker-compose files to support both local and prod deployments
- makefile commands to include local compose file

### Removed
- cookiecutter variable that makes social auth optional. instead the code takes care of that

## [0.0.3] - 2024-11-11
### Added
- Experimental Flag

## [0.0.3] - 2024-11-11
### Added
- Fix missing orphan on User settings page.
- Ignore the djlint " vs. ' error.
- Add django-ninja (with Auth and test endpoint)
- Update dependencies


## [0.0.2] - 2024-10-10
### Added
- SEO tags + JSON-LD on all the pages
- Optional Blog
- All pages to the sitemap

## [0.0.1] - 2024-09-28
### Added
- Sign-in with Github and Logout button don't go to separate screen anymore.

### Fixed
- close button on messages now works fine
