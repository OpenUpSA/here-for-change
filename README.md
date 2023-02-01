[![codecov](https://codecov.io/gh/paulmwatson/here_for_change/branch/master/graph/badge.svg)](https://codecov.io/gh/paulmwatson/here_for_change/)
[![Build Status](https://travis-ci.org/paulmwatson/here_for_change.png)](https://travis-ci.org/paulmwatson/here_for_change)

Here For Change
===============================


Complete project setup
----------------------

- [ ] Initialise a git repository in this directory
  - [ ] Explicitly add directories needed for collectstatic to work: `git add -f staticfiles/.gitkeep here_for_change/static/.gitkeep`
- [ ] Create a repository on [GitHub](https://github.com/OpenUpSA) and add as a remote to this repository
  - e.g. `git remote add origin git@github.com:OpenUpSA/here_for_change.git`
- [ ] Enable Continuous Integration checks for the GitHub Repository at [travis-ci.org](https://travis-ci.org)
  - [ ] Enable periodic builds, e.g. weekly, to detect when dependency changes break your builds before they hurt you.
- [ ] Enable code coverage reporting for the project at [codecov.io](https://codecov.io)
  - [ ] Enable GitHub integration - it automatically configures Travis-CI and shows coverage diffs in pull requests
  - [ ] Verify that you see coverage % on the Commits tab for the project. If it's just zero, check for errors by clicking a commit item.
- [ ] Clean up this checklist - your project is set up now and you don't need it any more.


Project Layout
--------------

### Docker

On Linux, you probably want to set the environment variables `USER_ID=$(id -u)`
and `GROUP_ID=$(id -g)` where you run docker-compose so that the container
shares your UID and GID. This is important for the container to have permission
to modify files owned by your host user (e.g. for python-black) and your host
user to modify files created by the container (e.g. migrations).


### Django

Apps go in the project directory `here_for_change`


### Python

Dependencies are managed via poetry in the docker container.

Add and lock dependencies in a temporary container:

    docker-compose run --rm web poetry add pkgname==1.2.3

Rebuild the image to contain the new dependencies:

    docker-compose build web

Make sure to commit updates to pyproject.toml and poetry.lock to git

Development setup
-----------------

The first time, or after a reset:

    yarn dev-init

To run the app in development:

    yarn dev

Migrations can be run:

    yarn db-migrate

Demo/seed data can be loaded with:

     yarn db-load-full-data

To dump data from your db for updating demo/seed data:

     yarn db-dump-demo-data

To fetch and load provinces into db:

     yarn db-load-provinces

To fetch and load municipalities into db:

     yarn db-load-municipalities

To fetch and load wards into db:

     yarn db-load-wards

To load dummy ward details into db:

     yarn db-load-demo-wards-details

To load ward details from json data file:

     yarn db-load-wards-details

To load municipality details from json data file:

     yarn db-load-municipality-details
  
  
If you need to destroy and recreate your dev setup, e.g. if you've messed up your
database data or want to switch to a branch with an incompatible database schema,
you can destroy all volumes and recreate them by running the following, and running
the above again:

    yarn dev-reset

Running tests
-------------

    yarn test

Tests might fail to connect to the databse if the docker-compose `db` service wasn't running and configured yet. Just check the logs for the `db` service and run the tests again.


Settings
--------

Undefined settings result in exceptions at startup to let you know they are not configured properly. It's one this way so that the defaults don't accidentally let bad things happen like forgetting analytics or connecting to the prod DB in development.


| Key | Default | Type | Description |
|-----|---------|------|-------------|
| `DATABASE_URL` | undefined | String | `postgresql://user:password@hostname/dbname` style URL |
| `DJANGO_DEBUG_TOOLBAR` | False | Boolean | Set to `True` to enable the Django Debug toolbar NOT ON A PUBLIC SERVER! |
| `DJANGO_SECRET_KEY` | undefined | String | Set this to something secret and unguessable in production. The security of your cookies and other crypto stuff in django depends on it. |
| `TAG_MANAGER_CONTAINER_ID` | undefined | String | [Google Tag Manager](tagmanager.google.com) Container ID. [Use this to set up Google Analytics.](https://support.google.com/tagmanager/answer/6107124?hl=en). Requried unless `TAG_MANAGER_ENABLED` is set to `False` |
| `TAG_MANAGER_ENABLED` | `False` | Boolean | Use this to disable the Tag Manager snippets, e.g. in dev or sandbox. |