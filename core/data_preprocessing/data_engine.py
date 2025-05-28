from core.data_preprocessing.components.data_label import DataLabel
from core.data_preprocessing.components.data_preprocessing import DataPreprocessing
from core.data_preprocessing.components.data_raw import DataRaw
from core.config.config import (
    OPENAI_API_KEY, DATA_PATH, DATA_COLUMN, RAW_DATA_DIR
)


class DataEngine(object):
    def __init__(self, data_path, data_column):
        self.data_path = data_path
        self.data_column = data_column

    def start_engine(self):
        datas = DataRaw.get_generator_data(RAW_DATA_DIR)

        data_label = DataLabel()
        labeled_datas = data_label.label_data(raw_datas_generator=datas)
    
    def tag_data_nsw(self):
        data_label = DataLabel()
        pass
        
    