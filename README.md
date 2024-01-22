# Data Ingestion Pipeline from DrugBank

* Make sure pycurl is installed or run `sudo apt install python3-pycurl` Also take a look at the dependencies in the `requirements.txt` file 
* Copy `pipeline.conf.example` over `pipeline.conf` and set credentials on sections `[drugbank_credentials]` and `[etl_drugbank_postgresql]`
* Section `[etl_drugbank_paths]` contains the paths to working directories for the DrugBank files by format
* Find the scripts to run the PostgreSql docker container under the `docker` directory
* To access the PostgreSql database (Docker) via shell use:
  * `docker exec -it drugbank-postgres bash`
  * `su postgres`
  * `psql`
  * `\c drugbank`
* A log file with the updates applied by the pipeline is stored under `./logs/latest_updates.json`