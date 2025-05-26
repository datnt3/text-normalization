FROM library/busybox

WORKDIR /app

COPY data_storage/train_test/2025-05-25 /app/data_storage/train_test
COPY data_storage/processed/2025-05-25/vn-text-norm-300k-v2 /app/data_storage/