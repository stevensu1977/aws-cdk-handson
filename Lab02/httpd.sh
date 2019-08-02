#!/bin/sh

#install httpd
yum install httpd -y

#enable and start httpd
systemctl enable httpd
systemctl start httpd

echo "Welcome AWS $(hostname -f) " >  /var/www/html/index.html
echo "<hr>" >>  /var/www/html/index.html
curl http://169.254.169.254/latest/meta-data/public-hostname >> /var/www/html/index.html
