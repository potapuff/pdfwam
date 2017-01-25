
""" Local configuration for PDF wam. We are not relying
on old Egovmon system configuration anymore.

"""

pdfwamservers='localhost:8893'
pdfwamvalidateimgs=1
pdfwamignoresinglebitimgs=0
pdfwamurlcache=1
pdfwamurlcachefolder='/var/local/cache/tingtun/pdf-wam'
pdfwamlogfile='pdfwam.log'
pdfwamurlcachettl=24
# Maximum size in MB for a PDF file.
pdfmaxsize=10
pdfwamloglevel='info'
dbfile='/var/tingtun/db/pdfwam_log.db'
# static (temp) files prefix
staticprefix='http://testui.eiii.eu/static/temp/'












