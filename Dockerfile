FROM phusion/baseimage

RUN apt-get update
RUN apt-get -y install python-pip
RUN pip install npyscreen

# enable ssh
RUN rm -f /etc/service/sshd/down
RUN /usr/sbin/enable_insecure_key
EXPOSE 22

CMD ["/sbin/my_init"]