FROM library/busybox

WORKDIR /app

COPY data_storage/dataset/2025-06-07/gwen_vn_text_norm_dataset /app/data_storage/dataset/2025-06-07/qwen-text-norm-dataset
# COPY data_storage/processed/2025-05-25/vn-text-norm-300k-v2 /app/data_storage/