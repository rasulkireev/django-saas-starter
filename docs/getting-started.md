## 1 Dependencies

### Python dependencies
After you have run the cookiecutter command and the project has been generated the first thing you should do is install all the dependencies.

```
poetry install
```

Notes:

If you are having issues like this:

```
poetry install

Current Python version (3.7.7) is not allowed by the project (^3.10).
Please change python executable via the "env use" command.
```

Try running `poetry env use python3.10` and then trying poetry install again.

### Javascript

Next let's install javascript dependencies with `npm install`


## 2 Creating the Database

The next thing you want to do is to create and apply the migrations. First run:

```
poetry run python manage.py makemigrations
```

then

```
poetry run python manage.py migrate
```

This will create a SQLite database with all the necessary tables.

## 3 Start the dev server

Start by building the frontend resource. You can do that by running:

```
npm run start
```

You should see something like this:

```
webpack 5.73.0 compiled successfully in 3254 ms
```

Note:
Make sure you are running tht latest LTS Node. As of this writing it is 16. You can activate it with `nvm use 16` if you have nvm installed.

Now let's start the python server by `poetry run python manage.py runserver` in a new terminal window (we don't want to close the npm stuff. You can do that by pressing Ctrl+N while in VS Code Terminal). If you need a primer on how to use poetry, check out [this blog post](https://builtwithdjango.com/blog/basic-django-setup)

---

Et Voila, you should have a basic site running.