#!/usr/bin/env python3
"""
Mirror Clock Task Data Generator

Complete example script for generating mirror clock reasoning task datasets.

Usage:
    python3 examples/generate_data.py
    python3 examples/generate_data.py --num-samples 100
    python3 examples/generate_data.py --num-samples 50 --output data/my_dataset --seed 42
    python3 examples/generate_data.py --num-samples 50 --no-videos
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import OutputWriter
from src import TaskGenerator, TaskConfig


def main():
    parser = argparse.ArgumentParser(
        description="Generate mirror clock reasoning task dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate 50 tasks with default settings (balanced difficulty, with videos)
    python3 examples/generate_data.py --num-samples 50
    
    # Generate 100 tasks with custom output directory
    python3 examples/generate_data.py --num-samples 100 --output data/my_dataset
    
    # Generate with specific random seed for reproducibility
    python3 examples/generate_data.py --num-samples 50 --seed 42
    
    # Generate without videos (faster, smaller output)
    python3 examples/generate_data.py --num-samples 50 --no-videos
    
    # Generate with specific difficulty level
    python3 examples/generate_data.py --num-samples 30 --difficulty easy
        """
    )
    
    parser.add_argument(
        "--num-samples",
        type=int,
        default=50,
        help="Number of task samples to generate (default: 50)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="data/questions",
        help="Output directory (default: data/questions)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: None)"
    )
    
    parser.add_argument(
        "--no-videos",
        action="store_true",
        help="Disable video generation (default: videos enabled)"
    )
    
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["easy", "medium", "hard"],
        default=None,
        help="Specific difficulty level (default: balanced distribution across all levels)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🕐 Mirror Clock Task Data Generator")
    print("=" * 70)
    print(f"📊 Number of samples: {args.num_samples}")
    print(f"📁 Output directory: {args.output}")
    print(f"🎲 Random seed: {args.seed if args.seed else 'None (random)'}")
    print(f"🎥 Video generation: {'Disabled' if args.no_videos else 'Enabled'}")
    print(f"📈 Difficulty: {args.difficulty if args.difficulty else 'Balanced (easy/medium/hard)'}")
    print("=" * 70)
    print()
    
    # Create configuration
    config = TaskConfig(
        num_samples=args.num_samples,
        random_seed=args.seed,
        output_dir=Path(args.output),
        generate_videos=not args.no_videos,
        difficulty=args.difficulty,
    )
    
    # Create generator and generate dataset
    print("🎲 Generating tasks...")
    generator = TaskGenerator(config)
    tasks = generator.generate_dataset()
    
    # Write to disk
    print(f"💾 Writing {len(tasks)} tasks to disk...")
    writer = OutputWriter(Path(args.output))
    writer.write_dataset(tasks)
    
    # Summary
    print()
    print("=" * 70)
    print("✅ Generation Complete!")
    print("=" * 70)
    print(f"📁 Output location: {Path(args.output).absolute() / config.domain}_task/")
    print(f"📦 Total tasks: {len(tasks)}")
    
    if not args.no_videos:
        print(f"🎥 Videos: Generated ({config.video_fps} fps)")
    else:
        print(f"🎥 Videos: Disabled")
    
    print("=" * 70)
    print()
    print("Generated files per task:")
    print("  - first_frame.png      (mirrored clock)")
    print("  - final_frame.png      (future time clock)")
    print("  - prompt.txt           (instructions)")
    if not args.no_videos:
        print("  - ground_truth.mp4     (solution video)")
    print()


if __name__ == "__main__":
    main()

