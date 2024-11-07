This project holds files for using the Cisco ASD API.

eoxHWbyPID.py takes a CSV file containing properly formatted Cisco Product IDs and outputs and stores End of Life milestone dates in eoxHWpidresults.csv

hasval.py is a script that takes a CSV file containg properly formated
imagenames and uses the ASD API to retrieve the associated SHA512 and
MD5 Checksum Hashes.

eox.py takes a CSV file containing properly formatted SW relasenames and
retrieves the associated EoX information.

This Project leverages the ASD.py class for obtaining an OAUTH2
authentication tokens.

The Cisco ASD API requires registration for usage and is available to
cisco employees and SNTC customers.
https://developer.cisco.com/docs/support-apis/#!eox/get-eox-by-product-ids
