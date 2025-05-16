import typer
from typing import Optional, Annotated
from typer import Argument
import rootutils
rootutils.setup_root(__file__,
                     indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
                     pythonpath=True)
from core.config.load_config import load_config
from core.data_preprocessing.data_engine import DataEngine
from core.config.config import (
    OPENAI_API_KEY, DATA_PATH, DATA_COLUMN
)

app = typer.Typer()


@app.command("label_data")
# def label_data(config_path: Annotated[str, Argument(help="Path to config")]="core/config/config.yaml"):
#   config = load_config(config_path)
#   data_engine = DataEngine(config=config.data)
#   data_engine.start_engine()
def label_data():
    data_engine = DataEngine(data_path=DATA_PATH, data_column=DATA_COLUMN)
    data_engine.start_engine()
    
@app.command("create_test_data")
def create_test_data():
    pass


@app.command("train_model")
def train_model():
    pass


if __name__ == "__main__":
    app()
