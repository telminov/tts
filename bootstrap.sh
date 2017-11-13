#! /bin/bash

# copy the configuration to the host machine, if it is not there
if [ ! -f /conf/settings_local.py ]
    then
        cp /opt/tts/project/local_settings.sample.py /conf/settings_local.py
fi
if [ ! -f /conf/RHVoice.conf ]
    then
        cp /usr/local/etc/RHVoice/RHVoice.conf /conf/RHVoice.conf
fi
if [ ! -f /conf/nginx.conf ]
    then
        cp /etc/nginx/sites-enabled/tts /conf/nginx.conf
fi
if [ ! -f /conf/supervisor.conf ]
    then
        cp /etc/supervisor/conf.d/tts.conf /conf/supervisor.conf
fi

# slip the new configuration
ln -sf /conf/settings_local.py project/settings_local.py
ln -sf /conf/RHVoice.conf /usr/local/etc/RHVoice/RHVoice.conf
ln -sf /conf/nginx.conf /etc/nginx/sites-enabled/tts
ln -sf /conf/nginx.conf /etc/nginx/sites-enabled/tts
ln -sf /conf/supervisor.conf /etc/supervisor/conf.d/tts.conf

# run service
service nginx restart
python3 ./manage.py migrate
python3 ./manage.py collectstatic --noinput
/usr/bin/supervisord --nodaemon
