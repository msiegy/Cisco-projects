"""This script takes a CSV file containing properly formated HW Serial (eg: FHK0933224R) from
[csvInputPath] and uses the EOX V5 API within Cisco API Console to retrieve  and the write the associated EoX
information to a CSV.



    PsuedoCode: For Each Serial In 'csvInputPath' Run get_eoxbySerial and append EoS, LDoS, etc tuples in 'csvWritePath'
"""

import requests
import sys
import os.path
import csv
import json
from ASD import get_token

csvInputPath = 'C:/Users/matsiege/PycharmProjects/Templates/CiscoAPIconsole/hwinventory-serial.csv'
csvWritePath = 'C:/Users/matsiege/PycharmProjects/Templates/CiscoAPIconsole/eoxHWresults.csv'

def get_eoxbySerial(hwPID):
    """returns HW EoX info when providing HW Serial
    The resulting data structure is a Dictionary, that contains elements of Dictionaries and Lists. e.g: EOXRecord is a
    list and the first element happens to be an unnamed dictionary, so it is identified with [0]. Within this unnamed
    dictionary there are Key/Value pairs representing PIDs and EoX dates.
    """

    token = get_token()

    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/" + hwPID
    headers = {
        'content-type': "application/json",
        'authorization': "" + token['token_type'] + " " + token['access_token'],
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)

    return response.text

def writecsv(PID, EoS, EoM, LDoS, URL, MigrationPID, MigrationURL, MigrationStrat, ErrorDescription):
    """Appends HWPID, EoS, EoM, LDoS and URL Bulletins to CSV file defined at top."""

    """Set File existence flag, If results file does not yet exist we will write Field Headers to the CSV"""
    file_exists = os.path.isfile(csvWritePath)

    with open(csvWritePath, 'ab') as csvfile:
        fieldnames = ['PID', 'EoS', 'EoM', 'LDoS', 'EoX URL', 'MigrationPID', 'MigrationURL', 'MigrationStrat', 'Error Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({'PID': PID, 'EoS': EoS, 'EoM': EoM, 'LDoS': LDoS, 'EoX URL': URL, 'MigrationPID': MigrationPID, 'MigrationURL': MigrationURL, 'MigrationStrat': MigrationStrat, 'Error Description': ErrorDescription})

def parsecsv():
    """Reads CSV of Serials and Appends results of get_eoxbySerial() to CSV file csvWritePath defined at top
     using writecsv()."""

    with open(csvInputPath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hwSerial = row['Serial']
            #print("HW Serial from CSV:  " + hwSerial)
            EoX_results = get_eoxbySerial(row['Serial'])
            #print (EoX_results)
            data = json.loads(EoX_results)
            #print data
            PID = data['EOXRecord'][0]["EOLProductID"]
            EoS = data['EOXRecord'][0]["EndOfSaleDate"]["value"]
            EoM = data['EOXRecord'][0]["EndOfSWMaintenanceReleases"]["value"]
            LDoS = data['EOXRecord'][0]["LastDateOfSupport"]["value"]
            URL = data['EOXRecord'][0]["LinkToProductBulletinURL"]
            MigrationPID = data['EOXRecord'][0]["EOXMigrationDetails"]["MigrationProductId"]
            MigrationURL = data['EOXRecord'][0]["EOXMigrationDetails"]["MigrationProductInfoURL"]
            MigrationStrat = data['EOXRecord'][0]["EOXMigrationDetails"]["MigrationStrategy"]
            ErrorDescription = ""
            if 'EOXError' in data['EOXRecord'][0]:
                ErrorDescription = data['EOXRecord'][0]['EOXError']['ErrorDescription']
                #print type(data['EOXRecord'][0])
            else:
                ErrorDescription = "No Error(s) found"

            """
            print PID + "::"
            print "End of Sale Date: " + EoS
            print "End of SW Maintenance: " + EoM
            print "Last Date of Support: " + LDoS
            print "Product Bulletin URL: " + URL
            print "Migration PID: " + MigrationPID
            print "Migration URL: " + MigrationURL
            print "Migration Strategy: " + MigrationStrat
            print "Error Field: " + ErrorDescription
            print "-----"
            """
            #print hwSerial
            #print ErrorDescription

            writecsv(PID, EoS, EoM, LDoS, URL, MigrationPID, MigrationURL, MigrationStrat, ErrorDescription)



if __name__ == "__main__":

    #print get_eoxbySerial(sys.argv[1])
    parsecsv()