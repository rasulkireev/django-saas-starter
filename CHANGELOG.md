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


## [0.0.6] - 2025-11-03
### Added
- Added banner model to make it easy to create banners for specific Referrers.
- Added EmailSent model to keep track of all the emails sent to users.

### Changes
- All landing pages are now in `pages` app

## [0.0.6] - 2025-10-28
### Changed
- use simple text if mjml is not setup

## [0.0.6] - 2025-10-24
### Changed
- updated dj-stripe and stripe versions

## [0.0.6] - 2025-10-24
### Added
- Privacy Policy and Terms of Service Links
- Healthcheck API endpoint
- Custom 404 error page with modern design
- Add FAQs to landing page

### Changed
- default timeout for tassk to be around an hour

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
