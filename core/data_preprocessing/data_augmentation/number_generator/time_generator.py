import re
from typing import List
from core.data_preprocessing.data_augmentation.number_generator.base import (
    BaseGenerator,
)
from core.data_preprocessing.data_augmentation.number_rand import NumberRand

NUM_GEN = 5


class TimeGenerator(BaseGenerator):
    def generate(self, category: str, value: str) -> List[str]:
        if category == "hmhm":
            return self.hmhm_generate(value)
        if category == "hm":
            return self.hm_generate(value)

    def hmhm_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            hour_postfix, min_postfix = NumberRand.hour_min_postfix_rand()

            hour0 = NumberRand.hour_rand()
            minute0 = NumberRand.minute_rand()

            hour1 = NumberRand.hour_rand(hour0)
            minute1 = NumberRand.minute_rand(minute0)

            sample += f"{hour0}{hour_postfix}{minute0}{min_postfix} - {hour1}{hour_postfix}{minute1}{min_postfix}"
            generated_list.append(sample.strip())
        return generated_list
