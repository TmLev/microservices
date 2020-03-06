# pull official base image
FROM python

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /online-store
COPY . .

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
