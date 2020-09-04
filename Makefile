containerName := nfldb_pg
volumeName := nfldb
packageDir := ffmdl
modelDir := ${packageDir}/models
featureDir := ${packageDir}/features
envName := modelenv

venv: requirements.txt
	python3 -m virtualenv ${envName}
	source ${envName}/bin/activate
	pip install -r requirements.txt

dockerDb:
	docker volume create nfldb
	docker run --name ${containerName} -v ${volumeName}:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=${NFLDB_PASSWORD} -d postgres

database: run.sh .env
	. .env
	./run.sh

features: ${featureDir}/build_features.py ${featureDir}/feat_*.py
	python ${featureDir}/build_features.py

train: data/interim/base_fantasy_df.pkl ${modelDir}/train.py
	python3 ${modelDir}/train.py

inference: data/interim/base_fantasy_df.pkl ${modelDir}/inference.py
	python3 ${modelDir}/inference.py

clean:
	docker stop ${containerName}
	docker container prune -f
	# docker volume rm ${volumeName}

.PHONY: clean features train database dockerDb venv