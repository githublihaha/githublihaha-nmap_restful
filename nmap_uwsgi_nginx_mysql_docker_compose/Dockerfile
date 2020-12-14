FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN  sed -i s@/deb.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN  apt-get clean && apt-get update && apt-get install -y  nmap net-tools --auto-remove $buildDeps && rm /var/log/dpkg.log /var/log/alternatives.log /var/log/apt/*.log
WORKDIR /root/.pip
COPY ./app /app
WORKDIR /root/.pip
RUN  echo  '[global] \n\
index-url = https://pypi.tuna.tsinghua.edu.cn/simple' \
>> pip.conf
WORKDIR /app
RUN pip install -r requirements.txt
