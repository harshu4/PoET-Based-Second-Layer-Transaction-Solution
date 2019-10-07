FROM test


CMD tail -f /dev/null
RUN apt-get -y update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask

COPY . /apps

WORKDIR /apps
RUN echo fc747a11f43f7686c78b07f784cc3ffdb712ef79d8beb119adf42e90cc4c2664 > priv.txt
EXPOSE 8080
ENTRYPOINT [ "python3" ]

CMD [ "bank.py" ]
