FROM ubuntu:20.04

MAINTAINER Koorye <a1311586225@gmail.com>

COPY requirements.txt /tmp
WORKDIR /tmp

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt clean && apt update
RUN apt install -y iputils-ping
RUN apt install -y python3 python3-dev python3-pip
RUN pip3 install -r requirements.txt

COPY simplekv simplekv

WORKDIR simplekv
ENTRYPOINT ["python3", "app.py"]
CMD ["--host", "(host)", "--all-hosts", "(host1)", "(host2)", "(host3)"]
