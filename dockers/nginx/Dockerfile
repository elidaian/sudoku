FROM nginx:latest

MAINTAINER Eli Daian "elidaian@gmail.com"

# Add static website content
RUN mkdir -p /var/edsudoku/static /var/edsudoku/fonts

# Add static bootstrap contents
ADD https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip /tmp/
RUN unzip /tmp/bootstrap-3.3.5-dist.zip
RUN cp /tmp/bootstrap-3.3.5-dist/css/* /var/edsudoku/static
RUN cp /tmp/bootstrap-3.3.5-dist/js/* /var/edsudoku/static
RUN cp /tmp/bootstrap-3.3.5-dist/fonts/* /var/edsudoku/fonts

# Add static jQuery contents
ADD http://code.jquery.com/jquery-2.1.4.min.js /var/edsudoku/static/

COPY nginx.conf /etc/nginx/nginx.conf
