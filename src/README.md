# LCL Classifier

## Setting up development environment

### Requirements

- Docker
- docker-compose
- Ansible
- psql

### Environment variables

Create `.env` file as a sibling of this README and
add the following variables there:
```
POSTGRES_PASSWORD='<DB_PASSWORD>'
POSTGRES_PASSWORD_UNQUOTED=<DB_PASSWORD>
POSTGRES_HOST=db
```

### Running locally

To run the project locally in production mode, do the following:

1. Generate a dummy certificate (this step only needs to be done
once)

```
./init-dummycert.sh
```

2. Spin up the front end, back end and a database with docker-compose

```
docker-compose up --build
```

### Developing locally

#### Starting up the client

1. Navigate to the client directory
```
cd client
```

2. Install the dependencies
```
npm install
```

3. Run the development server
```
npm run dev
```

#### Starting PostgresDB locally

Run the following command from the root `src` directory:
```
docker-compose start db
```

#### Starting up the server


1. Navigate to the server directory
```
cd server
```

2. Install the dependencies
```
poetry shell
poetry install 
```
To exit the poetry shell later, issue `exit` command.

3. Run the flask app
```
poetry run python ./api.py
```

## Pre-commit

Husky will execute the pre-commit hook.

It runs `prettier`, `eslint-typescript`, `svelte-check` for
the client;

and then `black`, `pyflakes` for the server.

* `prettier` makes sure that the code style at the client is consistent
* `eslint-typescript` is a linter for TypeScript
* `svelte-check` checks `.svelte` files for the following:
  * Unused CSS
  * Svelte A11y hints
  * JavaScript/TypeScript compiler errors
* `black` makes sure that the code style at the server is consistent
* `pyflakes` is a linter for Python

## Deployment

The app is available at [lcl-classifier.cs.aalto.fi](https://lcl-classifier.cs.aalto.fi)
### Creating an instance


## Generating problems on the remote server

```
POSTGRES_HOST=195.148.21.214 POSTGRES_PASSWORD='<DB password>' python ./main.py
```

## To restore from a backup

```
psql "host=195.148.21.214 port=5432 dbname=postgres user=postgres" -f ./backup/<date>.sql
```

## To provision

```
ansible-playbook -i ./devops/ansible/hosts.ini ./devops/ansible/provision.yml
```


## Acknowledgements

The authors wish to acknowledge [CSC – IT Center for Science, Finland](https://www.csc.fi/en), for computational resources.
