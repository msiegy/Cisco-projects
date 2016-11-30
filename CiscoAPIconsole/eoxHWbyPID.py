import requests
import sys
import csv
import json
from ASD import get_token

"""This script takes a CSV file containing properly formated HW PIDs (eg: N7K-M148GS-11L) from
[csvInputPath] and uses the EOX V5 API within Cisco API Console to retrieve  and the write the associated EoX
information to a CSV.

    PsuedoCode: For Each SW Release In 'csvInputPath' Run get_eoxbyPID and append EoS, LDoS, etc tuples in 'csvWritePath'
"""


csvInputPath = 'C:/Users/matsiege/PycharmProjects/Templates/CiscoAPIconsole/hwinventory.csv'
csvWritePath = 'C:/Users/matsiege/PycharmProjects/Templates/CiscoAPIconsole/eoxHWresults.csv'

def get_eoxbyPID(hwPID):
    """returns HW EoX info when providing HWPID"""

    token = get_token()

    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/" + hwPID
    headers = {
        'content-type': "application/json",
        'authorization': "" + token['token_type'] + " " + token['access_token'],
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)

    return response.text

def writecsv(PID, EoS, EoM, LDoS, URL, MigrationPID, MigrationURL, MigrationStrat):
    """Appends ReleaseName, EoS, EoM, LDoS and URL Bulletins to CSV file defined at top."""

    with open(csvWritePath, 'ab') as csvfile:
        fieldnames = ['PID', 'EoS', 'EoM', 'LDoS', 'URL', 'MigrationPID', 'MigrationURL', 'MigrationStrat']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'PID': PID, 'EoS': EoS, 'EoM': EoM, 'LDoS': LDoS, 'URL': URL, 'MigrationPID': MigrationPID, 'MigrationURL': MigrationURL, 'MigrationStrat': MigrationStrat})

def parsecsv():
    """Reads CSV of ReleaseNames and Appends results of get_eoxbyPID() to CSV file csvWritePath defined at top
     using writecsv()."""

    with open(csvInputPath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hWPID = row['PID']
            #print("HW PID from CSV:  " + hwPID)
            EoX_results = get_eoxbyPID(row['PID'])
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
            print PID + "::"
            print "End of Sale Date: " + EoS
            print "End of SW Maintenance: " + EoM
            print "Last Date of Support: " + LDoS
            print "Product Bulletin URL: " + URL
            print "Migration PID: " + MigrationPID
            print "Migration URL: " + MigrationURL
            print "Migration Strategy: " + MigrationStrat
            print "-----"

            writecsv(PID, EoS, EoM, LDoS, URL, MigrationPID, MigrationURL, MigrationStrat)



if __name__ == "__main__":

    #print get_eoxbyPID(sys.argv[1])

    parsecsv()