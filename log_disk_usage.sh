#!/bin/bash

DISK_USAGE_REPORT=$(df -hT)
REPORT_DATE=$(date)

echo "--- sil.supnapps.com Disk Usage Report $REPORT_DATE ---" >> logs/sil_disk_usage.log
echo "$DISK_USAGE_REPORT" >> logs/sil_disk_usage.log