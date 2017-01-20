""" Get PDF-WAM usage stats from the remote server """

import sqlite3
import os, sys
import cPickle
import signal

db_path = 'tt2.s.tingtun.no:/var/tingtun/db/pdfwam_log.db'
hosts = {}

def sighandler(signum, stack):
    """ Signal handler """

    print 'Caught signal. Exiting.'
    if signum in (signal.SIGINT, signal.SIGTERM,):
        cPickle.dump(hosts, open('hosts.pckl','wb'))
    sys.exit(1)
    
def get_remote_db():
    """ Grab a copy of the remote sqlite3 pdfwam database """

    print 'Grabbing a copy of PDF WAM remote database...'
    cmd = 'rsync --compress --checksum --update --progress %s .' % db_path
    os.system(cmd)

def find_stats(check_hosts=False):
    """ Find statistics """
    global hosts
    
    conn = sqlite3.connect("pdfwam_log.db")
    # Get a report of URL, IP address, visit time of the entries
    curs = conn.cursor()
    curs.execute('SELECT url, ip_address, visit_time from tracking_visit order by ip_address desc;')

    entries = []

    f = open('pdfwamstats.csv','wb')
    f.write("@@@".join(('URL','IP Address','Time-stamp','Host Information','DNS-Stuff URL')) + '\n')
            
    if os.path.exists('hosts.pckl'):
        hosts = cPickle.load(open('hosts.pckl','rb'))
        
    for  url, ip_address, visit_time in curs.fetchall():
        # Skip tests by tt5.s.tingtun.no since these are Nagios checks
        if url=='http://accessibility.tingtun.no/testfiles/pdf/test.pdf':
            # print 'Skipping tingtun nagios URL ...'
            continue

        # Ignore private addresses if any
        if any(ip_address.startswith(x) for x in ('10.','172.','192.')):
            print 'Skipping',ip_address,'...'         
            continue
        
        # Use the host program to find out the information
        fields = [url, ip_address, visit_time]

        if check_hosts:
            cmd = "host -W 5 " + ip_address

            try:
                # Replace newlines if any
                hostinfo = hosts[ip_address]
                fields.append(' '.join(filter(lambda x: len(x.strip()), hostinfo.split())))
            except KeyError:
                try:
                    print 'Finding host information for',ip_address,'...'
                    pipe = os.popen(cmd)
                    hostinfo = pipe.read().strip()
                    if hostinfo.find('not found') != -1:
                        hosts[ip_address] = "Host information not found"                    
                        fields.append('Host information not found')
                    else:
                        hosts[ip_address] = hostinfo
                        fields.append(hostinfo)                 
                except Exception, e:
                    fields.append('Host information not found')
        else:
            fields.append("Host check not done")

        # Append DNS stuff URL
        fields.append("http://www.dnsstuff.com/tools#ipInformation|type=ipv4&&value=%s" % ip_address)
        text = u'@@@'.join(fields) + '\n'
        text = unicode(text).encode('ascii','xmlcharrefreplace')
        f.write(text)
        f.flush()
        
        
    # Pickle host dictionary
    cPickle.dump(hosts, open('hosts.pckl','wb'))
    # print entries
    
    # Write to pdfwamstats.csv
    # open('pdfwamstats.csv','w').writelines(entries)
    print 'Dumped stats.'
    conn.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sighandler)    
    get_remote_db()
    check_hosts = '--check-hosts' in sys.argv
    find_stats(check_hosts)
