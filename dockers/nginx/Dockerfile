FROM nginx:latest

MAINTAINER Eli Daian "elidaian@gmail.com"

# Add static website content
RUN mkdir -p /var/edsudoku

COPY fonts /var/edsudoku/fonts
COPY static /var/edsudoku/static
COPY nginx.conf /etc/nginx/nginx.conf
