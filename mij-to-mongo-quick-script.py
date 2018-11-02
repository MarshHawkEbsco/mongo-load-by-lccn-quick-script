import csv
import io
import json
import sys

import requests
from pymarc import XmlHandler, parse_xml
from pymongo import MongoClient

mongo_connection_string = sys.argv[1]
path_to_csv_of_lccns = sys.argv[2]

c = MongoClient(mongo_connection_string)
db = c['catrecords']
mij = db.mij

handler = XmlHandler()

lccns = []
with open(path_to_csv_of_lccns) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for r in spamreader:
        for l in r:
            lccns.append(l)

for lccn in lccns:
    r = requests.get("http://lccn.loc.gov/{0}/marcxml".format(lccn))
    f = io.StringIO(r.text)
    parse_xml(f, handler)

for rec in handler.records:
    mij.insert_one(json.loads(rec.as_json()))
    

