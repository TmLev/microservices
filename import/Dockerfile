# pull official base image and pipenv
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /import

# install dependencies using cache for faster build
COPY import/Pipfile Pipfile
COPY import/Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

# copy everything else
ADD import .
