# docker build -t voice-synthesizer .
FROM ubuntu:16.04
MAINTAINER bm0 <bm0@soft-way.biz>

# Setting the locale
RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

EXPOSE 80
VOLUME /opt/voice-synthesizer/generated_wav/
VOLUME /data
VOLUME /conf
VOLUME /static

# install dependencies
RUN apt-get update &&\
    apt-get install -y python3-pip git nginx scons gcc libpulse-dev libao-dev portaudio19-dev

# install RHVoice
WORKDIR /opt
RUN git clone https://github.com/Olga-Yakovleva/RHVoice.git

WORKDIR /opt/RHVoice
RUN scons && scons install && ldconfig

# copy source and install requirements

COPY . /opt/voice-synthesizer
WORKDIR /opt/voice-synthesizer
RUN cp conf/nginx.conf /etc/nginx/sites-enabled/voice-synthesizer
RUN rm /etc/nginx/sites-enabled/default
RUN pip3 install -r requirements.txt

# Starting the server
CMD test "$(ls /conf/settings_local.py)" || cp conf/sample.settings_local.py /conf/settings_local.py;\
    ln -s /conf/settings_local.py project/settings_local.py;\
    service nginx restart;\
    python3 ./manage.py collectstatic --noinput;\
    gunicorn project.wsgi --bind=127.0.0.1:8000 --workers=5