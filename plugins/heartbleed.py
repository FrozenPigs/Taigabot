#!/usr/bin/env python

# Based on the original code by Jared Stafford.

# NOTE: this code has been modified to test for OpenSSL versions vulnerable to 
# Heartbleed without exploiting the server, therefore the heartbeat request
# does _not_ cause the server to leak any data from memory or expose any data
# in an unauthorized manner.
# Based on: https://github.com/dchan/metasploit-framework/blob/master/modules/auxiliary/scanner/ssl/openssl_heartbleed.rb
# See: https://blog.mozilla.org/security/2014/04/12/testing-for-heartbleed-vulnerability-without-exploiting-the-server/

# Usage example: python ssltest.py example.com
from util import hook
import sys
import struct
import socket
import time
import select
import re
import netaddr
import json
import os
import datetime
import signal
from optparse import OptionParser
from collections import defaultdict

host_status = {}
hosts_to_skip = []
counter = defaultdict(int)


options = OptionParser(usage='%prog <network> [network2] [network3] ...', description='Test for SSL heartbleed vulnerability (CVE-2014-0160) on multiple domains')
options.add_option('--input', '-i', dest="input_file", default=[], action="append", help="Optional input file of networks or ip addresses, one address per line")
options.add_option('--logfile', '-o', dest="log_file", default="results.txt", help="Optional logfile destination")
options.add_option('--resume', dest="resume", action="store_true", default=False, help="Do not rescan hosts that are already in the logfile")
options.add_option('--timeout', '-t', dest="timeout", default=5, help="How long to wait for remote host to respond before timing out")
options.add_option('--json', dest="json_file", default=None, help="Save data as json into this file")
options.add_option('--only-vulnerable', dest="only_vulnerable", action="store_true", default=False, help="Only scan hosts that have been scanned before and were vulnerable")
options.add_option('--only-unscanned', dest="only_unscanned", action="store_true", default=False, help="Only scan hosts that appear in the json file but have not been scanned")
options.add_option('--summary', dest="summary", action="store_true", default=False, help="Useful with --json. Don't scan, just print old results")
options.add_option('--verbose', dest="verbose", action="store_true", default=False, help="Print verbose information to screen")
options.add_option('--max', dest="max", default=None, help="Exit program after scanning X hosts. Useful with --only-unscanned")
opts, args = options.parse_args()

def h2bin(x):
    return x.replace(' ', '').replace('\n', '').decode('hex')

hello = h2bin('''
16 03 02 00  dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01                                  
''')

hb = "\x18\x03\x02N#\x01N " + "\x01"*20000


def recvall(s, length, timeout=5):
    endtime = time.time() + timeout
    rdata = ''
    remain = length
    while remain > 0:
        rtime = endtime - time.time()
        if rtime < 0:
            return None
        r, w, e = select.select([s], [], [], 5)
        if s in r:
            try:
                data = s.recv(remain)
            except Exception, e:
                return None
            # EOF?
            if not data:
                return None
            rdata += data
            remain -= len(data)
    return rdata


def recvmsg(s):
    hdr = recvall(s, 5)
    if hdr is None:
        return None, None, None
    typ, ver, ln = struct.unpack('>BHH', hdr)
    pay = recvall(s, ln, 10)
    if pay is None:
        return None, None, None
    return typ, ver, pay


def hit_hb(s):
    try:
        s.send(hb)
    except Exception, e:
        return False
    while True:
        typ, ver, pay = recvmsg(s)
        if typ is None:
            return False

        if typ == 24:
            return True

        if typ == 21:
            return False


def is_vulnerable(host, timeout):
    """ Check if remote host is vulnerable to heartbleed

     Returns:
        None  -- If remote host has no ssl
        False -- Remote host has ssl but likely not vulnerable
        True  -- Remote host might be vulnerable
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(int(timeout))
    try:
        s.connect((host, 443))
    except Exception, e:
        return None
    s.send(hello)
    while True:
        typ, ver, pay = recvmsg(s)
        if typ is None:
            return None
        # Look for server hello done message.
        if typ == 22 and ord(pay[0]) == 0x0E:
            break

    s.send(hb)
    return hit_hb(s)

def store_results(host_name, current_status):
    current_time = time.time()

    counter[current_status] += 1
    counter["Total"] += 1
    if host_name not in host_status:
        host_status[host_name] = {}
    host = host_status[host_name]
    # Make a note when this host was last scanned
    host['last_scan'] = current_time

    # Make a note if this host has never been scanned before
    if 'first_scan' not in host:
        host['first_scan'] = current_time
    elif host.get('status', 'never been scanned') != current_status:
        # If it has a different check result from before
        host['changelog'] = host.get('changelog', [])
        changelog_entry = [current_time, current_status]
        host['changelog'].append(changelog_entry)
    host['status'] = current_status
    #with open(opts.log_file, 'a') as f:
    message = "{current_time} {host} {current_status}".format(**locals())
        # f.write(message + "\n")
    return message

def scan_host(host):
    """ Scans a single host, logs into

    Returns:
        list(timestamp, ipaddress, vulnerabilitystatus)
    """
    host = str(host)
    result = is_vulnerable(host, opts.timeout)
    message = store_results(host, result)
    if opts.verbose: print message
    return message


def print_summary():
    """ Print summary of previously stored json data to screen """

    counter = defaultdict(int)
    for host, data in host_status.items():
        friendly_status = "unknown"
        status = data.get('status', "Not scanned")
        if status is None:
            friendly_status = "SSL Connection Refused"
        elif status is True:
            friendly_status = "Vulnerable"
        elif status is False:
            friendly_status = "Not Vulnerable"
        else:
            friendly_status = str(status)

        if opts.only_vulnerable and not status:
            continue
        elif opts.only_unscanned and 'status' in data:
            continue
        return "[{}] {}".format(host, friendly_status)
    return



@hook.command(autohelp=False) #, adminonly=True
def heartbleed(inp, reply=None):
    "bash <id> -- Gets a random quote from Bash.org, or returns a specific id."
    global host_status
    host_status = {}
        
    scan_host(inp)

    return print_summary()


