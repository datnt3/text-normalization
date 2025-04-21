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
# TRAIN_DATA_DIR = "vn-text-norm-8k"
TRAIN_DATA_DIR = "vn-text-norm-33k"
RAW_DATA_DIR = "data_storage/raw"

# LABELED_DATA_FILE = "processed_data_test.csv"
DATA_CHECKPOINT_DIR = "data_storage/checkpoints"
DATA_CHECKPOINT_FILE = "data_checkpoints.json"
# regex: "[0-9]+[\\/\\-\\.][0-9]+"

# OpenAI Model
OPENAI_MODEL = "gpt-4o-mini"

# Prompts
USER_PROMPT = """
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

SYSTEM_PROMPT = """
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]

# Examples [optional]

[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]
[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
"""

USER_PROMPT_FINAL = """
Extract the sentences from the provided Vietnamese paragraph that contain numerical non-standard words (NSW), which may include date, time, measure, address, number, currency, telephone, Roman number, score, fraction, ratio. Expand those numerical non-standard words into their phonetic spoken Vietnamese word equivalents.

### Steps

1. **Sentence Extraction**: Identify and extract all sentences from the Vietnamese paragraph that contain any numerical non-standard words. Remember that you must not return any sentence that contain no number.        
2. **Expansion to Spoken Words**: Convert each numerical non-standard word into its spoken phonetic Vietnamese form, integrating it back into the sentence.

### Output Format
 
The output must be structured in JSON format, with each element containing the following fields:
  - **input**: The full original raw sentence containing the numerical non-standard words.
  - **s_output**: The full sentence with the numerical non-standard words expanded into their spoken word equivalents.

### Example
  {
    "input": "Hôm nay là 3.12.2009, tôi nhận được cuộc gọi từ SĐT 0989170070 lúc 15h40p38s.",
    "s_output": "Hôm nay là ngày ba tháng mười hai năm hai nghìn không trăm lẻ chín, tôi nhận được cuộc gọi từ SĐT không chín tám chín một bảy không không bảy không lúc mười lăm giờ bốn mươi phút ba mươi tám giây."
  },
  {
    "input": "Hotline: 03.6969.6688 - 09.3206.3209",
    "s_output": "Hotline: không ba sáu chín sáu chín sáu sáu tám tám - không chín ba hai không sáu ba hai không chín"
  },
  {
    "input": "Cuộc gọi kéo dài 15 phút, trong đó 3/4 thời lượng là nói về cách pha nước cam theo tỉ lệ 1:2.",
    "s_output": "Cuộc gọi kéo dài mười lăm phút, trong đó ba phần tư thời lượng là nói về cách pha nước cam theo tỉ lệ một chia hai"
  },
  {
    "input": "Người gọi khoảng 31-34 tuổi, gọi trong khoảng từ ngày 13-16 tháng 12/2020.",
    "s_output": "Người gọi khoảng ba mươi mốt đến ba mươi tư tuổi, gọi trong khoảng từ ngày mười ba đến ngày mười sáu tháng mười hai năm hai nghìn không trăm hai mươi."
  }
  {
    "input": "Kỉ niệm thành lập công ty lần thứ IV, lương của tôi được tăng từ 1.000.000-2.000.000 VNĐ.",
    "s_output": "Kỉ niệm thành lập công ty lần thứ bốn, lương của tôi được tăng từ một triệu đến hai triệu VNĐ."
  }
  
  
### Notes
  - Must not return sentences containing no numbers.
  - Pay strong attention to date, telephone format.
  - Remember to handle edge cases, such as multiple NSW in a single sentence or different formats of dates and times.
  - Ensure that all transformations are accurate with the most natural and proper manner in Vietnamese. Consider the context in which the numerical non-standard words are used and maintain the coherence of the paragraph while making the transformations.
"""

# Logging
LOGGING_CONFIG_FILE = "core/config/logging_config.conf"
