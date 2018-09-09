## Setting up the Development Environment

```bash
git clone git@github.com:eJourn-al/eJournal.git
cd eJournal
make setup
```

The first step downloads the full repository.
`make setup` installs all required dependencies and sets up the virtual environment. This also runs

- `make migrate-back`: sets up the database so that it can be properly used.
- `make fill-db`: fills the database with random information so that we have something to test without having to create everything first.

### Structure of the Development Environment

#### Frontend

Files are stored in `src/vue`.
To start the development vue server type `make run-front` in the `eJournal` folder. The Frontend is dependent on the Backend to work properly with requesting data, so make sure to also run the backend.

`npm` should always be run in this directory, as the `node_modules` folder is stored here. For the actual source files, view the `src/vue/src` folder.

#### Backend

Files are stored in `src/django`.
To start the development django server type `make run-back` in the `eJournal` folder.

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
