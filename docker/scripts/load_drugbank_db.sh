#!/bin/bash

# Data loading script used by the drugbank-postgresql Docker image build

cd /opt/drugbank-data
su drugbank-admin
psql -d drugbank -f create_schema.pgsql.sql
psql -d drugbank -f load_tables.pgsql.sql
psql -d drugbank -f add_constraints.pgsql.sql