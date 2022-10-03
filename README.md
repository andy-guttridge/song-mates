# Song Mates

## Purpose

Thanks to modern technology, musicians can make great quality recordings at home. There's never been a better time for musicians to be able to express themselves via the 
medium of digital recording. Great music is often the result of collaboration, and while audio technology enables musicians to work with each other remotely, how do you find people to collaborate with?
 
The purpose of Song Mates is to provide a platform for musicians who want to write, perform and record material to find like minded people to collaborate with, whether that be for a song or an album.

Users can register with Song Mates, and create a profile with an image, a biography or summary of what they're looking for, and can specify the instruments they play and relevant skills. They can search for potential collaborators using these criteria, and make collaboration requests (like a connection request on LinkedIn or friend request on Facebook). Users can send direct messages to their  connections.

## Table of contents

## User stories

## Agile development methodology

## Features

## Planning

## Frameworks, libraries and dependencies

### Django 3.2

### Psychopg 2
Python PostgreSQL adapater

### Gunicorn
Python WSGI HTTP server

### dj-database-url
Django utility to create an environment variable to configure the Django application


## Data model

## Testing

### Manual testing

### Automated tests

### Validator testing

##  Bugs

### Resolved bugs

### Unresolved bugs

## Deployment

## Credits

### Code

- The steps to connect to a Heroku Postgres database and deploy were adapted from the Code Institute 'I think therefore I blog' tutorial. This includes defining `DATABASE_URL` and `SECRET_KEY` environment variables in an `env.py` file in the local environment and adding corresponding config variables in the Heroku dashboard, using dj_database_url to create a URL from the Heroku database URL in `settings.py`, updating `ALLOWED_HOSTS` in `settings.py` with the deployed Heroku URL and adding the templates path to a `TEMPLATES_DIR` variable in `settings.py`.

### Content