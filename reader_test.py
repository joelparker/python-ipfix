#!/usr/bin/env python2.7

import ipfix.reader
import ipfix.ie
import pprint
import argparse
import cProfile
import sys

ap = argparse.ArgumentParser(description="Dump an IPFIX file for debug purposes")
ap.add_argument('file', metavar='file', help='ipfix file to read')
ap.add_argument('--spec', metavar='specfile', help='iespec file to read')
args = ap.parse_args()

ipfix.ie.use_iana_default()
ipfix.ie.use_5103_default()
if args.spec:
    ipfix.ie.load_specfile(args.spec)

# prof = cProfile.Profile()
# prof.enable()

r = ipfix.reader.from_stream(open(args.file, mode="rb"))

tuplespec = """sourceIPv4Address
               destinationIPv4Address
               meanTcpRttMilliseconds
               reverseMeanTcpRttMilliseconds"""

ielist = ipfix.ie.list(ipfix.ie.for_spec(x) for x in tuplespec.split())

for rec in r.tuple_iterator(ielist):
#for rec in r.namedict_iterator():
    #print("--- record %u in message %u ---" % (r.reccount, r.msgcount))
    print("%15s -> %15s (%5u ms, %5u ms)" % (str(rec[0]), str(rec[1]), rec[2], rec[3]))
    # for key in rec:
    #     print("  %30s => %s" % (key, str(rec[key])))
    if r.reccount >= 100000:
        break

sys.stderr.write("read %u templates and %u records in %u messages\n\tskipped %u sets, %u sets without template\n" %
                 (r.tmplcount, r.reccount, r.msgcount, r.setskipcount, r.notmplcount))
# prof.disable()
# prof.dump_stats("cprofile.out")