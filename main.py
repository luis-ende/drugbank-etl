from extract_drugbank import fetch_drugbank_latest_downloads, download_latest_updates
from load_drugbank import load_latest_updates
from log_pipeline_info import log_updates_info

SUPERNUS_DRUGBANK_PATHS = {
    'JSON': '/home/jsalazar/Projects/sil_drugbank/drugbank_json',
    'CSV': '/home/jsalazar/Projects/sil_drugbank/drugbank_csv'
}


def build_drugbank():
    latest_updates = fetch_drugbank_latest_downloads()
    download_latest_updates(latest_updates)
    log_updates_info(latest_updates)
    load_latest_updates(latest_updates)


if __name__ == '__main__':
    build_drugbank()
