# pull official base image and pipenv
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /online-store

# install dependencies using cache for faster build
COPY online-store/Pipfile Pipfile
COPY online-store/Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

# copy everything else
ADD online-store .

# and grpc api
COPY api api
