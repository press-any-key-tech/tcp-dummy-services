# tcp-dummy-services

Dummy services for testing connectivity on cloud providers:
- TCP echo service
- HTTP crud service
- WEBSOCKETS crud service

## A bit of history

Some time ago, I had to conduct a proof of concept to determine the best way to publish several dozen services, of different types, on the internet: HTTP, WebSocket, and TCP in general.

Testing with the production services was almost impossible since, at that time, they were published on-premises and would require, as a first step, publishing those same services in a cloud environment.

The best way to test how to configure internet connectivity securely, in this case, is to use simulated services that cover the types of connectivity to be tested.

And thus, this project was born.

## Technology Stack:

- Python
- Fastapi
- Uvicorn
- Docker
- Pytest (\*)

## Development environment

### Requirements:

- Docker CE (Linux) or Docker Desktop (MacOS, Windows).
- Python >= 3.12 (Pyenv, best option)
- Poetry as dependency manager

### Activate development environment

```
poetry install
```

This will create a new virtual environment (if it does not exists) and will install all the dependencies.

To activate the virtual environment use:

```
poetry shell
```

### Add/remove dependencies

```
poetry add PIP_PACKAGE [-G group.name]
```

Add dependency to the given group. If not specified will be added to the default group.

```
poetry remove PIP_PACKAGE [-G group.name]
```

Remove dependency from the given group

### Run TCP project from command line

```

poetry run python ./src/aws_tcp_dummy_services/ 7000

```

### Run HTTP project from command line

```
uvicorn tcp_dummy_services.http.main:app --host 0.0.0.0 --port 8080
```





### Debug project from VS Code

First create a .env file in the root folder or copy the existing .env.example and set the required variables

Then use the Launch option from Visual Studio Code

## Tests

### Debug From VS Code

Get the path of the virtual environment created by poetry:

```bash
poetry env info -p
```

Set in visual studio code the default interpreter to the virtual environment created by poetry.(SHIT+CTRL+P Select interpreter)

Launch "Pytest launch" from the run/debug tab.

You can set breakpoints and inspections

## Docker build and run

### Build

From root directory execute:

```bash
docker build -f ./docker/Dockerfile -t tcp-dummy-services:latest .
```

### Run

From root directory execute:

```bash
docker run -d -p 7000:7000 --name tcp-dummy-services tcp-dummy-services:latest
```

Change entrypoint to execute both http and ws services


Do not use "localhost" as LOCAL_SERVER_IP, use your local IP address instead. Docker container will not be able to connect to your local database otherwise.


## Test websockets

### Create

```json
{
    "action": "create",
    "data": {
        "id": "1",
        "name": "Test 1"
    }
}
```

### Read

```json
{
    "action": "read",
    "id": "1"
}
```

## Test TCP (Echo)

Send characters and finish each line with ENTER.

To disconnect use one of these commands (in uppercase): END, QUIT, EXIT, ADIOS, BYE

## Test HTTP

Swagger explorer on /docs path. Example: http://localhost:8000/docs

