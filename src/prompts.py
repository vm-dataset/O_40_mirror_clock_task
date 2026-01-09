"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           MIRROR CLOCK TASK PROMPTS                           ║
║                                                                               ║
║  Prompts for mirror clock reasoning tasks.                                    ║
║  Prompts use {time_delta} placeholder for dynamic time insertion.             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  MIRROR CLOCK TASK PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = [
    """This is a mirrored clock. Follow these steps:
Step 1: Look at the mirrored clock shown in the image.
Step 2: Flip it horizontally to determine the original time.
Step 3: Add {time_delta} to the original time.
What time will the original clock show after {time_delta}?""",
    
    """The image shows a horizontally flipped clock. Solve this step by step:
Step 1: Identify the mirrored clock in the image.
Step 2: Unmirror it to find the original time.
Step 3: Calculate the new time after {time_delta} passes.
What will be the final time?""",
    
    """This mirror-reflected clock needs to advance {time_delta}. Solve in steps:
Step 1: Observe the mirrored clock face.
Step 2: Flip it back to reveal the original time.
Step 3: Add {time_delta} to get the future time.
Show what the original clock will display after {time_delta}.""",
    
    """From this mirrored clock, determine the answer step by step:
Step 1: Examine the mirrored clock image.
Step 2: Determine the original time by unmirroring the clock.
Step 3: Add {time_delta} to the original time.
What is the result?""",
]


def get_prompt(time_delta: str = "1 hour") -> str:
    """
    Select a random prompt and fill in the time_delta placeholder.
    
    Args:
        time_delta: Time delta string (e.g., "2 hours", "1 hour and 30 minutes")
        
    Returns:
        Formatted prompt string
    """
    prompt_template = random.choice(PROMPTS)
    return prompt_template.format(time_delta=time_delta)


def get_all_prompts() -> list[str]:
    """Get all prompt templates."""
    return PROMPTS
