FROM ubuntu:16.04

RUN apt-update && apt install -y python python-numpy python-scipy
