# tcp-dummy-services

Dummy services to test connectivity on cloud providers

## Technology Stack:

- Python
- Docker
- Pytest (\*)
- PostgreSql/Mysql

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

### Run project from command line

```

poetry run python .\src\aws_tcp_dummy_services\ 7000

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

Do not use "localhost" as LOCAL_SERVER_IP, use your local IP address instead. Docker container will not be able to connect to your local database otherwise.
