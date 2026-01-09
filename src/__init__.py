"""
Mirror clock task implementation.

Main components:
    - config.py   : Mirror clock task configuration (TaskConfig)
    - generator.py: Mirror clock task generation logic (TaskGenerator)
    - prompts.py  : Mirror clock task prompts/instructions (get_prompt)
"""

from .config import TaskConfig
from .generator import TaskGenerator
from .prompts import get_prompt

__all__ = ["TaskConfig", "TaskGenerator", "get_prompt"]
