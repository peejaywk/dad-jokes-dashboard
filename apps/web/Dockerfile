FROM nginx/nginx-unprivileged:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY version.txt /usr/share/nginx/html/version.txt
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 8080
