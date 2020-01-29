#!/bin/sh

cat <<EOF > /etc/init.d/start_printerest_client.sh
#!/bin/sh
### BEGIN INIT INFO
# Provides:          printerest_client
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

pip3 install requests
python3 $PWD/client.py

EOF

chmod +x /etc/init.d/start_printerest_client.sh
ln -s /etc/init.d/start_printerest_client.sh /etc/rc.d/
