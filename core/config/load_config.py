import yaml
from omegaconf import DictConfig

def load_config(path: str):
  with open(path, "r") as f:
    config = yaml.safe_load(f)
  
  return DictConfig(config)