#!/bin/sh

set -e

echo "🕒 Waiting for MinIO to be ready..."

until mc alias set minio-server http://$MINIO_SERVER_NAME:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"; do
    echo "⌛ MinIO not ready yet..."
    sleep 2
done

echo "✅ MinIO is reachable"

for BUCKET in $BUCKETS; do
    if ! mc ls minio-server/$BUCKET > /dev/null 2>&1; then
        echo "📁 Creating bucket: $BUCKET"
        mc mb minio-server/$BUCKET
    else
        echo "✔️ Bucket $BUCKET already exists"
    fi
done

echo "✅ All buckets initialized!"
