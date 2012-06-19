#
# Regular cron jobs for the fotoshare package
#
0 4	* * *	root	[ -x /usr/bin/fotoshare_maintenance ] && /usr/bin/fotoshare_maintenance
