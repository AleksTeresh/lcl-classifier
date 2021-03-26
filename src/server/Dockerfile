# adopted from https://stackoverflow.com/a/54763270
FROM python:3.8.3

ENV POETRY_VERSION=1.0.0
RUN pip install "poetry==$POETRY_VERSION"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi
COPY . .
RUN rm /usr/src/app/rust2py.so
COPY ./rust2py-linux.so /usr/src/app/rust2py.so

ENTRYPOINT [ "uwsgi" ]
CMD ["--ini=lcl_classifier.ini"]
