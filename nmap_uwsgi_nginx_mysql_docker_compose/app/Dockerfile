FROM ubuntu:20.04
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN  apt-get clean && apt-get update && apt-get install -y python3 python3-pip git nmap net-tools --auto-remove $buildDeps && rm /var/log/dpkg.log /var/log/alternatives.log /var/log/apt/*.log
WORKDIR /root/.pip
RUN  echo  '[global] \n\
index-url = https://pypi.tuna.tsinghua.edu.cn/simple' \
>> pip.conf
WORKDIR /
RUN  git clone https://github.com/githublihaha/nmap_restful.git
WORKDIR /nmap_restful
RUN  pip3 install -r requirements.txt
EXPOSE  5000
CMD python3 run.py


