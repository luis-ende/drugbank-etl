#!/bin/bash

DISK_USAGE_REPORT=$(df -hT)
DRUGBANK_USAGE_REPORT=$(du -h --max-depth=0 /opt/demo_drugbank/data/drugbank_json /opt/demo_drugbank/data/drugbank_csv/)
REPORT_DATE=$(date)

echo "--- sil.supnapps.com Disk Usage Report $REPORT_DATE ---" >> logs/sil_disk_usage.log
echo "$DISK_USAGE_REPORT" >> logs/sil_disk_usage.log
echo "--- DrugBank directories disk usage report ---" >> logs/sil_disk_usage.log
echo "$DRUGBANK_USAGE_REPORT" >> logs/sil_disk_usage.log