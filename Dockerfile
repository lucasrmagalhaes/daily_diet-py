# Dockerfile
FROM python:3-alpine3.17

WORKDIR /src

# Dica: instale primeiro as dependências antes de copiar todo projeto
COPY src/*requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Este argumento será passado dentro do docker-compose
ARG FLASK_ENV
RUN if [ "$FLASK_ENV" = "dev" ] ; then pip install --no-cache-dir -r dev-requirements.txt  ; fi

COPY ./src .

CMD ["python3", "app.py"]