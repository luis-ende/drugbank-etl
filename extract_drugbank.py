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
    """
    Fetch the most recent available downloads by format after the last update (see pipeline.conf)
    """
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

    added_formats = []
    latest_updates = []
    for download in downloads_data:
        download_date = datetime.strptime(download['created_at'], date_format)
        add_download_entry = False
        if (download['format'] == 'JSON') and ('JSON' not in added_formats):
            add_download_entry = download_date > json_last_update
        elif (download['format'] == 'CSV') and ('CSV' not in added_formats):
            add_download_entry = download_date > csv_last_update

        if add_download_entry:
            update_to_apply = {'type': download['format'],
                               'fetch_date': datetime.now().strftime(date_format),
                               'download_info': download}
            latest_updates.append(update_to_apply)
            added_formats.append(download['format'])

    return latest_updates


def download_latest_updates(latest_updates):
    """
    Download latest available zip downloads of the DrugBank for supported formats.
    """
    # TODO Use download id instead of datestamp as file name
    # TODO Validate if the zip file already exists in the downloads directory,
    #  if it does, don't download the zip file again
    # TODO Remove older zip files, leave latest 3 (configurable)
    for update_info in latest_updates:
        update_format = None
        if update_info['download_info']['format'] in ('JSON', 'CSV'):
            update_format = update_info['download_info']['format']

        if update_format:
            if not os.path.exists('downloads'):
                os.mkdir('downloads')
            file_name = './downloads/drugbank_%s_%s.zip'
            file_name = file_name % (update_format, datetime.now().strftime("%m%d%Y_%H%M%S"))
            with open(file_name, 'wb') as f:
                print("Downloading file " + file_name + ' .....')
                pycurl = pycurl_lib.Curl()
                pycurl.setopt(pycurl.URL, update_info['download_info']['url'])
                pycurl.setopt(pycurl.USERPWD, '%s:%s' % (cfg_parser.get('drugbank_credentials', 'user'),
                                                         cfg_parser.get('drugbank_credentials', 'password')))
                pycurl.setopt(pycurl.FOLLOWLOCATION, True)
                pycurl.setopt(pycurl.WRITEDATA, f)
                pycurl.perform()
                pycurl.close()
                print("File downloaded.")
            if update_info['download_info']['content_type'] == 'application/zip':
                unzip_downloaded_file(file_name, update_format)


def unzip_downloaded_file(zip_update_file, update_format):
    drugbank_path = cfg_parser.get('supernus_drugbank_paths', update_format)
    if not os.path.exists(drugbank_path):
        sys.exit("DrugBank directory doesn't exist: " + drugbank_path +
                 ". See [supernus_drugbank_paths] section in config file.")

    if os.path.exists(zip_update_file) and zipfile.is_zipfile(zip_update_file):
        with zipfile.ZipFile(zip_update_file, 'r') as zip_ref:
            print('Extracting file ' + zip_update_file + ' to ' + drugbank_path)
            zip_ref.extractall(drugbank_path)
            print('Zip file extracted.')
    else:
        print("Path doesn't exist or not valid zip file '" + zip_update_file + "'")
        sys.exit("[Error] DrugBank extraction couldn't be completed successfully.")
