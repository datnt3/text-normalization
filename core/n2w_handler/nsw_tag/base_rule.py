import re
from typing import Dict, List
import rootutils

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.config.config import REGEX_RULE_LIST

class RegexRule:
    def __init__(self, name: str, pattern: str, priority: int):
        self.name = name
        self.pattern = re.compile(pattern=pattern, flags=re.IGNORECASE)
        self.priority = priority


class Rule:
    def __init__(self, rules: List):                                                    
        self.rules = []
        for rule in rules:
            regex_rule = RegexRule(
                name=rule["name"], pattern=rule["pattern"], priority=rule["priority"]
            )
            self.rules.append(regex_rule)

    def apply_rule(self, raw_sentence: str):
        match_names = []
        matched_spans = []  # List of matched (start, end)
        for rule in self.rules:
            pattern, name = rule.pattern, rule.name
            matches = list(pattern.finditer(raw_sentence))
            for match in matches:
                is_overlap = False
                for matched_start, matched_end in matched_spans:
                    if not (
                        match.end() <= matched_start or match.start() >= matched_end
                    ):  # If overlap
                        is_overlap = True

                if not is_overlap:
                    matched_spans.append((match.start(), match.end()))
                    match_names.append((match, name))

        return match_names

    def tag_sentence(self, raw_sentence: str, match_names: List[tuple]):
        tags = []
        match_infos = []
        for match, name in match_names:
          start = match.start()
          end = match.end()
          match_text = match.group()
          match_infos.append((start, end, match_text, name))
          if name not in tags: 
            tags.append(name)
        match_infos.sort(reverse=True, key= lambda x : x[0])

        tagged_sentence = raw_sentence
        for start, end, match_text, name in match_infos:
            tagged_text = f"~{match_text}#{name}"
            tagged_sentence = tagged_sentence[:start] + tagged_text + tagged_sentence[end:]
        
        return tagged_sentence, tags

    

if __name__ == "__main__":
    rule = Rule(REGEX_RULE_LIST)
    # print(REGEX_RULE_LIST)

    sentence = "Hôm qua, FIFA đã công bố 10 đề cử cho giải Puskas (Bàn thắng đẹp nhất năm). Đây là những bàn thắng đẹp nhất được FIFA lựa chọn trong khoảng thời gian từ tháng 10/2015 đến tháng 10/2016."
    match_names = rule.apply_rule(sentence)
    for match, name in match_names:
        print(name)
        print(match.group())
    
    tagged_sentence, tags = rule.tag_sentence(sentence, match_names)
    
    print("\n"+tagged_sentence)
    print(tags)

    print("\ndone")
