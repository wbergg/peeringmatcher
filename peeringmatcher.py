#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
import requests
import sys
from prettytable import PrettyTable
#import paramiko
import time

def main():
    if len(sys.argv) < 3:
        print "Not enough arguments."
        print
        print "Example:"
        print "./peeringmatcher.py <asn1> <asn2>"
        print
    elif len(sys.argv) == 3:
        # Print AS-numbers to names
        print
        print "Mututal peering locations for AS%s (%s) and AS%s (%s)" % (sys.argv[1], (get_as_name(sys.argv[1])), sys.argv[2], (get_as_name(sys.argv[2])))
        print
        
        api_data_asn1 = requests.get('https://www.peeringdb.com/api/netixlan?asn=' + sys.argv[1])
        api_data_asn2 = requests.get('https://www.peeringdb.com/api/netixlan?asn=' + sys.argv[2])
        json_data_asn1 = api_data_asn1.json()
        json_data_asn2 = api_data_asn2.json()
        asn1 = dict()
        asn2 = dict()

        for x in json_data_asn1['data']:
            if x['ixlan_id'] not in asn1:
                asn1[x['ixlan_id']] = list()
            data = { 'ipv4': x['ipaddr4'], 'ipv6': x['ipaddr6'], 'ix_id': x['ix_id'] }
            asn1[x['ixlan_id']].append(data)
        
        for x in json_data_asn2['data']:
            if x['ixlan_id'] not in asn2:
                asn2[x['ixlan_id']] = list()
            data = { 'ipv4': x['ipaddr4'], 'ipv6': x['ipaddr6'], 'ix_id': x['ix_id'] }
            asn2[x['ixlan_id']].append(data)
        
        # Create a pretty table
        x = PrettyTable(["IXLAN", "ASN", "IPv4", "IPv6"])
        x.padding_width = 1

        # Populate the table
        for key in set(asn1.keys()) & set(asn2.keys()):
            # Map IX number to human readable
            for y in asn1[key]:
                ix = map_id_to_ix(str(y['ix_id']), str(key))
                x.add_row([ix, sys.argv[1], y['ipv4'], y['ipv6']])
            for y in asn2[key]:
                ix = map_id_to_ix(str(y['ix_id']), str(key))
                x.add_row([ix, sys.argv[2], y['ipv4'], y['ipv6']])
            # How the f do I make an empty row!? Ugly below...
            x.add_row(["", "", "", ""])
        # Print pretty table
        print x

def map_id_to_ix(ixlan_id1, ixlan_id2):
    # Get the IX name
    api_data1 = requests.get('https://www.peeringdb.com/api/ix?id=' + ixlan_id1)
    # Get the IXLAN name
    api_data2 = requests.get('https://www.peeringdb.com/api/ixlan?id=' + ixlan_id2)
    json_data1 = api_data1.json()
    json_data2 = api_data2.json()
    for x in json_data1['data']:
        output1 = x['name']
    for x in json_data2['data']:
        output2 = x['name']
    return(output1 + ' ' + output2)

def get_as_name(asn):
    api_data = requests.get('https://www.peeringdb.com/api/net?asn=' + asn)
    json_data = api_data.json()
    for x in json_data['data']:
        return x['name']

if __name__ == '__main__':
    main()
