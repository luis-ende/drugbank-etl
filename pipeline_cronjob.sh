#!/bin/bash

# Cronjob runs on server sil.supnapps.com

echo date
echo "Executing Drugbank's data ingestion cron job..."
cd /opt/demo_drugbank/sas-etl-drugbank
python3 main.py

sh log_disk_usage.sh