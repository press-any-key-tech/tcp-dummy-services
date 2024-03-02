# tcp-dummy-services

Dummy services for testing connectivity on cloud providers:

- TCP echo service
- HTTP crud service
- HTTP to HTTP crud service
- WEBSOCKETS crud service

## A bit of history

Some time ago, I had to conduct a proof of concept to determine the best way to publish several dozen services, of different types (HTTP, WebSocket, and TCP in general), on different cloud providers.

Testing with the production services was almost impossible because they were published on-premises and would require, as a first step, publishing those same services in a cloud environment.

The best way to test how to configure internet connectivity securely, in this case, was to use create a series of minimal services to simulate the real services to be tested.

And thus, this project was born.

## Code repository

[tcp dummy services](https://github.com/press-any-key-tech/tcp-dummy-services)

## How to use this image

### HTTP

Launch a simple http service.

```
docker run -d -p 8000:8000 --name http-dummy-services tcp-dummy-services:latest sh -c "uvicorn tcp_dummy_services.http.main:app --host 0.0.0.0 --port 8000"
```

### HTTP to HTTP

Launch an HTTP service that calls another http service.

```
docker run -d -p 8002:8002 --name http-remote-dummy-services -e STUFF_ENABLED=true -e THINGS_ENABLED=false -e THINGS_BASE_URL=http://http-dummy-services:8000 tcp-dummy-services:latest sh -c "uvicorn tcp_dummy_services.http.main:app --host 0.0.0.0 --port 8002"
```

### Websocket

Launch a websockets service.

```
docker run -d -p 8001:8001 --name ws-dummy-services tcp-dummy-services:latest sh -c "uvicorn tcp_dummy_services.ws.main:app --host 0.0.0.0 --port 8001"
```

### TCP

Launch a TCP echo service.

```
docker run -d -p 7001:7001 --name tcp-dummy-services tcp-dummy-services:latest sh -c "python /code/tcp_dummy_services/tcp/"
```
## Environment variables

LOG_LEVEL: log level, default is INFO

ROOT_PATH (HTTP): root path for the application (is it behing a proxy?). Default "".
STUFF_ENABLED (HTTP): Stuff controller enabled. Default: false.
THINGS_ENABLED (HTTP): Things controller enabled. Default: true
THINGS_BASE_URL (HTTP): Things url, for Remote calls from Stuff. Default ""

TCP_PORTS (TCP): TCP open ports. One single port or a range separated by "-".

## Test Services

### Test HTTP

Swagger explorer on /docs path. Example: http://localhost:8000/docs

There are two objects:
- Thing: a simple object that allows CRUD operations.
- Stuff: a remote object that calls (using HTTP) the Thing service.


### Websockets

Tested using Postman on url `ws://localhost:8001/`

Create a "Thing".

```json
{
  "action": "create",
  "data": {
    "id": "1",
    "name": "Test 1"
  }
}
```

Read a "Thing"

```json
{
  "action": "read",
  "id": "1"
}
```

Update a "Thing"

```json
{
  "action": "update",
  "id": "1",
  "data": {
    "id": "1",
    "name": "Test 1 Modified"
  }
}
```

Delete a "Thing"

```json
{
  "action": "delete",
  "id": "1"
}
```

### Test TCP (Echo)

Tested using telnet on port 7001

```bash
telnet localhost 7001
```

Send characters and finish each line with ENTER.

To disconnect use one of these commands (in uppercase): END, QUIT, EXIT, ADIOS, BYE

## Example docker compose

```yaml
version: '3.8'
services:
  http:
    networks:
      - app-network
    image: pressanykeytech/tcp-dummy-services:latest
    command:
      [
        "uvicorn",
        "tcp_dummy_services.http.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ]
    ports:
      - 8000:8000
    environment:
      - LOG_LEVEL=DEBUG
      - LOGGER_NAME=tcp-dummy-services
      - STUFF_ENABLED=false

  ws:
    networks:
      - app-network
    image: pressanykeytech/tcp-dummy-services:latest
    command:
      [
        "uvicorn",
        "tcp_dummy_services.ws.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8001"
      ]
    ports:
      - 8001:8001
    environment:
      - LOG_LEVEL=DEBUG
      - LOGGER_NAME=tcp-dummy-services

  remote_http:
    networks:
      - app-network
    image: pressanykeytech/tcp-dummy-services:latest
    command:
      [
        "uvicorn",
        "tcp_dummy_services.http.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8002"
      ]
    ports:
      - 8002:8002
    environment:
      - LOG_LEVEL=DEBUG
      - LOGGER_NAME=tcp-dummy-services
      - STUFF_ENABLED=true
      - THINGS_ENABLED=false
      - THINGS_BASE_URL=http://http:8000
  tcp:
    networks:
      - app-network
    image: pressanykeytech/tcp-dummy-services:latest
    command: [ "python", "/code/tcp_dummy_services/tcp/" ]
    ports:
      - 7001:7001
      - 7002:7002
      - 7003:7003
    environment:
      - LOG_LEVEL=DEBUG
      - LOGGER_NAME=tcp-dummy-services
      - TCP_PORTS=7001-7003

networks:
  app-network:
    driver: bridge

```
