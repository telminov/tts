# docker build -t bm0/voice-synthesizer .
# docker push bm0/voice-synthesizer
# docker run -ti --rm --name voice -v /var/docker/voice/data/:/data/ -v /var/docker/voice/conf/:/conf/ -v /var/docker/voice/output/:/output -p 8000:80 bm0/voice-synthesizer
FROM ubuntu:16.04
MAINTAINER bm0 <bm0@soft-way.biz>

# Setting the locale
RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

EXPOSE 80
VOLUME /output
VOLUME /data
VOLUME /conf
VOLUME /static

# install dependencies
RUN apt-get update &&\
    apt-get install -y python3-pip git nginx scons gcc libpulse-dev libao-dev portaudio19-dev vim supervisor

# install RHVoice
RUN git clone https://github.com/Olga-Yakovleva/RHVoice.git /opt/RHVoice
WORKDIR /opt/RHVoice
RUN scons && scons install && ldconfig

# copy source and install requirements
COPY . /opt/voice-synthesizer
WORKDIR /opt/voice-synthesizer
COPY conf/supervisor.conf /etc/supervisor/conf.d/voice-synthesizer.conf
COPY conf/nginx.conf /etc/nginx/sites-enabled/voice-synthesizer
RUN rm /etc/nginx/sites-enabled/default
RUN pip3 install -r requirements.txt

# Starting the server
CMD test "$(ls /conf/settings_local.py)" || cp /opt/voice-synthesizer/project/local_settings.sample.py /conf/settings_local.py;\
    ln -s /conf/settings_local.py project/settings_local.py;\
    rm -rf generated; ln -s /output generated;\
    service nginx restart;\
    python3 ./manage.py migrate;\
    python3 ./manage.py collectstatic --noinput;\
    /usr/bin/supervisord --nodaemon