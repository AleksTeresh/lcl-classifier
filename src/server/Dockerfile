FROM rust:1.46.0 as re

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN git clone https://github.com/AleksTeresh/round-eliminator .
RUN rustup install nightly
RUN RUSTFLAGS="-C target-cpu=native" cargo +nightly build -p re-rust2py --release

FROM python:3.8.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY --from=re /usr/src/app/target/release/librust2py.so /usr/src/app/rust2py.so
COPY requirements.txt lcl_classifier.ini /usr/src/app/
RUN pip install -r requirements.txt
COPY . .
RUN ls -l

ENTRYPOINT [ "uwsgi" ]
CMD ["--ini=lcl_classifier.ini"]
