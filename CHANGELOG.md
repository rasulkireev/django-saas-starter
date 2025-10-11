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
