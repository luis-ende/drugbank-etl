import sys
import os
import json
import configparser


cfg_parser = configparser.ConfigParser()
cfg_parser.read('pipeline.conf')


def log_updates_info(latest_updates):
    """
    Log applied updates (see pipeline.conf)
    """
    updates_log_file = cfg_parser.get('pipeline_log_paths', 'latest_updates_file')
    updates_list = []
    if os.path.exists(updates_log_file):
        f = open(updates_log_file)
        updates_list = json.load(f)
        f.close()

    updates_list = updates_list + latest_updates
    with open(updates_log_file, 'w') as outfile:
        json.dump(updates_list, outfile)


def update_config_info(latest_updates):
    """
    Update config with the latest applied updates (see pipeline.conf)
    """
    for update_info in latest_updates:
        cfg_parser.set('drugbank_last_update', '%s_last_update' % update_info['download_info']['format'].lower(),
                       update_info['download_info']['created_at'])
        with open('pipeline.conf', 'w') as configfile:
            cfg_parser.write(configfile)
