FROM maven:3.5.0-jdk-8

WORKDIR /apps
COPY . /apps
CMD tail -f /dev/null
RUN apt-get -y update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask
ENTRYPOINT [ "python3" ]

CMD [ "aadhar-api.py" ]

