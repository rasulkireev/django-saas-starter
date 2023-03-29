Once cookiecutter the project run `makemigrations` and `migrate` to create the database.

## Features

- For Django 4.0
- Works with Python 3.11
- Registration via django-allauth
- 12-Factor based settings via django-environ
- TailwindCSS & StimulusJS (Hotwire) - comes with Webpack configure for dev & prod.
- Comes with custom user model ready to go
- SQLite for Database


## Roadmap
- Add more default styling
- Create a core app and start populating it with CRUD operations
- Add optional Stripe support
- Add some tech overview to the Readme
- Add Wagtail for the blog
- Send emails via Anymail (Mailgun by default) (plus add Mailhog)
- Media storage with Cloudinary
- Add github workflows to automate deployment (digitalocean, fly, appliku)
- Add pre-commit
- Set up logs for dev and prod
- Add Sentry option
