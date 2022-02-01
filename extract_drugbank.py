#! /usr/bin/env python3

import sys
import os
import json
import zipfile

import pycurl as pycurl_lib
import configparser
from datetime import datetime
from io import BytesIO

DRUGBANK_DOWNLOADS_URL = 'https://portal.drugbank.com/downloads.json'
cfg_parser = configparser.ConfigParser()
cfg_parser.read('pipeline.conf')


def fetch_drugbank_latest_downloads():
    data = BytesIO()

    pycurl = pycurl_lib.Curl()
    pycurl.setopt(pycurl.URL, DRUGBANK_DOWNLOADS_URL)
    pycurl.setopt(pycurl.HTTPHEADER, ["Accept: application/json"])
    pycurl.setopt(pycurl.USERPWD, '%s:%s' % (cfg_parser.get('drugbank_credentials', 'user'),
                                             cfg_parser.get('drugbank_credentials', 'password')))
    pycurl.setopt(pycurl.WRITEFUNCTION, data.write)
    pycurl.perform()
    pycurl.close()

    downloads_data = json.loads(data.getvalue())

    date_format = '%Y-%m-%dT%H:%M:%S.000Z'
    json_last_update = datetime.strptime(cfg_parser.get('drugbank_last_update', 'json_last_update'), date_format)
    csv_last_update = datetime.strptime(cfg_parser.get('drugbank_last_update', 'csv_last_update'), date_format)

    latest_updates = {}
    for download in downloads_data:
        download_date = datetime.strptime(download['created_at'], date_format)
        if (download['format'] == 'JSON') and ('json' not in latest_updates):
            if download_date > json_last_update:
                latest_updates['json'] = download
        elif (download['format'] == 'CSV') and ('csv' not in latest_updates):
            if download_date > csv_last_update:
                latest_updates['csv'] = download

    return latest_updates


def download_latest_updates(latest_updates):
    for update_info in latest_updates:
        update_format = None
        if latest_updates['json']:
            update_format = 'JSON'
        elif latest_updates['csv']:
            update_format = 'CSV'

        if update_format:
            if not os.path.exists('downloads'):
                os.mkdir('downloads')
            file_name = './downloads/drugbank_%s_%s.zip'
            file_name = file_name % (update_format, datetime.now().strftime("%m%d%Y_%H%M%S"))
            with open(file_name, 'wb') as f:
                print("Downloading file " + file_name + ' .....')
                pycurl = pycurl_lib.Curl()
                pycurl.setopt(pycurl.URL, latest_updates[update_info]['url'])
                pycurl.setopt(pycurl.USERPWD, '%s:%s' % (cfg_parser.get('drugbank_credentials', 'user'),
                                                         cfg_parser.get('drugbank_credentials', 'password')))
                pycurl.setopt(pycurl.FOLLOWLOCATION, True)
                pycurl.setopt(pycurl.WRITEDATA, f)
                pycurl.perform()
                pycurl.close()
                print("File downloaded.")
            if update_info['content_type'] == 'application/zip':
                unzip_downloaded_file(file_name, update_format)


def unzip_downloaded_file(zip_update_file, update_format):
    drugbank_path = cfg_parser.get('supernus_drugbank_paths', update_format)
    if os.path.exists(zip_update_file) and \
            os.path.exists(drugbank_path) and \
            zipfile.is_zipfile(zip_update_file):
        with zipfile.ZipFile(zip_update_file, 'r') as zip_ref:
            print('Extracting file ' + zip_update_file + ' to ' + drugbank_path)
            zip_ref.extractall(drugbank_path)
            print('Zip file extracted.')
    else:
        print("Path doesn't exist or not valid zip file '" + zip_update_file + "'")
