# Incremental Long-Term Assignments for Canvas VLE [![Build Status](https://travis-ci.com/Rickyboy320/PSE_Hokkies.svg?token=r1oSN27zZYdQJnbijrgR&branch=develop)](https://travis-ci.com/Rickyboy320/PSE_Hokkies)

Canvas VLE integration

During the first and second years of the Bachelor Informatics at the University of Amsterdam, students follow a course called PAV (practicum academische vaardigheden or practicum academic competencies). One part of the PAV course is the colloquium journal; students are required to attend events related to their field of study and report on their experiences. Each event can be worth one or more points and students are required to acquire at least ten points by the end of their second year of study. The students' reports are evaluated by a tutor and assigned points on a regular basis.

[Full description](https://www.overleaf.com/read/hxzqgqqmzvwc)

## Setting up the Development Environment

```bash
git clone git@github.com:Rickyboy320/PSE_Hokkies.git
cd PSE_Hokkies
make setup
```

The first step downloads the full repository.
`make setup` installs all required dependencies and sets up the virtual environment. This also runs

- `make migrate-back` sets up the database so that it can be properly used.
- `make fill-db` fills the database with random information so that we have something to show.

### Structure of the Development Environment

#### Frontend:

Files are stored in `src/vue`.
To start the vue-server type `make run-front` in the `PSE_Hokkies` folder.
The Frontend is dependent on the Backend to work properly with requesting data, so make sure to also run the backend.

npm should always be ran in this directory, as the `node_modules` folder is stored here.
For the actual source files, enter the `src` directory in `src/vue`.

#### Backend:

Files are stored in `src/django`.
To start the django-server type `make run-back` in the `PSE_Hokkies` folder.

## Testing

Tests are written in `src/vue/test` and `src/django/test` respectively.
To run the tests and linters, use `make test`. Make sure to run this before starting a Pull Request, else it is certain to fail.
If you only want to test the frontend or backend, use `make test-front` and `make test-back` respectively.

## Git Flow

To initiate git flow, use `git flow init`. It will ask for settings, just press enter for all, as we are using the defaults.

Feature:
`git flow feature start [name]`
Program the feature and test if everything works.
Add and commit.
Merge with the latest develop branch.
`git flow feature publish`
Start a pull request (on github.com).
Wait for Travis to finish testing, and let a fellow developer review and approve your code.

For bugfixes, the same approach is used, but replace all `feature` with `bugfix`.

If Git Flow does not work for whatever reason, default Git commands can be used instead (the Git Flow commands are shortcuts after all).

Feature:
`git checkout -b feature/name`
Program the feature and test if everything works.
Add and commit.
Merge with the latest develop branch. (`git pull origin develop`)
`git push origin feature/name`
Start a pull request (on github.com).
Wait for Travis to finish testing, and let a fellow developer review and approve your code.

## Deployment

### Preconfiguring Production

In the file `settings/deploy.conf` there are multiple options to configure:

- `APACHEDIR`: should be pointed to the directory where apache is installed (defaults to `/etc/apache2`)
- `TARGET`: should be the directory where apache will be serving files from (defaults to `/var/www/ejournal`)
- `PORT`: should be the port the website will be accessible over, this will be appended to the `$APACHE_DIR/ports.conf` file (defaults to `8080`)
- `URL`: should be the basis URL of the site. The site will be accessible on `$URL:$PORT$HOOKPOINT`, most apis will be accessible on `$URL:$PORT$HOOKPOINTapi`, and admin will be accessible on `$URL:$PORT$HOOKPOINTadmin` (defaults to `localhost:8080`)
- `HOOKPOINT`: Defines the path after the URL to serve as a root folder for this project (defaults to `/`).


### Deploying

Run

```bash
make deploy
```

If not already installed, it will install [apache2](https://httpd.apache.org/), apache2-dev, and [wsgi_mod 4.6.4](https://github.com/GrahamDumpleton/mod_wsgi) from source.
It sets up the modular `wsgi.conf` file in `$APACHE_DIR/conf-available/` and automatically enables it.
It also sets up the modular `ejournal.conf` file in `$APACHE_DIR/sites-available/` and enables it on the set port (default 8080),
also adding the port to the `$APACHE_DIR/ports.conf` file.

It compiles the vue files, and copies all mandatory source files to the destination folder, replacing configurables where needed.

### Additional Configuration

#### Create a Superuser

If this is the first time deploying the code to a server instance, you may want to make a superuser. A superuser is created by running the following commands.

```bash
source ./venv/bin/activate
python ./django/manage.py createsuperuser
deactivate
```

Make sure to use a strong password and username, as these credentials will be able to manipulate the database at will.


## Contributors

Jeroen van Bennekum
Xavier van Dommelen
Okke van Eck
Engel Hamer
Lars van Hijfte
Hendrik Huang
Maarten van Keulen
Joey Lai
Teun Mathijssen
Rick Watertor
Dennis Wind
Zi Long Zhu
