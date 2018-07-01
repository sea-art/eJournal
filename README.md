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

- `make migrate-back`: sets up the database so that it can be properly used.
- `make fill-db`: fills the database with random information so that we have something to test without having to create everything first.

### Structure of the Development Environment

#### Frontend

Files are stored in `src/vue`.
To start the development vue server type `make run-front` in the `PSE_Hokkies` folder. The Frontend is dependent on the Backend to work properly with requesting data, so make sure to also run the backend.

`npm` should always be run in this directory, as the `node_modules` folder is stored here. For the actual source files, view the `src/vue/src` folder.

#### Backend

Files are stored in `src/django`.
To start the development django server type `make run-back` in the `PSE_Hokkies` folder.

## Testing

Tests are written in `src/vue/test` and `src/django/test` respectively.
To run the tests and linters, use `make test`. Make sure to run this before starting a Pull Request, else it is certain to fail.
If you only want to test the frontend or backend, use `make test-front` and `make test-back` respectively.

## Git Flow

To initiate git flow, use `git flow init`. It will ask for settings, just press enter for all, as we are using the defaults.

Git Flow introduces five types of branches that can be used for development.

A significant branch is the `master` branch. This is the branch solely used for full releases and major milestones. Any Pull Request to the master branch requires three reviewers to accept the PR.

More important for developers is the `develop` branch. This always represents the latest state of development and should often be pulled into the `feature/` branches. All features will submit a PR to the develop branch, and never to the `master`. When a develop commit is deemed stable enough, a PR can be opened to merge develop to master.

The `feature/` branches are where all features are developed. Every feature branch has the following name convention: `feature/the-feature-name`. The feature branch can freely be manipulated, pushed to and pulled from. When a feature is deemed finished, it can be Pull Requested for pull into `develop`.

Two smaller types of branches, and often less consistently used are the `bugfix/` and `hotfix/` branches. These are meant for bugfixes and small 'hot' fixes.

### Feature

`git flow feature start [name]`
Program the feature and test if everything works.
Add and commit.
Merge with the latest develop branch (`git pull origin develop`).
`git flow feature publish`
Start a pull request (on github.com).
Wait for Travis to finish testing, and let a fellow developer review and approve your code.

For bugfixes and hotfixes, the same approach is used, but replace all `feature` with `bugfix` and `hotfix` respectively.

If Git Flow does not work for whatever reason, default Git commands can be used instead (the Git Flow commands are multiple commands in one after all). In most cases these substitutions suffice:
`git flow feature start [name]` -> `git checkout -b feature/name`
`git flow feature publish` -> `git push origin feature/name`

## Deployment

### Preconfiguring Production

In the file `settings/deploy.conf` there are multiple options to configure:


- `APACHE_DIR`: should be pointed to the directory where apache is installed (defaults to `/etc/apache2`).
- `TARGET`: should be the directory where apache will be serving files from (defaults to `/var/www/ejournal`).
- `TYPE`: should be the http type: either http or https (defaults to `http`).
- `SERVERNAME`: should be the website URL. The site will be accessible on `$URL:$PORT$HOOKPOINT` (defaults to `localhost`).
- `APIURL`: should be the API URL. The API will be accessible on `$APIURL:$PORT$HOOKPOINT` (defaults to `api.localhost`).
- `PORT`: should be the port the website will be accessible over, this will be appended to the `$APACHE_DIR/ports.conf` file (defaults to `80`).
- `HOOKPOINT`: Defines the path after the URL to serve as a root folder for this project. Should always end with a `/` (defaults to `/`).


In the file `settings/database.conf` you will need to configure the database. By default we use [postgresql](https://www.postgresql.org/).

- `DATABASE_TYPE`: the backend of the database. Can be one of the backends [specified by django](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DATABASE-ENGINE) (defaults to postgresql).
- `DATABASE_NAME`: the name of the database (defaults to ejournal).
- `DATABASE_HOST`: the URL of the server running the database (defaults to localhost).
- `DATABASE_PORT`: the port on which the database is accessible through `$DATABASE_HOST`.
- `DATABASE_USER`: the user for the server to create as database owner. Note that this user will gain all rights for the table set in `$DATABASE_NAME`, as this is required for the server to be able to freely manipulate the database.
- `DATABASE_PASSWORD`: the password that should be set for the `$DATABASE_USER`.

In the file `settings/secrets.conf` you will be required to generate new secret keys for django and LTI. Neither of these fields should be the same, and it is suggested you use a random string generator to generate the secret.
Use a sufficiently long and complex secret (the default by django is 50 characters).

### Deploying

```bash
make deploy
```

This will, if not already installed, install [apache2](https://httpd.apache.org/), apache2-dev, and [wsgi_mod 4.6.4](https://github.com/GrahamDumpleton/mod_wsgi) from source.
It sets up the modular `wsgi.conf` file in `$APACHE_DIR/conf-available/` and automatically enables it.
It also sets up the modular `ejournal.conf` file in `$APACHE_DIR/sites-available/` and enables it on the set port (default 8080), also adding the port to the `$APACHE_DIR/ports.conf` file.

It compiles the vue files, and copies all mandatory source and static files to the destination folder, replacing configurables where needed.

### Additional Configuration

#### Create a Superuser

If this is the first time deploying the code to a server instance, you may want to make a superuser. A superuser will be an user that can access /admin and therefore set up the site according to his will. At least one superuser is required, else no initial courses, assignments and journals can be created.

A superuser is created by running the following commands while in the `$TARGET` folder

```bash
source ./venv/bin/activate
python ./django/manage.py createsuperuser
deactivate
```

Make sure to use a strong password, as these credentials will be able to manipulate the database at will.


## Troubleshooting

May the setup or deployment fail, [open an issue on github](https://github.com/Rickyboy320/PSE_Hokkies/issues/new).
The setup and deployment scripts have been built for ubuntu, and may not work on any other linux distributions. May the need for this arise, the scripts can be altered to support additional distributions.

## Contributors

Jeroen van Bennekum: Scrum Master, Database Design & Implementation  
Xavier van Dommelen: Design, Front-end & EDAG  
Engel Hamer: Design, Front-end  
Hendrik Huang: Design, Front-end & EDAG  
Maarten van Keulen: Design, Front-end  
Zi Long Zhu: Database Design, Back-end, Test Implementations  
Joey Lai: Front-end, Back-end, Test Implementations  
Teun Mathijssen: Back-end, Database specialist, Testing  
Lars van Hijfte: Project Structure, Back-end, Project Deployment, Server Master  
Rick Watertor: Project Structure, Back-end, Project Deployment, Git Master  
Okke van Eck: Front-end & LTI  
Dennis Wind: LTI Specialist  
