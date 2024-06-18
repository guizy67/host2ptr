# `host2ptr.py` Hosts File Parser

This script parses a Unix-style `/etc/hosts` file to extract valid IP addresses and relevant information to create DNS reverse lookup entries. The script is designed to work specifically with IPv4 addresses and generates PTR records that contain fully qualified domain names (FQDNs).

## Features

- Parses `/etc/hosts` file to extract IP addresses and hostnames.
- Generates PTR records for DNS reverse lookup.
- Supports adding a default domain to short hostnames.
- Retains comments from the `/etc/hosts` file.
- Outputs the processed data in JSON format.
- Allows filtering and displaying records by `netname`.

## Requirements

- Python 3.6+
- `re` module (regular expressions, included in the standard library)
- `json` module (JSON handling, included in the standard library)
- `ipaddress` module (IP address validation, included in the standard library)
- `collections` module (defaultdict for grouping records, included in the standard library)

## Usage

1. Ensure you have a `/etc/hosts` style file named `raw-hosts-files.txt` in the same directory as the script.
2. Run the script:
    ```bash
    ./host2ptr.py
    ```
3. The script will generate a JSON file named `hostfile-converted-ptr-data.json` containing the processed data.

### Example Output Format

The JSON output format for a single entry looks like this:

```json
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
]
```


## `gen-zone.py` Utility

# Zone File Generator

This script reads a JSON file containing PTR record data and generates DNS zone files for reverse DNS lookup.

## Requirements

- Python 3.6+
- `json` module (included in the standard library)

## Usage

1. Ensure you have the JSON file `hostfile-converted-ptr-data.json` in the same directory as the script.
2. Run the script:
    ```bash
    ./gen-zone.py
    ```
3. The script will generate zone files named `<zonename>.db` for each unique `zonename` found in the JSON file.

### Example Input JSON

The input JSON file should be in the following format:

```json
[
  [
    "192.168.36.98",
    {
      "ipaddr": "192.168.36.98",
      "netname": "192.168.36",
      "zonename": "36.168.192.in-addr.arpa",
      "lastoctet": "98",
      "names": [
        "example001",
        "example001.example.com"
      ],
      "hosts": [
        "example001.example.com",
        "example001.example.com"
      ],
      "fqdn": "example001.example.com",
      "comment": "# Comment from hosts file",
      "ptr_record": "98  IN PTR  example001.example.com.    ;Comment from hosts file"
    }
  ],
  [
    "192.168.5.7",
    {
      "ipaddr": "192.168.5.7",
      "netname": "192.168.5",
      "zonename": "5.168.192.in-addr.arpa",
      "lastoctet": "7",
      "names": [
        "example002",
        "example002.example.com"
      ],
      "hosts": [
        "example002.example.com",
        "example002.example.com"
      ],
      "fqdn": "example002.example.com",
      "comment": "# Another comment",
      "ptr_record": "7  IN PTR  example002.example.com.    ;Another comment"
    }
  ]
]
```

