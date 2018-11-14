Steps to bring the service up and running

1. Installi Docker CE
Link for the same: https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac

2. Install Docker compose
For MAC:
	brew install docker-compose

For Windows:
	Link for the same: https://docs.docker.com/compose/install/

Bring the docker service up and running

3. Go to the assigments folder and run:
docker-compose build

4. Then bring the services of the application up by running the below command.(It may take some time to build)
docker-compose up

5. Go to browser and type http://127.0.0.1:32001/
it should return string "It Works"

6. Api to get fibonacci numbers between index 2 and 5 is http://127.0.0.1:32001/fib/2/5 
It returns: {"fibonacci_numbers": [2, 3, 5]}

7. To bring down the services 
docker-compose down
