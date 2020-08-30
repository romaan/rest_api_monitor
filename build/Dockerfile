FROM ubuntu:18.04

EXPOSE 80/tcp

RUN apt update
RUN apt install -y python3 python3-pip supervisor nginx pkg-config wget

RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xvzf redis-stable.tar.gz
RUN cd redis-stable && make && make install

COPY supervisor/* /etc/supervisor/conf.d/
COPY nginx/nginx.conf /etc/nginx/sites-available/default

COPY webapp /opt/webapp
COPY webui /opt/webui
COPY startup.sh /opt

RUN chmod u+x /opt/startup.sh
WORKDIR /opt/webapp

RUN pip3 install -r requirements.txt

CMD /opt/startup.sh