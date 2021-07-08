### What is Pokedex ? 

---

- Pokedex use free pokeapi.co API for searching pokemon related information using pokemon names.
- ✔️ Uses django web framework with django rest framework pip package. 
- ✔️ Uses docker/docker-compose.
- ✔️ Uses redis for caching for dramatically reducing load on third party apis and speed improvement. 
- ✔️ Comes with unit tests based on python unit test framework and vcr cassettes for recording request response interactions with pokeapi.co API. 
- ✔️ Load tested with [npm loadtest](https://www.npmjs.com/package/loadtest) 

---

### Call the API:

---

- Visit [localhost:5000/swagger](http://localhost:5000/swagger/) and try the APIs.
- Or, Use curl
```
# get info for pokemon_name pikachu
curl -X GET "http://localhost:5000/pokemon/pikachu" -H  "accept: application/json" -H  "X-CSRFToken: RRJjriTZY4PEWRjiM0NeW5dbobUSB3Sxpv5SZgZj7aiOmxd79d0TgUyCE0wuKGr3"

# get translated info for pokemon_name pikachu
curl -X GET "http://localhost:5000/pokemon/translated/pikachu" -H  "accept: application/json" -H  "X-CSRFToken: RRJjriTZY4PEWRjiM0NeW5dbobUSB3Sxpv5SZgZj7aiOmxd79d0TgUyCE0wuKGr3"
```

---

### HOW TO BUILD, SPIN, WATCH LOGS, etc

---

- Prerequisites: 
  - Need docker at-least, so please install [docker](https://docs.docker.com/get-docker/)
  - I am assuming you are using Unix like system. 

- Before running the project add `.env.local` file at project root directory and copy contents of `.env.example` file using:
  - `cat .env.example | tee .env.local`. Note that this command might not work properly on Windows, it's better to create `.env.local` by hand.

- Run the project (Using `docker-compose`):
  - `docker-compose up`. But remember to add `.env.local` file at project root directory and copy contents of `.env.example` file as already mentioned in the first step. Otherwise the build will fail.

  - Run test cases:
    - `docker-compose run pokemon_container bash -c "cd project &&  python3 manage.py test --no-input"` 

- Run the project (Using `docker` commands):
  - Create a network `docker network create --driver bridge pokemon_network` 

  - Run db `docker run -dit --rm --network pokemon_network --env-file .env.local -p 5432:5432 --name pokemon_db postgres` 

  - Run redis `docker run -dit --rm -p 6379:6379 --network pokemon_network --name pokemon_redis redis:alpine3.13`

  - Build api server `docker build -t pokemon_image .` 
  - Run api server `docker run -dit --rm -p 5000:8000 --network pokemon_network --volume (pwd)/project:/home/pokemon/project --name pokemon_container pokemon_image` 

  - Run tests, `docker exec -it pokemon_container bash -c "cd project && python3 manage.py test --no-input --keepdb"` 

  - Optional commands, use as per need:
    - Stop api server `docker container stop pokemon_container` 
    - Stop db `docker container stop pokemon_db` 
    - Stop redis `docker container stop pokemon_redis` 
    - See logs `docker container logs -ft pokemon_container` 
 
 
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

---

## Production checklist

---

- [ ] add logging
- [ ] add sentry 
- [ ] add travis CI
- [ ] do some profiling and load testing
- [ ] use dependabot for keeping dependencies fresh

---

### Load test results 

---

- Before using caching (100 requests in total, concurrency=10):
```
ash@Ashishs-MacBook-Pro ~> loadtest -n 100 -k -c 10 http://localhost:5000/pokemon/mewtwo
[Mon Jul 05 2021 07:57:21 GMT+0900 (Japan Standard Time)] INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Target URL:          http://localhost:5000/pokemon/mewtwo
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Max requests:        100
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Concurrency level:   10
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Agent:               keepalive
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Completed requests:  100
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Total errors:        0
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Total time:          3.099425439 s
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Requests per second: 32
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Mean latency:        304.7 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO Percentage of the requests served within a certain time
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO   50%      284 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO   90%      428 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO   95%      466 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO   99%      511 ms
[Mon Jul 05 2021 07:57:24 GMT+0900 (Japan Standard Time)] INFO  100%      511 ms (longest request)
```

- After using caching (100 requests in total, concurrency=10):
```
ash@Ashishs-MacBook-Pro ~> loadtest -n 100 -k -c 10 http://localhost:5000/pokemon/mewtwo
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Requests: 0 (0%), requests per second: 0, mean latency: 0 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Target URL:          http://localhost:5000/pokemon/mewtwo
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Max requests:        100
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Concurrency level:   10
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Agent:               keepalive
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Completed requests:  100
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Total errors:        0
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Total time:          0.660191959 s
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Requests per second: 151
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Mean latency:        61.9 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO Percentage of the requests served within a certain time
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO   50%      24 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO   90%      216 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO   95%      393 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO   99%      407 ms
[Mon Jul 05 2021 08:46:54 GMT+0900 (Japan Standard Time)] INFO  100%      407 ms (longest request)
```
- Using cache has improved the mean latency from 304.7 ms to 61.9 ms which is about 5 times faster. 
- Using cache has increase number of requests per second handled by system from 32 requests to 151 requests which is 5 times more.

---

### NOTES

---

- [x] comply
- [x] check if django user in docker really needed 
- [x] manage secrets using .env file
- [x] add tests as per compliance
- [x] cache
