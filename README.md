[![Pipeline](https://github.com/dlin96/nfl-fantasy-model/actions/workflows/python-app.yml/badge.svg)](https://github.com/dlin96/nfl-fantasy-model/actions/workflows/python-app.yml)
## Runbook
docker run --name nfldb_pg -v nfldb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=PG_PASSWD -d postgres
