<p align="center">
    <img width="250" src="https://avatars1.githubusercontent.com/u/41028230"/>
</p>

[![Build Status](https://travis-ci.com/eJourn-al/eJournal.svg?branch=develop)](https://travis-ci.com/eJourn-al/eJournal) [![Coverage Status](https://codecov.io/gh/eJourn-al/eJournal/branch/develop/graph/badge.svg)](https://codecov.io/gh/eJourn-al/eJournal)

eJournal is a blended learning web application that provides an easy to manage graded journal system focused on education.

## Server management

`make run-ansible-[TAG] [VARS]`

**TAG** options:
- `provision` install all dependencies and setup (new) server (also runs deploy)
- `deploy` deploy frontend and backend
- `deploy-front` deploy frontend
- `deploy-back` deploy backend
- `preser_db` reset db to preset db
- `backup` create backup

**VARS** (optional):

- `branch=[current branch]` specify branch
- `host=[staging]` specify host

## File structure

- `config/` server configuration
- `requirements/` requirements
- `src/` source code
  - `django/VLE/` backend code
  - `django/test/` unit tests backend
  - `vue/src/` frontend code
- `monitoring/` monitoring configuration

## Troubleshooting

For any technical trouble regarding eJournal, please [open an issue](https://github.com/eJourn-al/eJournal/issues/new). Keep in mind that eJournal currently only supports being hosted on Debian based platforms.

Other support issues can also be send to [support@ejournal.app](mailto:support@ejournal.app).

## Contributors

<table>
    <tr>
    <td align="center">
        <a href="https://github.com/engelhamer">
            <img src="https://avatars1.githubusercontent.com/u/39912581?s=100" width="100px;"><br />
            <sub><b>Engel Hamer</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Larspolo">
            <img src="https://media-exp1.licdn.com/dms/image/C4D03AQFbS0NuXNGFGA/profile-displayphoto-shrink_200_200/0?e=1590624000&v=beta&t=-TyvPbMQ2K-5YjIk8SxAIuGaiRVgZRUtTtTjzQ9S94c" width="100px;"><br />
            <sub><b>Lars van Hijfte</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/mjvkeulen">
            <img src="https://media-exp1.licdn.com/dms/image/C5603AQGmUyL2hMKnHQ/profile-displayphoto-shrink_200_200/0?e=1590624000&v=beta&t=0xmS38Va9Xmic_3fkO2P46Y4w_VhuOwQDOFJzTZTDfM" width="100px;"><br />
            <sub><b>Maarten van Keulen</b></sub>
        </a>
    </td>
  </tr>
</table>

Together with:

Jeroen van Bennekum, Xavier van Dommelen, Okke van Eck, Hendrik Huang, Siard Keulen, Joey Lai, Teun Mathijssen, Mohammed el Mochoui, Rick Watertor, Dennis Wind, Zi Long Zhu.

## Contributing

For information about contributing to the project, see [CONTRIBUTING.MD](CONTRIBUTING.MD).
