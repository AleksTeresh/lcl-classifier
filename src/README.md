# Running locally

1. 

```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

or if the container already exists

```
docker start some-postgres
```

2.

```
cd server/
python ./api.py
```

3.

```
cd client/
npm run dev
```
