import sys
import json
import pycurl as pycurl_lib
import configparser
from datetime import datetime
import git
from git import Repo

cfg_parser = configparser.ConfigParser()
cfg_parser.read('pipeline.conf')


def load_latest_updates(latest_updates):
    for latest_update in latest_updates:
        drugbank_repo_path = cfg_parser.get('supernus_drugbank_paths', latest_update['format'])
        drugbank_git_repo = Repo(drugbank_repo_path)
        repo_has_changes = drugbank_git_repo.is_dirty()
        print("Repo has changes: " + "No" if repo_has_changes else "Yes")
        if repo_has_changes:
            print("Adding changes via Git...")
            drugbank_git_repo.git.add(all=True)
            drugbank_git_repo.index.commit("DrugBank Version: " + latest_update['created_at'])
            drugbank_git_repo.create_tag(latest_update['id'])
            print("Changes added.")
            if latest_update['format'] == 'CSV':
                load_postgresql_database()


def load_postgresql_database(drugbank_csv_path):
    # Execute shell script to run a new docker container and load new version of the drugbank postgresql db
    # See folder docker/create_drugbank_db_container.sh
    pass
