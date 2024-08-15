#!/bin/bash

TARGET_DIR_TIMESCALEDB="/mnt/data/AGC_data/timescale_data"
TARGET_DIR_GRAFANA="/mnt/data/AGC_data/grafana_data"
TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES="/mnt/data/AGC_data/grafana_provisioning/datasources/"

mkdir -p "$TARGET_DIR_TIMESCALEDB"
mkdir -p "$TARGET_DIR_GRAFANA"
mkdir -p "$TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES"

chmod 777 "$TARGET_DIR_TIMESCALEDB"
chmod 777 "$TARGET_DIR_GRAFANA"
chmod 777 "$TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES"

cp ./datasources.yaml "$TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES"

echo "Directory $TARGET_DIR_TIMESCALEDB has been created and permissions set to 777."
echo "Directory $TARGET_DIR_GRAFANA has been created and permissions set to 777."
echo "Directory $TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES has been created and permissions set to 777."
echo "./datasources.yaml has been copied to $TARGET_DIR_GRAFANA_PROVISIONING_DATASOURCES."