# pull official base image and pipenv
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /upload

# install dependencies using cache for faster build
COPY upload/Pipfile Pipfile
COPY upload/Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

# copy everything else
ADD upload .

# and grpc api
COPY api api
