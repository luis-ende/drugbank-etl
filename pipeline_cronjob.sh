#!/bin/bash

# Cronjob runs on server sil.supnapps.com

echo date
echo "Executing Drugbank's data ingestion cron job..."
cd /opt/sas_drugbank/sas-supernus-drugbank
python3 main.py

sh log_disk_usage.sh