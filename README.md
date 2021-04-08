# djRDO

<div style="text-align:center"><img alt="djRDO banner" src="assets/banner.png" /></div>


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

### Configuring your workspace

First clone the repo and install the dependencies.
This project uses `pipenv` to manage the python dependencies

```shell
git clone https://github.com/gbip/djRDO
cd djRDO
pipenv shell # Move into the virtual environnement
pipenv install # Install dependencies
```

Stay in the pipenv shell at the end of the process.

You will need to generate a secret key for djRDO :

```shell
echo "SECRET_KEY = " `python -c "import secrets; print(secrets.token_urlsafe())"` > .env
```


Then, you can create the database :

```shell
# Still in pipenv shell
python manage.py migrate
```

You can then run all your django commands within this shell.

To launch a development web server : 

```shell
python manage.py runserver
```

To run the test suite :

```shell
python manage.py test
```