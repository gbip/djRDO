# djRDO

<div href="https://demo.djrdo.org" style="text-align:center"><img alt="djRDO banner" src="assets/banner.png" /></div>

## [Demo](https://demo.djrdo.org)

djRDO is a free software that allows dj to manage their music collection.

At the moment it is geared towards djs that are using CD players.

## Features


* Lightweight application : only your music metadata is uploaded to the server, not the whole file
* Gain new insight on your collection : find holes in your collection
* Group your music by collection

## Screenshots
 <p align="middle">
<img href="https://github.com/gbip/djRDO/blob/master/readme_assets/collection.png?raw=true" alt="Collection view screenshot" src="https://github.com/gbip/djRDO/blob/master/readme_assets/collection.png?raw=true" width="150">
<img href="https://github.com/gbip/djRDO/blob/master/readme_assets/insights.png?raw=true" alt="Collection view screenshot" src="https://github.com/gbip/djRDO/blob/master/readme_assets/insights.png?raw=true" width="150">
<img href="https://github.com/gbip/djRDO/blob/master/readme_assets/music.png?raw=true" alt="Collection view screenshot" src="https://github.com/gbip/djRDO/blob/master/readme_assets/music.png?raw=true" width="150">
<img href="https://github.com/gbip/djRDO/blob/master/readme_assets/upload.png?raw=true" alt="Collection view screenshot" src="https://github.com/gbip/djRDO/blob/master/readme_assets/upload.png?raw=true" width="150">
</p>


## Development

### Manual setup

First clone the repo and install the dependencies.
This project uses `pipenv` to manage the python dependencies

```shell
git clone https://github.com/gbip/djRDO
cd djRDO
pipenv shell # Move into the virtual environment
```

However, before installing the dependencies, you need to install a few packages that are needed by the mysql, postgresql and argon2 python libraries:

On **Ubuntu**-based distro you can install those packages with :
```shell
sudo apt install gcc musl-dev postgresql-dev musl-dev libffi-dev mariadb-connector-c-dev mariadb-dev
```    

On **Arch**-based distro you can install them with :
```shell
postgresql python-mysqlclient python-argon2_cffi
```

```shell
pipenv install # Install dependencies
```

All django commands must be typed in the pipenv shell !
So stay in the pipenv shell at the end of the process.

You will need to create a `.env` file that defines your database configuration.
Some examples are provided (`.env.*`). To use sqlite3 as a database (recommended for development) use this command :

```shell
ln -s .env.sqlite3 .env
```


Then, you can create the database :

```shell
# Still in pipenv shell
python manage.py migrate
```

To launch a development web server : 

```shell
python manage.py runserver
```

To run the test suite :

```shell
python manage.py test
```

### Using docker


A `docker-compose` configuration file is provided for this project.
Run `docker-compose -f docker-compose.yml up` to use it.

This docker image is based on the following files :
* `.env.docker.dev`
* `docker-compose.yml`
* `Dockerfile`

## Configuration

Currently, the application is configured using a `.env` file. The provided `.env.sqlite3` makes a good candidate for a 
development configuration.

### Options

* `DEMO_ENABLED` : enables the demo message and loads a pre-filled database. It does not take care of flushing the database
every hour, this needs to be automated using a system tool (eg `crontab`).
* `REGISTRATION_ENABLED` : enabled by default, set to false to disable registration

## Deployment

### With docker

The current docker-compose setup spins up a nginx reverse proxy along with let's encrypt certificates for https.
Two versions are provided :
* a *staging* version which uses the staging letsencrypt environment
* a *production* version which uses the production letsencrypt environment

Docker environment files are named using the following syntax : `.env.docker.(staging | prod).(nginx|djrdo|postgre)`.
Where `djrdo` is the python configuration, `postgre` the database configuration and `nginx` some of the nginx config.
The other part of the nginx configuration lives in `./nginx`

Before running any docker command, you should modify the files `.env.docker.prod.*.example` to suit your setup.

Then, starting djRDO can be done using either of the following commands :
```shell
sudo docker-compose -f docker-compose.staging.yml up # Staging version
```

```shell
sudo docker-compose -f docker-compose.prod.yml up # Production version
```

### Without docker

Not supported yet.