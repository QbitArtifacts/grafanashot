FROM debian:bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3-pip \
    python3-venv \
    firefox-esr


COPY . /code

WORKDIR  /code

RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]

