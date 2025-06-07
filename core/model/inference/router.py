import re
import rootutils
rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)
from core.config.regex_config import AUGMENT_REGEX_RULES

class Router(object):
    def __init__(self, rules=AUGMENT_REGEX_RULES):
        self.rules = rules
    
    def check_match_info(self, text, pattern):
        matchs = re.findall(pattern, text)
        return len(matchs) != 0
    
    def check_router(self, text):
        for rule in self.rules:
            pattern = rule['pattern']
            if self.check_match_info(text, pattern): return True
        return False
    
    def gateway(self, text):
        return "INFERENCE_REGEX_RULES" if self.check_router(text) else "NOT_INFERENCE_REGEX_RULES"
    
    
if __name__ == "__main__":
    text = "Hạn nộp hồ sơ là 01/05/2024, ngày phỏng vấn là 15-06-2025."
    router = Router()
    print(router.gateway(text))