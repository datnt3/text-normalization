import os
from dotenv import load_dotenv, find_dotenv


# Load environment variables from .env file
load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Data
DATA_PATH = "data_storage/raw/the-thao_7.csv"
DATA_COLUMN = "text"
LABELED_DATA_DIR = "data_storage/processed"
LABELED_DATA_FILE = "processed_data.csv"
# LABELED_DATA_FILE = "processed_data_test.csv"
# regex: "[0-9]+[\\/\\-\\.][0-9]+"

# OpenAI Model
OPENAI_MODEL = "gpt-4o-mini"

# Prompts
USER_PROMPT ="""
You are tasked with transforming a Vietnamese paragraph that contains non-standard words into its corresponding spoken phonetic Vietnamese form.

Your goal is to identify the non-standard words from the given paragraph, which may include links, dates, times, measures, addresses, numbers, currencies, telephone numbers, Roman numerals, scores, fractions, ratios, special characters, and words that are abbreviations or loanwords.

For each non-standard word, you must:
- Normalize it by converting it into spoken phonetic Vietnamese.
- Expand abbreviations to their full forms.
- Convert loanwords into their Vietnamese phonetic equivalents.

Pay special attention to the type "Word," which includes abbreviations (e.g., "ĐHBKHN" to "Đại học Bách Khoa Hà Nội") and loanwords (e.g., "YouTube" to "Diu-túp").

# Output Format

The output should be a single paragraph in Vietnamese where all non-standard words have been transformed appropriately into their phonetic forms. Ensure that the paragraph remains cohesive and clear.

# Examples

**Example 1:**
- **Input:** "Đại học Bách Khoa Hà Nội là một trong những trường đại học kỹ thuật hàng đầu tại Việt Nam, được thành lập năm 1956. Với bề dày lịch sử hơn 60 năm, ĐHBKHN đã trở thành cái nôi đào tạo hàng nghìn kỹ sư, nhà khoa học và chuyên gia công nghệ xuất sắc, đóng góp tích cực vào sự phát triển của đất nước"
- **Output:** "Đại học Bách Khoa Hà Nội là một trong những trường đại học kỹ thuật hàng đầu tại Việt Nam, được thành lập năm một ngìn chín trăm năm mươi sáu. Với bề dày lịch sử hơn sáu mươi năm, đại học bách khoa hà nội đã trở thành cái nôi đào tạo hàng nghìn kỹ sư, nhà khoa học và chuyên gia công nghệ xuất sắc, đóng góp tích cực vào sự phát triển của đất nước"

**Example 2:**
- **Input:** "huấn luyện viên Philippe Troussier chỉ ra nguyên nhân khiến U việt nam thua Indonesia đáng tiếc 2-3 ở trận bán kết Seagame 2018 là do thiếu bản lĩnh kinh nghiệm nhưng không vì thế mà ông mất niềm tin vào các cầu thủ"
- **Output:** "huấn luyện viên phi-líp tru-xi-ê chỉ ra nguyên nhân khiến u việt nam thua in-đô-nê-xi-a đáng tiếc hai ba ở trận bán kết xi ghêm hai nghìn không trăm mười tám là do thiếu bản lĩnh kinh nghiệm nhưng không vì thế mà ông mất niềm tin vào các cầu thủ"

**Example 3:**
- **Input:** "điều này đồng nghĩa những mẫu Iphone đã 5-6 năm tuổi như Iphone 6S, Iphone 6S Plus và Iphone SE vẫn được Apple hỗ trợ cập nhật lên IOS 16 mới nhất vào 3/2/2019"
- **Output:** "điều này đồng nghĩa những mẫu ai-phôn đã từ năm đến sáu năm tuổi như ai-phôn sáu ét, ai-phôn sáu ét p-lớt và ai-phôn se vẫn được áp-pồ hỗ trợ cập nhật lên ai-ô-ét mười sáu mới nhất vào ngày ba tháng 2 năm hai nghìn không trăm mười chín"

# Notes

Ensure that all transformations are accurate and consider the context in which the non-standard words are used. Maintain the coherence of the paragraph while making the transformations.
"""

# Logging
LOGGING_DATA_FILE="data_label.log"