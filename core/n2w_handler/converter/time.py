import re
from ctnx import num_to_words
from vietnam_number import n2w_single

from core.n2w_handler.converter.base import BaseNSWConverter


class TimeConverter(BaseNSWConverter):
  def convert(self, category: str, value: str) -> str:
    if category == "hm":
      pass
  

