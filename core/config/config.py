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
# NSW_TAGGED_DATA_FILE = "nsw_tagged_data.csv"
NSW_TAGGED_DATA_FILE = "retagged_data.csv"
WRONG_TAGS_DATA_FILE = "wrong_tags_data.csv"
TRUE_TAGS_DATA_FILE = "true_tags_data.csv"

TRAIN_DATA_DIR = "vn-text-norm-300k-v2"
RAW_DATA_DIR = "data_storage/raw"

TRAIN_TEST_DATA_DIR = "data_storage/train_test"
TEST_DATA_FILE = "test_data.csv"
TRAIN_DATA_FILE = "train_data.csv"
TEST_RATIO = 0.2

RAW_DATA_LENGTH = 500

DATA_CHECKPOINT_DIR = "data_storage/checkpoints"
DATA_CHECKPOINT_FILE = "data_checkpoints.json"
NSW_TAGGED_CHECKPOINT_FILE = "nsw_tagged_checkpoints.json"

# OpenAI Model
OPENAI_MODEL = "gpt-4o-mini"

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
    "s_output": "Kỉ niệm thành lập công ty lần thứ bốn, lương của tôi được tăng từ một triệu đến hai triệu việt nam đồng."
  }
  
  
### Notes
  - Must not return sentences containing no numbers.
  - Pay strong attention to date, telephone format.
  - Remember to handle edge cases, such as multiple NSW in a single sentence or different formats of dates and times.
  - Ensure that all transformations are accurate with the most natural and proper manner in Vietnamese. Consider the context in which the numerical non-standard words are used and maintain the coherence of the paragraph while making the transformations.
"""

NSW_LIST = [
    "dmdmy",
    "ddmy",
    "dmdm",
    "dmydmy",
    "mymy",
    "dmy",
    "mmy",
    "qqy",
    "ddm",
    "qq",
    "dd",
    "mm",
    "yy",
    "my",
    "dm",
    "qy",
    "hmshms",
    "hmhm",
    "msms",
    "hms",
    "hh",
    "t_mm",
    "ss",
    "hm",
    "ms",
    "hour",
    "tel",
    "math_operator",
    "currency_range",
    "currency",
    "measure_range",
    "measure",
    "num_int",
    "num_int1",
    "num_float",
    "range",
    "roman",
    "roman_range",
    "score",
    "fraction",
    "ratio"
]

# FIXME: Add rule to match confusing types: measure, currency, roman
REGEX_RULE_LIST = [
    {
        "name": "DMDMY",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[-–—−]\s*(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 1,
        "tag": "dmdmy"
    },
    {
        "name": "DDMY",
        "pattern": r"\b(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[-–—−]\s*(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})\b",
        "priority": 2,
        "tag": "ddmy"
    },
    {
        "name": "DMDM",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[-–—−]\s*(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])(?![\w\/])",
        "priority": 3,
        "tag": "dmdm"
    },
    {
        "name": "DMYDMY",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})\s*[-–—−]\s*(?:ngày|ngay\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 4,
        "tag": "dmydmy"
    },
    {
        "name": "MYMY",
        "pattern": r"(?<![\w\/\.])(?:tháng|thang)?\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})\s*[-–—−]\s*(?:tháng|thang)?\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 5,
        "tag": "mymy"
    },
    {
        "name": "DMY",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)?\s*(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 6,
        "tag": "dmy"
    },
    {
        "name": "MMY",
        "pattern": r"(?<![\w\/\.])(?:tháng|thang)?\s*(0?[1-9]|1[0-2])\s*[-–—−]\s*(?:tháng|thang)?\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 7,
        "tag": "mmy"
    },
    {
        "name": "QQY",
        "pattern": r"(?<![\w\/\.])(?:quý|quy)\s*([0?[1-4]|I|II|III|IV])\s*[-–—−]\s*(?:quý|quy)?\s*([0?[1-4]|I|II|III|IV])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 8,
        "tag": "qqy"
    },
    {
        "name": "DDM",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)\s*(0?[1-9]|[12][0-9]|3[01])\s*[-–—−]\s*(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)?\s*(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])(?![\w\/])",
        "priority": 9,
        "tag": "ddm"
    },
    {
        "name": "QQ",
        "pattern": r"(?<![\w\/\.])(?:quý|quy)\s*([0?[1-4]|I|II|III|IV])\s*[-–—−]\s*(?:quý|quy)?\s*([0?[1-4]|I|II|III|IV])(?![\w\/])",
        "priority": 10,
        "tag": "qq"
    },
    {
        "name": "DD",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)\s*(0?[1-9]|[12][0-9]|3[01])\s*[-–—−]\s*(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)?\s*(0?[1-9]|[12][0-9]|3[01])(?![\w\/])",
        "priority": 11,
        "tag": "dd"
    },
    {
        "name": "MM",
        "pattern": r"(?<![\w\/\.])(?:tháng|thang)\s*(0?[1-9]|1[0-2])\s*[-–—−]\s*(?:tháng|thang)?\s*(0?[1-9]|1[0-2])(?![\w\/])",
        "priority": 12,
        "tag": "mm"
    },
    {
        "name": "YY",
        "pattern": r"(?<![\w\/\.])(?:năm|nam)\s*([0-9]{1,4})\s*[-–—−]\s*(?:năm|nam)?\s*([0-9]{1,4})(?![\w\/])",
        "priority": 13,
        "tag": "yy"
    },
    {
        "name": "MY",
        "pattern": r"(?<![\w\/\.])(?:tháng|thang)\s*(0?[1-9]|1[0-2])\s*[\.\/\-]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 14,
        "tag": "my"
    },
    {
        "name": "DM",
        "pattern": r"(?<![\w\/\.])(?:ngày|ngay|sáng|sang|trưa|trua|chiều|chieu|tối|toi)\s*(0?[1-9]|[12][0-9]|3[01])\s*[\.\/\-]\s*(0?[1-9]|1[0-2])(?![\w\/])",
        "priority": 15,
        "tag": "dm"
    },
    {
        "name": "QY",
        "pattern": r"(?<![\w\/\.])(?:quý|quy)\s*([0?[1-4]|I|II|III|IV])\s*[\.\/\-]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 16,
        "tag": "qy"
    },
    {  # dang thay do
        "name": "HMSHMS",
        "pattern": r"\b(\d{1,2})[hg:](\d{1,2})[mp':\u2032](\d{1,2})(?:''|'|s|\u2032\u2032|\u2032)?\s*[-–—−]\s*(\d{1,2})[hg:](\d{1,2})[mp':\u2032](\d{1,2})(?:''|'|s|\u2032\u2032|\u2032)?(?=\W|$)",
        "priority": 17,
        "tag": "hmshms"
    },
    {
        "name": "HMHM",
        "pattern": r"\b(\d{1,2})[hg:](\d{1,2})(?:[p'\u2032m]?)\s*[-–—−]\s*(\d{1,2})[hg:](\d{1,2})(?:[p'\u2032m]?)(?=\W|$)",
        "priority": 18,
        "tag": "hmhm"
    },
    {
        "name": "MSMS",
        "pattern": r"\b(\d{1,2})[p':\u2032](\d{1,2})(?:''|'|s|\u2032\u2032|\u2032)?\s*[-–—−]\s*(\d{1,2})[p':\u2032](\d{1,2})(?:''|'|s|\u2032\u2032|\u2032)?(?=\W|$)",
        "priority": 19,
        "tag": "msms"
    },
    {
        "name": "HMS",
        "pattern": r"\b(\d{1,2})[hg:](\d{1,2})[mp':\u2032](\d{1,2})(?:''|'|s|\u2032\u2032|\u2032)?(?=\W|$)",
        "priority": 20,
        "tag": "hms"
    },
    {
        "name": "HH",
        "pattern": r"\b(\d{1,2})\s*[hg]?\s*[-–—−]\s*(\d{1,2})\s*[hg]\b",
        "priority": 21,
        "tag": "hh"
    },
    {
        "name": "T_MM",
        "pattern": r"\b(\d{1,2})\s*[p'\u2032]?\s*[-–—−]\s*(\d{1,2})\s*[p'\u2032](?=\W|$)",
        "priority": 22,
        "tag": "t_mm"
    },
    {
        "name": "SS",
        "pattern": r"\b(\d{1,2})\s*(?:''|s|\u2032\u2032)?\s*[-–—−]\s*(\d{1,2})\s*(?:''|s|\u2032\u2032)(?=\W|$)",
        "priority": 23,
        "tag": "ss"
    },
    {
        "name": "HM",
        "pattern": r"\b(\d{1,2})[hg](\d{1,2})[mp'\u2032]?(?=\W|$)",
        "priority": 24,
        "tag": "hm"
    },
    {
        "name": "MS",
        "pattern": r"\b(\d{1,2})[p'\u2032](\d{1,2})(?:''|s|\u2032\u2032)?(?=\W|$)",
        "priority": 25,
        "tag": "ms"
    },
    {
        "name": "TEL1",
        "pattern": r"(?<!\w)(?:\(?\+?84\)?)[-. ]?((?:\d[ .]?){9,10})(?!\w)",
        "priority": 26,
        "tag": "tel"
    },
    {
        "name": "TEL2",
        "pattern": r"(?<!\w)(\(?0\d{2}\)?)[-. ]?((?:\d[ .]?){8})(?!\w)",
        "priority": 27,
        "tag": "tel"
    },
    {
        "name": "TEL3",
        "pattern": r"(?<!\w)0[-. ]?((?:\d[ .]?){9})(?!\w)",
        "priority": 28,
        "tag": "tel"
    },
    {
        "name": "TEL4",
        "pattern": r"(?<!\w)1[8|9]00[-. ]?((?:\d[ .]?){4,6})(?!\w)",
        "priority": 29,
        "tag": "tel"
    },
    {
        "name": "MATH_OPERATOR",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))(?:\s?([\+\*x])\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))){1,2}(?![\w])",
        "priority": 30,
        "tag": "math_operator"
    },
    {
        "name": "CURRENCY_RANGE",
        "pattern": r"(?<![\w])(((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)?\s?[-–—−]\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)|(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?[-–—−]\s?(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)?\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0)))(?![\w])",
        "priority": 31,
        "tag": "currency_range"
    },
    {
        "name": "CURRENCY",
        "pattern": r"(?<![\w])(((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)|(\$|€|¥|£|₫|chf|cad|aud|nzd|sgd|hkd|cny|usd|eur|jpy|gbp|krw|inr|vnd|vnđ|php)\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0)))(?![\w])",
        "priority": 32,
        "tag": "currency"
    },
    {
        "name": "HOUR_MEASURE",
        "pattern": r"(?<![\w])((?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?g(?![\w])",
        "priority": 33,
        "tag": ""
    },
    {
        "name": "MEASURE_RANGE",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(l\/100km|(?:km|cm|m|mg|mmol)\/(?:h|s|l|kg)|[khdcmμnp][gm]|m\d{0,5}|in|J|kJ|cal|kcal|Wh|kWh|W|kW|MW|m²|km2|km²|cm2|cm²|ft2|ft²|ha|L|mL|m³|cm³|cm3|oz|°C|Hz|kHz|GHz|B|KB|MB|GB|TB|\%)?\s?[-–—−]\s?((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(l\/100km|(?:km|cm|m|mg|mmol)\/(?:h|s|l|kg)|[khdcmμnp][gm]|m\d{0,5}|in|J|kJ|cal|kcal|Wh|kWh|W|kW|MW|m²|km2|km²|cm2|cm²|ft2|ft²|ha|L|mL|m³|cm³|cm3|oz|°C|Hz|kHz|GHz|B|KB|MB|GB|TB|\%)(?![\w])",
        "priority": 34,
        "tag": "measure_range"
    },
    {
        "name": "MEASURE",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5},\d+|\d+,\d+|[1-9][0-9]{0,2}(?:\.[0-9]{3}){1,5}|[1-9][0-9]{0,14}000|[1-9][0-9]{0,6}|0))\s?(l\/100km|(?:km|cm|m|mg|mmol)\/(?:h|s|l|kg)|[khdcmμnp][gm]|m\d{0,5}|in|J|kJ|cal|kcal|Wh|kWh|W|kW|MW|m²|km2|km²|cm2|cm²|ft2|ft²|ha|L|mL|m³|cm³|cm3|oz|°C|Hz|kHz|GHz|B|KB|MB|GB|TB|\%)(?![\w])",
        "priority": 35,
        "tag": "measure"
    },
    {
        "name": "RANGE",
        "pattern": r"(?<!\w)((\d+,\d+)\s*[-–—−]\s*(\d+(?:,\d+)?)|(\d+(?:,\d+)?)\s*[-–—−]\s*(\d+,\d+))(?![\w\,])",
        "priority": 36,
        "tag": "range"
    },
    {
        "name": "FRACTION",
        "pattern": r"(?<!\w)((\d+,\d+)\s*\/\s*(\d+(?:,\d+)?)|(\d+(?:,\d+)?)\s*\/\s*(\d+,\d+))(?![\w\,])",
        "priority": 37,
        "tag": "fraction"
    },
    {
        "name": "NUM:NUM",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6})):((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))(?![\w])",
        "priority": 38,
        "tag": ""
    },
    {
        "name": "NUM-NUM",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))\s*[-–—−]\s*((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))(?![\w])",
        "priority": 39,
        "tag": ""
    },
    {
        "name": "NUM/NUM",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))\s*/\s*((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))(?![\w])",
        "priority": 40,
        "tag": ""
    },
    {
        "name": "NUM_INT1",
        "pattern": r"(?<![\d\.])((?:\\-|\\+)?(?:[1-9][0-9]{0,2}(?:[\.][0-9]{3}){1,5}))(?!\w)",
        "priority": 41,
        "tag": "num_int1"
    },
    {
        "name": "NUM.NUM",
        "pattern": r"(?<![\w])((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))\.((?:\-|\+)?(?:[0-9][0-9]{0,2}(?:[\.][0-9]{3}){0,5}|[0-9][0-9]{0,14}[0]{3}|[0-9][0-9]{0,6}))(?![\w])",
        "priority": 42,
        "tag": ""
    },
    {
        "name": "NUM_FLOAT",
        "pattern": r"(\d+,\d+)",
        "priority": 43,
        "tag": "num_float"
    },
    {
        "name": "NUM_INT",
        "pattern": r"(?<![\d\.])((?:\\-|\\+)?(?:[1-9][0-9]{0,2}(?:[\\.][0-9]{3}){1,5}|[1-9][0-9]{0,14}[0]{3}|[1-9][0-9]{0,6}|0))",
        "priority": 44,
        "tag": "num_int"
    },
    {
        "name": "ROMAN_RANGE",
        "pattern": r"(?<!\w)([IVX]{1,5})\s?[-–—−]\s?([IVX]{1,5})(?!\w)",
        "priority": 45,
        "tag": "roman_range"
    },
    {
        "name": "ROMAN",
        "pattern": r"(?<!\w)(chương|phần|mục|bài|quyển|tập|điều|khoản|phụ lục|mục lục|số|thứ|lần|kỷ|kỉ|kì|kỳ|khóa)\s?([IVX]{1,5})(?!\w)",
        "priority": 46,
        "tag": "roman"
    },
]

CONFUSED_NSW_DICT = {
    "HOUR_MEASURE": {
        "true_labels": """
        - HOUR: Hour format
        - MEASURE: Gram unit in measurement units
        """,
        "examples": """
        - **Input**: Ngày hôm nay ~3/10#DM, tôi đi khỏi nhà lúc ~5g#HOUR_MEASURE
        - **Output**: {
            "tagged_sentence": "Ngày hôm nay ~3/10#DM, tôi đi khỏi nhà lúc ~5g#HOUR"
            "tags": "HOUR"
        }
        - **Input**: Lúc ~19h#HOUR_MEASURE, tôi đi chợ mua ~1.000g#HOUR_MEASURE muối
        - **Output**: {
            "tagged_sentence": "Lúc ~19h#HOUR, tôi đi chợ mua ~1.0000g#MEASURE muối"
            "tags": "HOUR, MEASURE"
        }
        """,
    },
    "NUM:NUM": {
        "true_labels": """
        - RATIO: ratio between two numbers
        - HM: Hours and Minutes format
        - MS: Minutes and Seconds format
        """,
        "examples": """
        - **Input**: Nhà tắm nên chọn ~2#NUM_INT màu gạch chia ngang phần tường thành ~2#NUM_INT mảng màu theo tỷ lệ ~1:1#NUM:NUM
        - **Output**: {
            "tagged_sentence": "Nhà tắm nên chọn ~2#NUM_INT màu gạch chia ngang phần tường thành ~2#NUM_INT mảng màu theo tỷ lệ ~1:1#RATIO"
            "tags": "RATIO"
        }
        - **Input**: Lúc ~15:30#NUM:NUM, tôi chia bánh theo tỉ lệ ~1:3#NUM:NUM
        - **Output**: {
            "tagged_sentence": "Lúc ~15:30#HM, tôi chia bánh theo tỉ lệ ~1:3#RATIO"
            "tags": "HM, RATIO"
        }
        - **Input**: Việt Nam thắng vào phút ~15:30#NUM:NUM
        - **Output**: {
            "tagged_sentence": "Việt Nam thắng vào phút ~15:30#MS"
            "tags": "MS"
        }
        """,
    },
    "NUM-NUM": {
        "true_labels": """
        - RANGE: a span of values between two numbers
        - SCORE: Numerical results
        - DM: Date and Month format
        - MY: Month and Year format
        """,
        "examples": """
        - **Input**: Cũng trong ~chiều 23/4#DM, Thường trực Huyện ủy Vĩnh Lộc đã họp và thống nhất cho ông Hà Nguyên Phấn không ứng cử đại biểu HĐND xã khóa XX, nhiệm kỳ ~2021-2026#NUM-NUM.
        - **Output**: {
            "tagged_sentence": "Cũng trong ~chiều 23/4#DM, Thường trực Huyện ủy Vĩnh Lộc đã họp và thống nhất cho ông Hà Nguyên Phấn không ứng cử đại biểu HĐND xã khóa XX, nhiệm kỳ ~2021-2026#RANGE"
            "tags": "RANGE"
        }
        - **Input**: ~3/10#NUM-NUM, cuối hiệp ~1#NUM_INT, tỷ số được nâng lên ~2-0#NUM-NUM cũng sau một đường tấn công biên.
        - **Output**: {
            "tagged_sentence": "~3/10#DM, cuối hiệp ~1#NUM_INT, tỷ số được nâng lên ~2-0#SCORE cũng sau một đường tấn công biên."
            "tags": "DM, SCORE"
        }
        - **Input**: Từ ~8-2024#NUM-NUM đến ~9-2024#NUM-NUM, tôi đi công tác.
        - **Output**: {
            "tagged_sentence": "Từ ~8-2024#MY đến ~9-2024#MY, tôi đi công tác."
            "tags": "MY"
        }
        """,
    },
    "NUM/NUM": {
        "true_labels": """
        - FRACTION: a part of a whole
        - DM: Date and Month format
        - MY: Month and Year format
        """,
        "examples": """
        - **Input**: Sáng nay, ~5/10#NUM/NUM, ~8#NUM_INT đội bóng đã bước vào trận thi đấu đầu tiên.
        - **Output**: {
            "tagged_sentence": "Sáng nay, ~5/10#DM, ~8#NUM_INT đội bóng đã bước vào trận thi đấu đầu tiên."
            "tags": "DM"
        }
        - **Input**: Đến nay, ~19/10#NUM/NUM, MU đã thua ~3/6#NUM/NUM trận tại Premier League và tụt xuống thứ ~12#NUM_INT trên BXH
        - **Output**: {
            "tagged_sentence": "Đến nay, ~19/10#DM, MU đã thua ~3/6#FRACTION trận tại Premier League và tụt xuống thứ ~12#NUM_INT trên BXH"
            "tags": "DM, FRACTION"
        }
        - **Input**: Từ ~8/2024#NUM/NUM, anh ấy định cư ở Mỹ.
        - **Output**: {
            "tagged_sentence": "Từ ~8/2024#MY, anh ấy định cư ở Mỹ."
            "tags": "MY"
        }
        """,
    },
    "NUM.NUM": {
        "true_labels": """
        - NUM_FLOAT: a floating-point number
        - DM: Date and Month format
        - MY: Month and Year format
        """,
        "examples": """
        - **Input**: Bên cạnh đó, chị cũng nhận được phần thưởng ~5000#NUM_INT Đô la Hồng Kong (tương đương hơn ~13.5#NUM.NUM triệu VNĐ).
        - **Output**: {
            "tagged_sentence": "Bên cạnh đó, chị cũng nhận được phần thưởng ~5000#NUM_INT Đô la Hồng Kong (tương đương hơn ~13.5#NUM_FLOAT triệu VNĐ)."
            "tags": "NUM_FLOAT"
        }
        - **Input**: Hôm nay, ~08.09#NUM.NUM, Perez đã chiêu mộ Luis Figo của Barcelona với mức giá ~71.6#NUM.NUM triệu euro
        - **Output**: {
            "tagged_sentence": "Hôm nay, ~08.09#DM, Perez đã chiêu mộ Luis Figo của Barcelona với mức giá ~71.6#NUM_FLOAT triệu euro"
            "tags": "DM, NUM_FLOAT"
        }
        - **Input**: Từ ~10.2025#NUM.NUM, mức phạt cho việc vượt đèn đỏ là ~10.5#NUM.NUM triệu.
        - **Output**: {
            "tagged_sentence": "Từ ~10.2025#MY, mức phạt cho việc vượt đèn đỏ là ~10.5#NUM_FLOAT triệu."
            "tags": "MY, NUM_FLOAT"
        }
        """,
    },
}

NSW_TAG_PROMPT = """
Based on the context of the sentence, classify the {category} category non-standard words which is placed in the pattern ~NSW#{category} into one of these labels:
{true_labels}
Replace the true labels back into the sentence.

### Output Format

The output must be structured in JSON format, with each element containing the following fields:
  - **tagged_sentence**: The full sentence containing the numerical non-standard words with the true label classified.
  - **tags**: The string containing all new tags classified, seperated by comma.
  
### Example

{examples}

### Notes

- Remember to focus on the context of the sentence to enhance classifying quality.
- Ensure that all classifications are accurate and the tags list returned contains enough number of new labels.
"""


# Logging
LOGGING_CONFIG_FILE = "core/config/logging_config.conf"
