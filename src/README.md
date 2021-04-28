# LCL Classifier

## Setting up development environment

### Requirements

For provisioning and deployment, one needs
- Ansible
- psql

For running locally, one needs
- Docker
- docker-compose

For developing locally, one needs
- Docker
- docker-compose
- npm
- Python (at least version 3.8.3)
- Python Poetry

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

Go to localhost:80 (or localhost:443).

If using Google Chrome, one might be prevented
from navigating to localhost:80 due to
Chrome showing a certificate warning and not allowing
to bypass it. If presented with such a warning with no visble
options to ignore it, type `thisisunsafe` on your keyboard.
Yes, just type it when presented with the warning screen,
and Chrome should let you in. See e.g. [https://dev.to/brettimus/this-is-unsafe-and-a-bad-idea-5ej4](https://dev.to/brettimus/this-is-unsafe-and-a-bad-idea-5ej4)

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

### Setting up an instance and volume in CSC

1. A production floating IP address (195.148.21.214) should
be already reserved. If not, or a new one is needed: go to
`Network / Floating IPs` and then do `Allocate IP`.

2. Create a security group that allows access from your home's IP address to the DB instance. `Network / Security groups`, then do `Create security group`, give name e.g. "From \<Your name\>'s home to 5432", set it up so that incoming TCP connections to port **5432** from **your home's IP address** (e.g. get [here](https://www.google.com/search?q=what%27s+my+IP)) are allowed.

3. `Compute / Key pairs`, then `Import Public Key`, put your SSH public key there, give descriptive name e.g. "\<Your name\> SSH key".

4. `Compute / Instances`, then `Launch instance`, pick e.g. `standard.tiny` flavor, boot source e.g. `Boot from image / Ubuntu-20.04`. In the `Access & security` page pick the right key pair and the following security groups:
      1. one that allows TCP from everywhere to port 22 (currently called `ssh open`)
      2. one that allows TCP from everywhere to port 80 (currrently called `From everywhere to port 80`)
      3. one that allows TCP from everywhere to port 443 (currrently called `From everywhere to port 443`)
      4. the ones that allow access from certain IP addresses to
       port 5432 (database). (currently e.g. `From Alex's home to 5432` and `From Jan's home to 5432`)

5. Other defaults are fine. Press `Launch`.

6. Once it's listed in the list of instances, you should see that in the dropdown menu you can do something like `associate floating IP`, do that so that there is also a public IP address with which you can connect to the virtual machine.

7. Once the instance is up and running try to SSH into it via
    `ssh ubuntu@<whatever-is-the-ip-address>`

8. `Volumes / Volumes`. A volume called "Storage 50G" should
   already be created. If not, create a new one (see instructions [here](https://docs.csc.fi/cloud/pouta/persistent-volumes/)). Make sure that
   the volume is attached to the instance (Dropdown / `Manage attachments`). Make sure only one volume is attached to the
   instance.

### Povisioning the instance

You'll need `ansible` as a dependency. You can install it with
e.g. `brew install ansible`.

Check that `./devops/ansible/hosts.ini` contains the correct IP
address (the IP address of the machine that needs to be provisioned).

Install necessary Ansible collections:

```
ansible-galaxy collection install ansible.posix
```

Then, run the following command:
```
ansible-playbook -i ./devops/ansible/hosts.ini ./devops/ansible/provision.yml
```

Note: If the last "Create SSL Certificate" step takes "forever" (more than 10 min, let's say), do it
manually: ssh into the host, navigate to the correct directory,
and issue the same command as specified in the Ansible's
yaml file under "Create SSL Certificate".

### Deploying the app

Now you can actually deploy the app.

```
./deploy
```

If asked for a password, input `<DB_PASSWORD>`

The script will also create a backup and save it locally in
the backup folder.

## Running tests

```
cd ./server
python -m unittest discover
```

## Generating problems on the remote server

`server/main.py` specifies what families should be
generated. Feel free to comment existing statements or
add new ones as needed.

```
POSTGRES_HOST=195.148.21.214 POSTGRES_PASSWORD='<DB password>' python ./main.py
```

## To restore from a backup

```
psql "host=195.148.21.214 port=5432 dbname=postgres user=postgres" -f ./backup/<date>.sql
```

## Acknowledgements

The authors wish to acknowledge [CSC – IT Center for Science, Finland](https://www.csc.fi/en), for computational resources.
