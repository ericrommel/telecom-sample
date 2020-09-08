# pull official base image
FROM python:3.8.1

# set working directory
WORKDIR /c/users

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install"]

# add app
COPY . .

EXPOSE 5000

# run server
CMD ["flask", "run", "--host", "0.0.0.0"]