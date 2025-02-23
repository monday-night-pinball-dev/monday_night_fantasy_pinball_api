# Summary

The DICS Core Data Service repository has three major moving parts:

1. The Database Migrator
2. The API itself built primarily as a CRUD service
3. A QDK (Quality Development Kit) implementation that tests all endpoints as modules and provides a development kit for more advanced integration tests.

# Getting Started

## Prerequisites

### Install Pyenv and Python

1. Install pyenv: https://github.com/pyenv/pyenv#installation
2. Run ```pyenv install 3.12.6```
3. Run ```pyenv local 3.12.6```
4. Run ```pyenv global 3.12.6```

### Install Docker Desktop

Install instructions can be found here: https://docs.docker.com/get-started/get-docker/

## Create and initialize the Database

1. Open the /database folder in Visual Studio Code.
2. Make sure your Docker is running.
3. Copy the .env-example file and name it ".env" (these are default values for the database and are fine for local development)
4. Open the terminal and run ```docker compose up -d```.
5. You should see a database instance with the settings from your .env file running in your docker!
6. Connect to your database using PgAdmin4 or similar and the settings prefixed with POSTGRES_ from your .env and run the following:
```
CREATE USER migrator WITH PASSWORD 'mMiIgGrRaAtToOrR1!2@3#4$' SUPERUSER; 

GRANT ALL PRIVILEGES ON DATABASE dics TO migrator;

CREATE USER service WITH PASSWORD 'sSeErRvViIcCeE1!2@3#4$' SUPERUSER;

GRANT 
	SELECT,
	INSERT,
	UPDATE,
	DELETE
ON ALL TABLES IN SCHEMA public TO service;

GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public to service;

ALTER DEFAULT PRIVILEGES FOR ROLE migrator IN SCHEMA public GRANT SELECT, UPDATE, INSERT, DELETE ON TABLES TO service;
```
This is important for setting up the roles that would already exist in a deployed database.

## Migrate the Database

Note: all migrations are idempotent, meaning they can be run over and over.  If the step has already run, nothing will happen.

1. Open the database folder in Visual Studio Code
2. Open the terminal and run ```pip install -r requirements.txt```
3. If step 2 does not work and complains about pg_config executable, "brew install postgresql" should fix your issue.
4. Go to the Debug Tab on the left and, near the top, select the "Python Debugger: DB Migrator" option.
5. Hit F5 on your keyboard.  You should see the console run some steps.
6. Connect to your database and check that all the steps ran.

For more information on the database, check out the ReadMe.md in the database folder!

## Run the service

1. Open the serverlessservice folder in Visual Studio Code
2. Copy the .env-example file to another file called ".env"
3. Open the terminal and run ```pip install poetry```
4. Run ```poetry install```
5. Run make install-dependencies
4. Go to the Debug Tab on the left and, near the top, select "Python Debugger: Run API"
5. Hit F5 on your keyboard.  You should see console output telling you that Uvicorn is running on 127.0.0.1:8001
6. If you have installed everything but the runtime can't find dependencies, try running ```rm -rf `poetry env list --full-path` ``` and then ```poetry install```
7. Your API is running!

For more information on the service, check out the ReadMe.md in the service folder!

## Run the API Tests

1. Open the tests folder in Visual Studio Code
2. Copy the .env-example file to a new file called ".env"
3. Open the terminal and run ```pip install -r requirements.txt```
4. The Flask Tab on the left should detect tests and you can run them from there.  Otherwise, go into the validation/CRUD folder and select a test file, and you can right click in the code and run a case from there.

For more information on the tests, check out the ReadMe.md in the tests folder!





