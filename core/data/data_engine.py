from core.data.components.data_label import DataLabel
from core.data.components.data_preprocessing import DataPreprocessing
from core.data.components.data_raw import DataRaw
from core.config.config import (
    OPENAI_API_KEY, DATA_PATH, DATA_COLUMN
)


class DataEngine(object):
    def __init__(self, data_path, data_column):
        self.data_path = data_path
        self.data_column = data_column

    def start_engine(self):
        text_datas = DataRaw.get_data(
            self.data_path, self.data_column)

        data_label = DataLabel()
        labeled_datas = data_label.label_data(text_datas[2737:])