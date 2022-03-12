FROM  python:3.7 as builder2

WORKDIR /home


RUN sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com#g' /etc/apt/sources.list
RUN sed -i 's#http://security.debian.org#http://mirrors.aliyun.com#g' /etc/apt/sources.list
RUN apt update
RUN apt update &&  apt-get install -y supervisor iputils-ping vim\
    curl net-tools netcat-traditional telnet libpq-dev libjpeg-dev  libpng-dev libgl1-mesa-glx && \
    mkdir -p ~/.pip/ && touch ~/.pip/pip.conf &&\
    echo "[global]" >> ~/.pip/pip.conf &&\
    echo "index-url = https://pypi.douban.com/simple" >> ~/.pip/pip.conf &&\
    pip3 install --upgrade pip


ENV TZ Asia/Shanghai
ENV SERVICE_NAME fund
ENV SERVICE_VERSION 0.1

ADD ./ /home/fund

RUN mkdir -p /var/filebeat/log &&\
    mkdir -p /var/log/fund &&\
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo "Asia/Shanghai" > /etc/timezone &&\
    echo "files = /home/fund/prod/launch/supervisor.d/*.ini" >> /etc/supervisor/supervisord.conf

ADD ./prod/launch/supervisor.d/*.conf /etc/supervisor/conf.d/

ENTRYPOINT ["/usr/bin/supervisord", "-n"]



FROM builder2

WORKDIR /home

ADD ./requirements.txt /home/requirements.txt
RUN pip3 install -r requirements.txt

ADD ./ /home/fund

EXPOSE 5000