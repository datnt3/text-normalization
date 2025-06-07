FROM library/busybox

WORKDIR /app

COPY data_storage/dataset/2025-06-07/vn_text_norm_augmented_dataset /app/data_storage/dataset/2025-06-07
# COPY data_storage/processed/2025-05-25/vn-text-norm-300k-v2 /app/data_storage/