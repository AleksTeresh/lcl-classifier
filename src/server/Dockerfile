FROM python:3.8.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt lcl_classifier.ini /usr/src/app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "uwsgi" ]
CMD ["--ini=lcl_classifier.ini"]
