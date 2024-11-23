FROM python:3.10.14

RUN pip install --upgrade typing-extensions
RUN pip install dict2xml
RUN pip install connexion[flask] connexion[swagger-ui] connexion[uvicorn]
RUN pip install flask-restplus
RUN pip install Flask

COPY ./src /src
COPY ./json /json
COPY ./main.py .
COPY ./swagger.yaml .

CMD ["python", "main.py"]