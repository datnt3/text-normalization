import re
from typing import List
from core.data_preprocessing.data_augmentation.number_generator.base import (
    BaseGenerator,
)
from core.data_preprocessing.data_augmentation.number_rand import NumberRand

NUM_GEN = 5


class DateGenerator(BaseGenerator):
    def generate(self, category: str, value: str) -> List[str]:
        if category == "dmdmy":
            return self.dmdmy_generate(value)
        if category == "ddmy":
            return self.ddmy_generate(value)
        if category == "dmdm":
            return self.dmdm_generate(value)
        if category == "dmydmy":
            return self.dmydmy_generate(value)
        if category == "mymy":
            return self.mymy_generate(value)
        if category == "dmy":
            return self.dmy_generate(value)
        if category == "mmy":
            return self.mmy_generate(value)
        if category == "qqy":
            return self.qqy_generate(value)
        if category == "ddm":
            return self.ddm_generate(value)
        # if category == "qq":
        #     return self.qq_generate(value)
        # if category == "dd":
        #     return self.dd_generate(value)
        # if category == "mm":
        #     return self.mm_generate(value)
        # if category == "yy":
        #     return self.yy_generate(value)
        # if category == "my":
        #     return self.my_generate(value)
        # if category == "dm":
        #     return self.dm_generate(value)
        # if category == "qy":
        #     return self.qy_generate(value)

    def dmdmy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    day0 = NumberRand.day_rand()
                    month0 = NumberRand.month_rand()
                    sample += f"{prefix}{day0}{seperator}{month0} - "
                else:
                    day1 = NumberRand.day_rand(day0)
                    month1 = NumberRand.month_rand(month0)
                    year1 = NumberRand.year_rand()
                    sample += f"{prefix}{day1}{seperator}{month1}{seperator}{year1}"
            generated_list.append(sample.strip())
        return generated_list

    def ddmy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    day0 = NumberRand.day_rand()
                    sample += f"{prefix}{day0} - "
                else:
                    day1 = NumberRand.day_rand(day0)
                    month1 = NumberRand.month_rand()
                    year1 = NumberRand.year_rand()
                    sample += f"{prefix}{day1}{seperator}{month1}{seperator}{year1}"
            generated_list.append(sample.strip())
        return generated_list

    def dmdm_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(ngày)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    day0 = NumberRand.day_rand()
                    month0 = NumberRand.month_rand()
                    sample += f"{prefix}{day0}{seperator}{month0} - "
                else:
                    day1 = NumberRand.day_rand(day0)
                    month1 = NumberRand.month_rand(month0)
                    sample += f"{prefix}{day1}{seperator}{month1}"
            generated_list.append(sample.strip())
        return generated_list

    def dmydmy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    day0 = NumberRand.day_rand()
                    month0 = NumberRand.month_rand()
                    year0 = NumberRand.year_rand()
                    sample += f"{prefix}{day0}{seperator}{month0}{seperator}{year0} - "
                else:
                    day1 = NumberRand.day_rand(day0)
                    month1 = NumberRand.month_rand(month0)
                    year1 = NumberRand.year_rand(year0)
                    sample += f"{prefix}{day1}{seperator}{month1}{seperator}{year1}"
            generated_list.append(sample.strip())
        return generated_list

    def mymy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(tháng)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    month0 = NumberRand.month_rand()
                    year0 = NumberRand.year_rand()
                    sample += f"{prefix}{month0}{seperator}{year0} - "
                else:
                    month1 = NumberRand.month_rand(month0)
                    year1 = NumberRand.year_rand(year0)
                    sample += f"{prefix}{month1}{seperator}{year1}"
            generated_list.append(sample.strip())
        return generated_list

    def dmy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", value)
        prefix = prefix_match.group(0) if prefix_match else ""

        for _ in range(NUM_GEN):
            seperator = NumberRand.date_seperator_rand()
            day = NumberRand.day_rand()
            month = NumberRand.month_rand()
            year = NumberRand.year_rand()
            sample = f"{prefix}{day}{seperator}{month}{seperator}{year}"

            generated_list.append(sample.strip())
        return generated_list

    def mmy_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(tháng)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    month0 = NumberRand.month_rand()
                    sample += f"{prefix}{month0} - "
                else:
                    month1 = NumberRand.month_rand(month0)
                    year1 = NumberRand.year_rand()
                    sample += f"{prefix}{month1}{seperator}{year1}"
            generated_list.append(sample.strip())
        return generated_list

    def qqy_generate(self, value: str) -> List[str]:
        pass

    def ddm_generate(self, value: str) -> List[str]:
        generated_list = []

        value = value.strip()
        parts = re.split(r"[-–—−]", value)
        if len(parts) != 2:
            print("Wrong format")
            return value

        for _ in range(NUM_GEN):
            sample = ""
            seperator = NumberRand.date_seperator_rand()

            for i in range(len(parts)):
                parts[i] = parts[i].strip()
                prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
                prefix = prefix_match.group(0) if prefix_match else ""

                if i == 0:
                    day0 = NumberRand.day_rand()
                    sample += f"{prefix}{day0} - "
                else:
                    day1 = NumberRand.day_rand(day0)
                    month1 = NumberRand.month_rand()
                    sample += f"{prefix}{day1}{seperator}{month1}"
            generated_list.append(sample.strip())
        return generated_list
