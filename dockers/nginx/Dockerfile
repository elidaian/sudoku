FROM nginx:latest

MAINTAINER Eli Daian "elidaian@gmail.com"

# Add static website content
RUN mkdir -p /var/edsudoku

COPY ../../src/edsudoku/server/fonts /var/edsudoku/fonts
COPY ../../src/edsudoku/server/static /var/edsudoku/static
COPY nginx.conf /etc/nginx/nginx.conf
