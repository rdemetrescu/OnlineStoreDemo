# Online Store (PoC)

## Required
* Docker
* Docker Compose

## Installation


Clone this repository

    git clone https://github.com/rdemetrescu/OnlineStoreDemo

Enter the repository

    cd OnlineStoreDemo


Copy `env.sample` to `.env`  (inside `backend` folder)

    cp backend/.env-example backend/.env


Build and start the app

    make run

Now the server is running and you can access the app REST api documentation using one of the below:

- Swagger [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Running tests

```bash
make test
```

## Containers
- Stopping containers
```bash
make stop
```


- Remove containers and database volume
```bash
make down
```
