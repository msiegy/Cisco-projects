import requests
import sys
import csv
import json
from ASD import get_token

"""This script takes a CSV file containg properly formated imagenames and uses the ASD API
   to retrieve the associated SHA512 and MD5 Checksum Hashes.

    PsuedoCode: For Each Image Name In 'csvImagePath' Run Get_Hash and append image/md5/sha tuple in 'csvWritePath'
"""


csvImagePath = 'C:/Users/matsiege/PycharmProjects/ASD/images.csv'
csvWritePath = 'C:/Users/matsiege/PycharmProjects/ASD/hashvalues.csv'

def get_hash(imagename):
    """returns image hash when providing image name"""

    token = get_token()

    url = "https://api.cisco.com/software/v2.0/checksum/image_names/" + imagename
    headers = {
        'content-type': "application/json",
        'authorization': "" + token['token_type'] + " " + token['access_token'],
        'cache-control': "no-cache",
        'postman-token': "e0d434c5-0404-7538-0d96-76323965fca5"
        }

    response = requests.request("GET", url, headers=headers)

    return response.text

def writecsv(imagename, md5, sha):
    """Appends imagename, md5, and sha checksums to CSV file defined at top."""

    with open(csvWritePath, 'ab') as csvfile:
        fieldnames = ['imagename', 'md5', 'sha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'imagename': imagename, 'md5': md5, 'sha':sha })

def parsecsv():
    """Reads CSV of Image Names and Appends results of Get_hash() to CSV file csvWritePath defined at top
     using writecsv()."""

    with open(csvImagePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['image'])
            image_results = get_hash(row['image'])
            #print image_results
            data = json.loads(image_results)
            #print data
            imagename = data['checksums'][0]["image_name"]
            sha = data['checksums'][0]["sha512_checksum"]
            md5 = data['checksums'][0]["md5_checksum"]
            print imagename + "::"
            print "SHA512 Checksum: " + sha
            print "MD5 Checksum: " + md5
            print "-----"

            writecsv(imagename, md5, sha)



if __name__ == "__main__":

    #print get_hash(sys.argv[1])

    parsecsv()
    #writecsv('IOS15-advipservices', 'md5392527adgahjsdgsaoia', 'sha232922626')