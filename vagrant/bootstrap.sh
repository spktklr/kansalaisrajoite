vag#!/usr/bin/env bash

# Readies kansalaisrajoite server for development

# Install development tools (git, python dev tools, postgresql)
apt-get update
apt-get install -y git python-software-properties python-dev python-pip python-flup libffi-dev postgresql libpq-dev

# Install python dependencies
pip install bottle sqlalchemy bottle-sqlalchemy bcrypt beaker pycrypto
pip install argparse pycparser wsgiref cffi psycopg2 --upgrade

# Pull the project into vagrant's shared directory
cd /vagrant
git clone https://github.com/spktklr/kansalaisrajoite
cd kansalaisrajoite
git checkout templatet-ja-routing

# Create a database user and database, and import fixture contents
sudo -u postgres createuser -E -d -r -S vagrant
sudo -u vagrant createdb ragemachine
sudo -u vagrant psql -d ragemachine -f db/create.sql
sudo -u vagrant psql -d ragemachine -f db/populate.sql
