import re
from ctnx import num_to_words
from vietnam_number import n2w_single

from core.n2w_handler.converter.base import BaseNSWConverter


class TelConverter(BaseNSWConverter):
    def convert(self, category: str, value: str) -> str:
        if category == "tel":
            return self.tel_convert(value=value)
        return value

    def tel_convert(value: str) -> str:
        value = value.strip()
        value = value.replace("(", "").replace(")", "")
        
        prefix_match = re.match(r"(\+84|84)", value)
        if prefix_match:
          value = "0" + value[prefix_match.end():].strip()

        return n2w_single(value)
        