FROM ubuntu:16.04

RUN apt update && apt install -y python python-numpy python-scipy

ADD /extract_results.py /usr/bin/

#ENTRYPOINT ["python", "/usr/bin/extract_results.py"]
#CMD ["/home/nimbix/data/8in_00"]

