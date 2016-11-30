import requests
import sys
import csv
import json
from ASD import get_token

"""This script takes a CSV file containg properly formated imagenames and uses the ASD API
   to retrieve the associated SHA512 and MD5 Checksum Hashes.

    PsuedoCode: For Each Image Name In 'csvImagePath' Run Get_Hash and append image/md5/sha tuple in 'csvWritePath'
"""


csvImagePath = 'C:/Users/matsiege/PycharmProjects/ASD/swreleases.csv'
csvWritePath = 'C:/Users/matsiege/PycharmProjects/ASD/eoxresults.csv'

def get_eox(releasename):
    """returns image hash when providing image name"""

    token = get_token()

    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXBySWReleaseString/1"
    querystring = {"responseencoding":"JSON","input1":"" + releasename}
    headers = {
        'content-type': "application/json",
        'authorization': "" + token['token_type'] + " " + token['access_token'],
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

def writecsv(ReleaseName, EoS, EoM, LDoS, URL):
    """Appends imagename, md5, and sha checksums to CSV file defined at top."""

    with open(csvWritePath, 'ab') as csvfile:
        fieldnames = ['ReleaseName', 'EoS', 'EoM', 'LDoS', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'ReleaseName': ReleaseName, 'EoS': EoS, 'EoM': EoM, 'LDoS':LDoS, 'URL': URL })

def parsecsv():
    """Reads CSV of Image Names and Appends results of Get_hash() to CSV file csvWritePath defined at top
     using writecsv()."""

    with open(csvImagePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ReleaseName = row['releasename']
            #print("ReleaseName from CSV:  " + ReleaseName)
            EoX_results = get_eox(row['releasename'])
            #print (EoX_results)
            data = json.loads(EoX_results)
            #print data
            PID = data['EOXRecord'][0]["EOLProductID"]
            EoS = data['EOXRecord'][0]["EndOfSaleDate"]["value"]
            EoM = data['EOXRecord'][0]["EndOfSWMaintenanceReleases"]["value"]
            LDoS = data['EOXRecord'][0]["LastDateOfSupport"]["value"]
            URL = data['EOXRecord'][0]["LinkToProductBulletinURL"]
            MigrationPID = data['EOXRecord'][0]["EOXMigrationDetails"]["MigrationProductName"]
            MigrationURL = data['EOXRecord'][0]["EOXMigrationDetails"]["MigrationProductInfoURL"]
            print ReleaseName + "::"
            print "End of Sale Date: " + EoS
            print "End of SW Maintenance: " + EoM
            print "Last Date of Support: " + LDoS
            print "Product Bulletin URL: " + URL
            print "Migration PID: " + MigrationPID
            print "Migration URL: " + MigrationURL
            print "-----"

            writecsv(ReleaseName, EoS, EoM, LDoS, URL)



if __name__ == "__main__":

    #print get_hash(sys.argv[1])

    parsecsv()