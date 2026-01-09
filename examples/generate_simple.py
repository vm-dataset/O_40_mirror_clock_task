#!/usr/bin/env python3
"""
Simple Python script to generate mirror clock tasks.

This is a minimal example showing how to use the generator in Python code.
"""

from pathlib import Path
from core import OutputWriter
from src import TaskGenerator, TaskConfig

# Configuration
num_samples = 50
output_dir = Path("data/questions")
random_seed = 42  # Set to None for random generation
generate_videos = True

# Create configuration
config = TaskConfig(
    num_samples=num_samples,
    random_seed=random_seed,
    output_dir=output_dir,
    generate_videos=generate_videos,
)

# Generate dataset
print(f"Generating {num_samples} mirror clock tasks...")
generator = TaskGenerator(config)
tasks = generator.generate_dataset()

# Write to disk
writer = OutputWriter(output_dir)
writer.write_dataset(tasks)

print(f"✅ Generated {len(tasks)} tasks in {output_dir}/{config.domain}_task/")

