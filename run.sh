#!/bin/bash

function build_db {
    export PGPASSWORD=$NFLDB_PASSWORD

    echo "Running build_db..."
    psql -h localhost -p 5432 -U postgres -c "CREATE USER nfldb WITH PASSWORD '$NFLDB_PASSWORD';"
    psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE nfldb;"
    psql -h localhost -p 5432 -U nfldb nfldb < data/external/nfldb.sql
}

alias lint=`pylint --fail-under=8 ffmdl`
alias flake=`flake8 ffmdl --count --select=E9,F63,F7,F82 --show-source --statistics`
# include training and prediction scripts