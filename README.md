## MUST DO
- [ ] comply
- [ ] check if django user in docker really needed
- [ ] manage secrets using docker
- [ ] add tests for sure
- [ ] cache


## HOW TO BUILD, SPIN, WATCH LOGS, etc
- Build : `docker build -t pokemon-image .` 
- Run : `docker run --rm -d -p 5000:8000 --volume /Users/ashish/Desktop/ash/pokemon/project:/home/pokemon/project --name pokemon-container pokemon-image` 
- Watch logs: `docker container logs -ft pokemon-container` 
- Exec: `docker exec -it pokemon-container bash`
- Restart: `docker container restart pokemon-container`
- Stop: `docker container stop pokemon-container`


## OVER KILL ?
- [ ] use dependabot
- [ ] use travis
- [ ] logging
- [ ] sentry 
- [ ] profiling needed ?
- [ ] deploy ?
- [ ] is db needed ? 