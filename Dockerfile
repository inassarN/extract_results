FROM ubuntu:16.04

RUN apt update && apt install -y python python-numpy python-scipy

ADD /extract_results.py /usr/bin/
