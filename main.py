from extract_drugbank import fetch_drugbank_latest_downloads, download_latest_updates
from load_drugbank import load_latest_updates, load_postgresql_database
from log_pipeline_info import log_updates_info, update_config_info
from datetime import datetime


def build_etl_drugbank():
    print('Fetching latest downloads info ..........................')
    latest_updates = fetch_drugbank_latest_downloads()
    if len(latest_updates) > 0:
        print('Downloading zip files ..........................')
        download_latest_updates(latest_updates)
        print('Loading updated directories and databases ................')
        load_latest_updates(latest_updates)
        print('Logging updates info .....................................')
        log_updates_info(latest_updates)
        update_config_info(latest_updates)
    else:
        print('[%s] No new updates to apply.' % datetime.now().strftime('%m-%d-%Y %H:%M:%S'))


if __name__ == '__main__':
    build_etl_drugbank()
