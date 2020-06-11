# pull official base image
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working directory
WORKDIR auth

# install dependencies using cache for faster build
COPY auth/Pipfile .
COPY auth/Pipfile.lock .
RUN pipenv install --system --deploy

# copy everything else
ADD auth .

# and grpc api
COPY api api
