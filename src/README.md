# Running locally

1. Generate a dummy certificate

```
./init-dummycert.sh
```

2. Spin up front-end, back-end and a database with docker-compose

```
docker-compose up --build
```

# Generating problems on the remote server

```
POSTGRES_HOST=195.148.21.214 POSTGRES_PASSWORD='<DB password>' python ./main.py
```
