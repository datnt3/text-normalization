FROM library/busybox

WORKDIR /app

COPY data_storage/train_test /app/data_storage/train_test
COPY data_storage/processed/vn-text-norm-300k /app/data_storage/train_test