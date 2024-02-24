FROM python:3.12 AS requirements-stage

ARG package_name=tcp_dummy_services
ARG module_name=tcp_dummy_services

# Create structure and install poetry
WORKDIR /tmp
RUN mkdir projects
RUN pip install poetry

# Build requirements
COPY ./pyproject.toml ./poetry.lock* ./projects/${package_name}/
RUN cd projects/${package_name} && poetry export -f requirements.txt --output requirements.txt --without-hashes
# ---------------------------------

# Build execution container
FROM python:3.12-alpine

# ARGs are needed for all the stages
ARG package_name=tcp_dummy_services
ARG module_name=tcp_dummy_services

WORKDIR /code
ENV PYTHONPATH=/code

# Install requirements
COPY --from=requirements-stage /tmp/projects/${package_name}/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code

