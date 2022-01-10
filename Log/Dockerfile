# Log Dockerfile
# Pull base image.
FROM ubuntu:latest


# Update the system 
RUN apt-get -y update        # Fetches the list of available updates 
RUN apt-get -y upgrade       # Strictly upgrades the current packages 
RUN apt-get -y dist-upgrade  # Installs updates (new ones)

# install basic apps, one per line for better expirence
RUN apt-get -y install net-tools
RUN apt-get -y install iproute2
RUN apt-get -y install iputils-ping
RUN apt-get -y install sudo
RUN apt-get -y install vim

# install supervisor for launch multiple command
RUN apt-get -y install supervisor
RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY supervisord2.conf /etc/supervisor/supervisord.conf

# Install Python.
RUN apt-get update && apt-get install -y python python-setuptools python-pip

# Install netifaces package
RUN python -m pip install netifaces

# copy the whole contentent of Shareholder-Scripts in to  /home-user/ path
COPY Shareholder-Scripts/  /home-user/

# creating user-script dir
RUN mkdir /user-script


# add simple-user
# RUN groupadd -g 999 simple-user && useradd -r -u 999 -g simple-user simple-user
RUN groupadd -r user -g 1000 &&\
  useradd -u 1000 -r -g user -m -d /home-user -s /sbin/nologin -c "App user" user && \
  chmod 755 /home-user
  
# set password for simple-user
# RUN echo "simple-user:docker" | chpasswd

# seu the root password
# oss: if you want to root privalge when you are inside the container: su -c /bin/bash and type password
RUN echo "root:docker" | chpasswd

# from this step the containers start in simple-user mode
USER user

# creating dir log_supervisord where to put log_supervisord's log
RUN mkdir /home-user/log_supervisord/
RUN chmod 755 /home-user/log_supervisord/

# creating data_users dir
RUN mkdir /home-user/data_users/
RUN chmod 755 /home-user/data_users/

# Define default command.
# Docker has a default entrypoint which is /bin/sh -c but does not have a default command.
# The command is run via the entrypoint. i.e., the actual thing that gets executed is /bin/sh -c python /usr/src/app/app.py
# CMD ["python","/usr/src/app/app.py"]
# CMD ["/bin/bash"]
# we use supervisor in order to launch python script and bash shell, so if the python fails or stop the container still alives
CMD ["/usr/bin/supervisord"]
