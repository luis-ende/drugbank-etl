import sys
import subprocess
import json
import configparser
from datetime import datetime
from git import Repo, InvalidGitRepositoryError

cfg_parser = configparser.ConfigParser()
cfg_parser.read('pipeline.conf')


def load_latest_updates(latest_updates):
    for update_info in latest_updates:
        drugbank_repo_path = cfg_parser.get('etl_drugbank_paths', update_info['download_info']['format'])
        try:
            drugbank_git_repo = Repo(drugbank_repo_path)
            print("Git repo found in '" + drugbank_repo_path + "'")
        except InvalidGitRepositoryError:
            print("Creating new git repo in '" + drugbank_repo_path + "'")
            drugbank_git_repo = Repo.init(drugbank_repo_path, bare=False)

        print("Adding changes via Git...")
        drugbank_git_repo.git.add(all=True)
        drugbank_git_repo.index.commit("DrugBank Version: " + update_info['download_info']['created_at'] +
                                       "|Download Id: " + str(update_info['download_info']['id']))
        drugbank_git_repo.create_tag(update_info['download_info']['id'])
        print("Changes added.")
        if update_info['download_info']['format'] == 'CSV':
            load_postgresql_database(drugbank_repo_path)


def load_postgresql_database(drugbank_csv_path):
    # Execute shell script to run a new docker container and load new version of the drugbank postgresql db
    print("Executing Docker container script.....")
    exit_code = subprocess.check_call("./docker/create_drugbank_db_container.sh %s %s" %
                                      (drugbank_csv_path,
                                       cfg_parser.get('etl_drugbank_postgresql', 'db_password')),
                                      shell=True)
    print("Script executed. Exit code: " + str(exit_code))

