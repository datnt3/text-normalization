FROM library/busybox

WORKDIR /app

COPY data_storage/dataset /app/data_storage/dataset
# COPY data_storage/processed/2025-05-25/vn-text-norm-300k-v2 /app/data_storage/