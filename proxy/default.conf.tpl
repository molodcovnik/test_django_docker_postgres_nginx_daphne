server {
    listen ${LISTEN_PORT};

    location /static/ {
        alias /vol/static/;
    }

    location / {
        proxy_pass      http://${APP_HOST}:${APP_PORT};
        include         /etc/nginx/proxy_params;
    }

    location /ws/ {
        proxy_pass http://${APP_HOST}:${APP_PORT};
        proxy_http_version 1.1;
        include         /etc/nginx/proxy_params;
    }
}