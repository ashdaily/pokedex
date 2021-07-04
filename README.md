### MUST DO

---

- [x] comply
- [x] check if django user in docker really needed 
- [x] manage secrets using .env file
- [x] add tests as per compliance
- [ ] cache


### HOW TO BUILD, SPIN, WATCH LOGS, etc

---

- Prerequisites: 
  - Need docker at-least, so please install [docker](https://docs.docker.com/get-docker/)
  - I am assuming you are using Unix like system. 
- Before running the project add `.env.local` file at project root directory and copy contents of `.env.example` file using:
  - `cat .env.example | tee .env.local`. Note that this command might not work properly on Windows, it's better to create `.env.local` by hand.
- Run the project:
  - `docker-compose up`. But remember to add `.env.local` file at project root directory and copy contents of `.env.example` file as already mentioned in the first step. Otherwise the build will fail.
- Run test cases: 
  - `docker-compose run pokemon_container bash -c "cd project &&  python3 manage.py test --no-input"` 
- Exec: `docker exec -it pokemon-container bash`
- Call the API:
  - Visit [localhost:5000/swagger](http://localhost:5000/swagger/) and try the APIs.
  - Or, Use curl
  ```
  # get info for pokemon_name pikachu
  curl -X GET "http://localhost:5000/pokemon/pikachu" -H  "accept: application/json" -H  "X-CSRFToken: RRJjriTZY4PEWRjiM0NeW5dbobUSB3Sxpv5SZgZj7aiOmxd79d0TgUyCE0wuKGr3"

  # get translated info for pokemon_name pikachu
  curl -X GET "http://localhost:5000/pokemon/translated/pikachu" -H  "accept: application/json" -H  "X-CSRFToken: RRJjriTZY4PEWRjiM0NeW5dbobUSB3Sxpv5SZgZj7aiOmxd79d0TgUyCE0wuKGr3"
  ```
 
 
### You can keep the builds for local, development, testing, staging production seperate: 

---

```
# For local environment, using --build-arg is not required. Build needs `.env.local` file at project root.
docker-compose build backend
OR
docker-compose build --build-arg TARGET_ENV=local backend

# For development environment, Build needs `.env.development` file at project root.
docker-compose build --build-arg TARGET_ENV=development backend

# For testing environment, Build needs `.env.testing` file at project root.
docker-compose build --build-arg TARGET_ENV=testing backend

# For staging environment, Build needs `.env.staging` file at project root.
docker-compose build --build-arg TARGET_ENV=staging backend

# For production environment, Build needs `.env.production` file at project root.
docker-compose build --build-arg TARGET_ENV=production backend
```


## Production checklist

---

- [ ] add logging
- [ ] add sentry 
- [ ] add travis CI
- [ ] do some profiling and load testing
- [ ] use dependabot for keeping dependencies fresh