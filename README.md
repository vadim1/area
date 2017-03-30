# area
The Area Method Application for Making Important Decisions

# Setting up Social account
    1. Add more and more providers in installed app e.g. allauth.socialaccount.providers.facebook
    2. Get app id and secret code from their website see http://django-allauth.readthedocs.io/en/latest/providers.html
    3. Go to admin portal and add those credential one after other

# Email setting
    1. EMAIL_HOST_USER = 'test@example.com'
    2. EMAIL_HOST_PASSWORD = 'example'
    3. EMAIL_HOST = "imap.example.net"
    4. EMAIL_PORT = 465

# Database setting
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'database_name',
            'USER': 'database_username',
            'PASSWORD': 'database_password',
            'HOST': 'database_host',
            'PORT': database_port,
        }
    }
# Installation Nginx
    1. Installed Nginx, Gunicorn
    2. Configure Gunicorn with wsgi app
    3. Configure Nginx proxy with Gunicorn socket
    4. Configure Nginx with SSL and redirect all http traffic to https

    `server {
            listen 80;
            server_name app.areamethod.com;
            access_log /var/log/nginx/access.log;
            error_log /var/log/nginx/error.log;
            return 301 https://$host$request_uri;
    }
    server {
            listen  443 ssl;

            server_name  app.areamethod.com;

            ssl_certificate    /etc/nginx/ssl/ssl.cert;
            ssl_certificate_key    /etc/nginx/ssl/ssl.key;

            access_log /var/log/nginx/https-access.log;
            error_log /var/log/nginx/https-error.log;

            location = /favicon.ico { access_log off; log_not_found off; }

            location /static {
                    alias /home/ubuntu/area/static;
            }

            location / {
                    proxy_redirect     off;
                    proxy_set_header   Host              $host;
                    proxy_set_header   X-Real-IP         $remote_addr;
                    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
                    proxy_pass http://unix:/home/ubuntu/area/area.sock;
            }
    }


# Gunicorn command : Django app is served via this
    1. sudo service gunicorn status : Give the status Gunicorn (You can see running/stoped/failed)
    2. sudo service gunicorn restart : Restart Gunicorn
    3. sudo service gunicorn start :  Start WSGI Gunicorn
    4. sudo service gunicorn stop  : Stop WSGI Gunicorn

# Nginx command
    1. similar command exist for nginx( replace gunicorn with nginx)

# Once you change static file then don't forgot to run below command 
    python manage.py collectstatic
