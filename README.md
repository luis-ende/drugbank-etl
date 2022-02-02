# SaS Data Ingestion Pipeline from DrugBank

* Copy `pipeline.conf.example` over `pipeline.conf` and set credentials on sections `[drugbank_credentials]` and `[supernus_drugbank_postgresql]`
* Section `[supernus_drugbank_paths]` contains the paths to working directories for the DrugBank files by format
* Find the scripts to run the PostgreSql docker container under the `docker` directory