#!/usr/local/bin/python3

"""
This program tries to parse unix style /etc/hosts file to extract
the valid IP addresses, and relevant information to create the
DNS reverse lookup entry.

Comment lines are disgarded, but comments following and IP / hostname
line are kept as the comment for that entry.

A default subdomain is used to fill in when none is present in the hostname for
a particular IP address. The generated PTR record always contains a FQDN.

This script currently only checks for valid IPv4 addresses and should only be
used for IPv4 /etc/hosts files.

(#TODO: add IPv6 support)

The output is a JSON file that can easily be parsed to generate a zonefile.
Example output format of 1 entry:
      [
    "192.168.36.98",
    {
      "ipaddr": "192.168.36.98",
      "netname": "192.168.36",
      "zonename": "36.168.192.in-addr.arpa",
      "lastoctet": "98",
      "names": [
        "xxxxxxxxxxxxx001",
        "xxxxxxxxxxxxx001.example.com"
      ],
      "hosts": [
        "xxxxxxxxxxxxx001.example.com",
        "xxxxxxxxxxxxx001.example.com"
      ],
      "fqdn": "xxxxxxxxxxxxx001.example.com",
      "comment": "# Comment from hosts file",
      "ptr_record": "98  IN PTR  xxxxxxxxxxxxx001.example.com.    ;Comment from hosts file"
    }
  ],
"""

import re
import json
import ipaddress
from collections import defaultdict
import sys

# Check if the input file is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input_file>")
    sys.exit(1)

filename = sys.argv[1]

## CHANGE THIS IF NEEDED
# Default domain to append to short names
default_domain = 'ip.nl.tmo'
##

# Function to check if we have a valid IP
def is_valid_ip(ip_str):
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except ValueError:
        return False

# Function to output records by netname
def output_records_by_netname(netname):
    records = grouped_records.get(netname, [])
    if records:
        print(f"Records with netname '{netname}':")
        for record in records:
            print(json.dumps(record, indent=2))
    else:
        print(f"No records found with netname '{netname}'.")

# Read and clean up the input lines
with open(filename) as file:
    lines = [line.strip() for line in file]

# Regex to reduce multiple whitespaces to a single space
whitespace_re = re.compile(r'\s+')

# Data structure to hold cleaned data
data = {}

# Process each line
for line in lines:
    # Skip lines starting with #
    if line.startswith('#'):
        continue

    # Replace multiple whitespaces with a single space
    items = whitespace_re.sub(' ', line)

    # Split the line by # to separate comments
    parts1 = items.split('#')
    comment = parts1[1] if len(parts1) > 1 else ' - no comment - '

    # Split the part before the comment by whitespace
    parts = parts1[0].split()

    # Only process lines where the first item is a valid IP
    if parts and is_valid_ip(parts[0]):
        ipaddr = parts[0]
        names = parts[1:]

        # Generate fully qualified domain names (FQDNs)
        hosts = [n if len(n.split('.')) > 2 else f"{n}.{default_domain}" for n in names]

        # Prepare data for PTR records
        ip_parts = ipaddr.split('.')
        last_octet = ip_parts[-1]
        octets = ip_parts[:3]
        netname = '.'.join(octets)
        reversed_octets = octets[::-1]
        zonename = '.'.join(reversed_octets) + '.in-addr.arpa'
        fqdn = hosts[0]  # Assuming the first host as the primary FQDN
        ptr_record = f"{last_octet}  IN PTR  {fqdn}.    ;{comment}"

        rev_octs = '.'.join(ip_parts[::-1])
        full_rec = f"{rev_octs}.in-addr.arpa. IN PTR  {fqdn}.   ; {comment}"

        # Create a record dictionary
        record = {
            'ipaddr': ipaddr,
            'netname': netname,
            'zonename': zonename,
            'lastoctet': last_octet,
            'names': names,
            'hosts': hosts,
            'fqdn': fqdn,
            'comment': '# ' + comment,
            'ptr_record': ptr_record,
            'full_record': full_rec
        }

        # Add the record to data dictionary if IP is not already present
        if ipaddr not in data:
            data[ipaddr] = record

# Sort the data by IP address
sorted_data = sorted(data.items())

# Save cleaned data to a JSON file
with open('hostfile-converted-ptr-data.json', 'w') as f:
    json.dump(sorted_data, f, indent=2)


# Group records by netname
grouped_records = defaultdict(list)
for ip, record in sorted_data:
    grouped_records[record['netname']].append(record)

# Example usage: output records with a specific netname
output_records_by_netname("192.168.100")
