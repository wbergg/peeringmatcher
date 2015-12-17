#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
import requests
import sys
from prettytable import PrettyTable
import paramiko
import time

def main():
    if len(sys.argv) < 3:
        print "Not enough arguments."
        print
        print "Example:"
        print "./peeringmatcher.py <asn1> <asn2>"
        print
    elif len(sys.argv) == 3:
        api_data_asn1 = requests.get('https://beta.peeringdb.com/api/asn/' + sys.argv[1])
        api_data_asn2 = requests.get('https://beta.peeringdb.com/api/asn/' + sys.argv[2])
        json_data_asn1 = api_data_asn1.json()
        json_data_asn2 = api_data_asn2.json()

        asn1 = dict()
        asn2 = dict()
        for x in json_data_asn1['data']:
            for y in x['netixlan_set']:
                data = { 'ipv4': y['ipaddr4'], 'ipv6': y['ipaddr6']}
                asn1[y['ixlan_id']] = data
        
        for x in json_data_asn2['data']:
            for y in x['netixlan_set']:
                data = { 'ipv4': y['ipaddr4'], 'ipv6': y['ipaddr6']}
                asn2[y['ixlan_id']] = data

        # Create a pretty table
        x = PrettyTable(["IXLAN", "ASN", "IPv4", "IPv6"])
        x.padding_width = 1

        # Populate the table
        for key in set(asn1.keys()) & set(asn2.keys()):
            # Map IX number to human readable
            ix = map_id_to_ix(str(key))
            x.add_row([ix, sys.argv[1], asn1[key]['ipv4'], asn1[key]['ipv6']])
            x.add_row([ix, sys.argv[2], asn2[key]['ipv4'], asn2[key]['ipv6']])
            # How the fuck do I make an empty row!? Ugly below...
            x.add_row(["", "", "", ""])
        # Print pretty table
        print x

def map_id_to_ix(ixlan_id):
    api_data = requests.get('https://beta.peeringdb.com/api/ixlan/' + ixlan_id)
    json_data = api_data.json()
    for x in json_data['data']:
        return x['ix']['name']

if __name__ == '__main__':
    main()
