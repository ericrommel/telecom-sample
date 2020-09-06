FROM python:3.8
COPY . .
WORKDIR . .
RUN ["pip", "install", "pipenv"]
ENV FLASK_APP=run.py
EXPOSE 5000
RUN ["pipenv", "install"]
CMD ["flask", "run", "--host", "0.0.0.0"]