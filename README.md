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
