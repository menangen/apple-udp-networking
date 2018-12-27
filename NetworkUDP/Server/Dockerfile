FROM python:alpine

MAINTAINER Menangen <menangen@gmail.com>

WORKDIR /opt/app/

COPY requirements.txt /opt/app/

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY *.py /opt/app/

CMD [ "python", "/opt/app/udp_blocking.py" ]