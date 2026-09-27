# Problem: Python error log location

**Date:** 2026-09-28

**Source:** Stack Overflow

**Category:** devops

**Why Selected:** Trending problem in devops category

## Description

I am developing a python application on flask framework. And I use .wsgi to deploy it. I got confused by error log locations. It looks like Python errors and debug information are put into different log files. First of all, I specify both access and error log locations in the apache vhost file. <VirtualHost *:myport> ... CustomLog /homedir/access.log common ErrorLog /homedir/error.log ... </VirtualHost> I also know there is another apache error log, /var/log/httpd/error_log . My access logs were

## Original URL

https://stackoverflow.com/questions/22334440/python-error-log-location
