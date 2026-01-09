"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MIRROR CLOCK TASK CONFIGURATION                            ║
║                                                                               ║
║  Configuration for mirror clock reasoning task generator.                     ║
║  Inherits common settings from core.GenerationConfig                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Mirror clock task configuration.
    
    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name (mirror_clock)
        - difficulty: Optional[str] # Difficulty level (easy/medium/hard)
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════
    
    domain: str = Field(default="mirror_clock")
    image_size: tuple[int, int] = Field(default=(500, 500))
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )
    
    video_fps: int = Field(
        default=10,
        description="Video frame rate"
    )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    balanced_difficulty: bool = Field(
        default=True,
        description="Whether to generate balanced dataset across difficulty levels"
    )
    
    clock_size: int = Field(
        default=500,
        description="Clock image size (width and height)"
    )
