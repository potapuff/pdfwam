#!/bin/bash
if [ `whoami` != "root" ];
then
echo "Run the script as root or sudo user"
exit 1
fi

echo "Adding tingtun user..."
/usr/bin/tingtunuser.sh
echo "Installing init scripts..."
cp -p scripts/* /etc/init.d
echo "Making log folders..."

LOGFOLDER="/var/log/tingtun/pdfwam"
mkdir -p $LOGFOLDER
# Make them writeable by tingtun user
chown tingtun:tingtun -R /var/log/tingtun

CACHEFOLDER="/var/local/cache/tingtun/pdf-wam/"
if [ ! -d "$CACHEFOLDER" ];
then
    echo "Making cache folders ..."
    mkdir -p $CACHEFOLDER
    chown tingtun:tingtun /var/local/cache/tingtun/
fi

# Copy DB file
echo "Creating location for Tingtun DB files..."
mkdir -p /var/tingtun/db
echo "Copying PDF WAM db..."
cp pdfwam_log.db  /var/tingtun/db/
chown tingtun:tingtun -R /var/tingtun/

# Add to startup scripts - Assume debian system
update-rc.d -n pdfwam defaults
echo "Done."
