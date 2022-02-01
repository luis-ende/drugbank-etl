import sys
import os
import json
import configparser


cfg_parser = configparser.ConfigParser()
cfg_parser.read('pipeline.conf')


def log_updates_info(latest_updates):
    updates_log_file = cfg_parser.get('pipeline_log_paths', 'latest_updates_file')
    updates_list = []
    if os.path.exists(updates_log_file):
        f = open(updates_log_file)
        updates_list = json.load(f)
        f.close()

    updates_list.append(latest_updates)

    with open(updates_log_file, 'w') as outfile:
        json.dump(updates_list, outfile)
