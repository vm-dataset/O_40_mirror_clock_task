"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MIRROR CLOCK TASK GENERATOR                                ║
║                                                                               ║
║  Generates mirror clock reasoning tasks combining spatial (mirror)           ║
║  and temporal (time addition) reasoning.                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import math
import random
import tempfile
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

from core import BaseGenerator, TaskPair
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class ClockRenderer:
    """Clock face rendering utility"""
    
    def __init__(self, image_size: int = 500):
        """
        Initialize clock renderer
        
        Args:
            image_size: Size of the clock image (width and height)
        """
        self.image_size = image_size
        self.center = image_size // 2
        self.clock_radius = int(image_size * 0.4)
        self.hour_hand_length = int(self.clock_radius * 0.5)
        self.minute_hand_length = int(self.clock_radius * 0.7)
    
    def _draw_clock_face(self, draw: ImageDraw.Draw):
        """Draw the basic clock face with numbers"""
        # Draw outer circle
        draw.ellipse(
            [
                self.center - self.clock_radius,
                self.center - self.clock_radius,
                self.center + self.clock_radius,
                self.center + self.clock_radius
            ],
            outline='#333333',
            width=4,
            fill='#ffffff'
        )
        
        # Try to load a nice font
        font_size = int(self.image_size * 0.07)  # Responsive font size
        try:
            # Try system fonts
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Draw hour numbers
        for hour in range(1, 13):
            angle = math.radians(90 - (hour * 30))  # 12 is at top (90 degrees)
            x = self.center + int((self.clock_radius * 0.75) * math.cos(angle))
            y = self.center - int((self.clock_radius * 0.75) * math.sin(angle))
            
            hour_str = str(hour)
            bbox = draw.textbbox((0, 0), hour_str, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            draw.text(
                (x - text_width // 2, y - text_height // 2),
                hour_str,
                fill='#333333',
                font=font
            )
        
        # Draw center dot
        center_dot_radius = max(4, int(self.image_size * 0.016))
        draw.ellipse(
            [
                self.center - center_dot_radius,
                self.center - center_dot_radius,
                self.center + center_dot_radius,
                self.center + center_dot_radius
            ],
            fill='#333333'
        )
    
    def _draw_hand(self, draw: ImageDraw.Draw, angle_degrees: float,
                   length: int, width: int, color: str):
        """
        Draw a clock hand
        
        Args:
            angle_degrees: Angle in degrees (0 = 12 o'clock, clockwise)
            length: Length of the hand
            width: Width of the hand
            color: Color of the hand
        """
        # Convert to radians (subtract 90 to make 0 degrees point up)
        angle_rad = math.radians(angle_degrees - 90)
        
        end_x = self.center + int(length * math.cos(angle_rad))
        end_y = self.center + int(length * math.sin(angle_rad))
        
        draw.line(
            [self.center, self.center, end_x, end_y],
            fill=color,
            width=width
        )
    
    def draw_clock(self, hours: int, minutes: int) -> Image.Image:
        """
        Draw a clock showing the specified time
        
        Args:
            hours: Hour (0-23, will be converted to 12-hour)
            minutes: Minutes (0-59)
            
        Returns:
            PIL Image of the clock
        """
        # Create image
        img = Image.new('RGB', (self.image_size, self.image_size), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw clock face
        self._draw_clock_face(draw)
        
        # Convert to 12-hour format
        hours_12 = hours % 12
        
        # Calculate angles
        # Hour hand: moves 30 degrees per hour + 0.5 degrees per minute
        hour_angle = (hours_12 * 30) + (minutes * 0.5)
        # Minute hand: moves 6 degrees per minute
        minute_angle = minutes * 6
        
        # Draw hands (minute hand first, then hour hand on top)
        hand_width = max(3, int(self.image_size * 0.012))
        self._draw_hand(draw, minute_angle, self.minute_hand_length, hand_width, '#666666')
        self._draw_hand(draw, hour_angle, self.hour_hand_length, hand_width + 2, '#333333')
        
        return img


class TaskGenerator(BaseGenerator):
    """
    Mirror Clock Task Generator
    
    Generates tasks where:
    1. First frame: Mirrored clock (horizontally flipped)
    2. Final frame: Future time clock (original time + time delta)
    3. Prompt: Instructions to determine future time from mirrored clock
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        clock_size = config.clock_size if hasattr(config, 'clock_size') else config.image_size[0]
        self.clock_renderer = ClockRenderer(image_size=clock_size)
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one mirror clock task pair."""
        
        # Determine difficulty if not specified
        difficulty = self.config.difficulty
        if difficulty is None:
            difficulty = random.choice(["easy", "medium", "hard"])
        
        # Generate random time based on difficulty
        hours, minutes = self._generate_random_time(difficulty)
        
        # Generate time delta to add
        add_hours, add_minutes = self._generate_time_delta(difficulty)
        
        # Calculate future time
        future_hours, future_minutes = self._add_time(hours, minutes, add_hours, add_minutes)
        
        # Generate original clock image
        original_image = self.clock_renderer.draw_clock(hours, minutes)
        
        # Create mirrored version by flipping horizontally (first frame)
        mirrored_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Generate future clock image (final frame)
        future_image = self.clock_renderer.draw_clock(future_hours, future_minutes)
        
        # Generate video if enabled
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(mirrored_image, future_image, task_id, original_image)
        
        # Format time delta string for prompt
        time_delta_str = self._format_time_delta(add_hours, add_minutes)
        
        # Select prompt
        prompt = get_prompt(time_delta_str)
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=mirrored_image,
            final_image=future_image,
            ground_truth_video=video_path
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO GENERATION
    # ══════════════════════════════════════════════════════════════════════════
    
    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str,
        original_image: Image.Image
    ) -> Optional[str]:
        """
        Generate ground truth video showing step-by-step reasoning process.
        
        Steps:
        1. Show mirrored clock (first frame)
        2. Flip back to original clock (reasoning step)
        3. Show future clock (final answer)
        
        Args:
            first_image: Mirrored clock image (start frame)
            final_image: Future clock image (end frame)
            task_id: Task ID for naming the video file
            original_image: Original clock image (unmirrored, intermediate step)
            
        Returns:
            Path to video file, or None if generation fails
        """
        if not self.video_generator:
            return None
        
        # Create temporary directory for videos
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        # Generate step-by-step video frames
        frames = []
        
        # Step 1: Hold mirrored clock (first frame) - 15 frames
        for _ in range(15):
            frames.append(first_image.copy())
        
        # Step 2: Transition from mirrored to original clock - 20 frames
        mirrored_rgba = first_image.convert('RGBA')
        original_rgba = original_image.convert('RGBA')
        if mirrored_rgba.size != original_rgba.size:
            original_rgba = original_rgba.resize(mirrored_rgba.size, Image.Resampling.LANCZOS)
        
        for i in range(20):
            alpha = i / (20 - 1) if 20 > 1 else 1.0
            blended = Image.blend(mirrored_rgba, original_rgba, alpha)
            frames.append(blended.convert('RGB'))
        
        # Hold original clock - 15 frames (showing reasoning step)
        for _ in range(15):
            frames.append(original_image.copy())
        
        # Step 3: Transition from original to future clock - 20 frames
        future_rgba = final_image.convert('RGBA')
        if original_rgba.size != future_rgba.size:
            future_rgba = future_rgba.resize(original_rgba.size, Image.Resampling.LANCZOS)
        
        for i in range(20):
            alpha = i / (20 - 1) if 20 > 1 else 1.0
            blended = Image.blend(original_rgba, future_rgba, alpha)
            frames.append(blended.convert('RGB'))
        
        # Hold future clock (final frame) - 15 frames
        for _ in range(15):
            frames.append(final_image.copy())
        
        # Create video from frames
        result = self.video_generator.create_video_from_frames(frames, video_path)
        
        return str(result) if result else None
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TIME GENERATION METHODS
    # ══════════════════════════════════════════════════════════════════════════
    
    def _generate_random_time(self, difficulty: str) -> Tuple[int, int]:
        """
        Generate a random time based on difficulty
        
        Args:
            difficulty: easy, medium, or hard
            
        Returns:
            (hours, minutes) tuple
        """
        if difficulty == "easy":
            # Only hour marks (no minutes)
            hours = random.randint(1, 12)
            minutes = 0
        elif difficulty == "medium":
            # 5-minute intervals
            hours = random.randint(1, 12)
            minutes = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        else:  # hard
            # Any minute
            hours = random.randint(1, 12)
            minutes = random.randint(0, 59)
        
        return hours, minutes
    
    def _generate_time_delta(self, difficulty: str) -> Tuple[int, int]:
        """
        Generate a time delta based on difficulty
        
        Args:
            difficulty: easy, medium, or hard
            
        Returns:
            (hours_to_add, minutes_to_add) tuple
        """
        if difficulty == "easy":
            # Only add full hours (1-3 hours)
            return random.randint(1, 3), 0
        elif difficulty == "medium":
            # Add hours with 30-minute intervals
            hours = random.randint(0, 2)
            minutes = random.choice([0, 30])
            # Ensure at least some time is added
            if hours == 0 and minutes == 0:
                hours = 1
            return hours, minutes
        else:  # hard
            # Any time combination (0-3 hours, 0-59 minutes)
            hours = random.randint(0, 3)
            minutes = random.randint(0, 59)
            # Ensure at least some time is added
            if hours == 0 and minutes == 0:
                minutes = random.randint(15, 45)
            return hours, minutes
    
    def _add_time(self, hours: int, minutes: int,
                  add_hours: int, add_minutes: int) -> Tuple[int, int]:
        """
        Add time to a given time
        
        Args:
            hours: Original hours
            minutes: Original minutes
            add_hours: Hours to add
            add_minutes: Minutes to add
            
        Returns:
            (new_hours, new_minutes) tuple
        """
        total_minutes = minutes + add_minutes
        extra_hours = total_minutes // 60
        new_minutes = total_minutes % 60
        
        new_hours = (hours + add_hours + extra_hours) % 24
        
        return new_hours, new_minutes
    
    def _format_time_delta(self, hours: int, minutes: int) -> str:
        """
        Format time delta as a string for prompts
        
        Args:
            hours: Hours to add
            minutes: Minutes to add
            
        Returns:
            Formatted string like "2 hours" or "1 hour and 30 minutes"
        """
        if hours == 0:
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif minutes == 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
    
    def generate_dataset(self):
        """Generate dataset with optional balanced difficulty distribution"""
        if hasattr(self.config, 'balanced_difficulty') and self.config.balanced_difficulty:
            return self._generate_balanced_dataset()
        else:
            return super().generate_dataset()
    
    def _generate_balanced_dataset(self):
        """Generate balanced dataset across difficulty levels"""
        difficulties = ["easy", "medium", "hard"]
        samples_per_difficulty = self.config.num_samples // len(difficulties)
        remaining = self.config.num_samples % len(difficulties)
        
        pairs = []
        task_counter = 0
        
        for difficulty in difficulties:
            count = samples_per_difficulty + (1 if remaining > 0 else 0)
            remaining -= 1
            
            # Temporarily set difficulty
            original_difficulty = self.config.difficulty
            self.config.difficulty = difficulty
            
            for i in range(count):
                task_id = f"{self.config.domain}_{task_counter:04d}"
                pair = self.generate_task_pair(task_id)
                pairs.append(pair)
                print(f"  Generated: {task_id} (difficulty: {difficulty})")
                task_counter += 1
            
            # Restore original difficulty
            self.config.difficulty = original_difficulty
        
        return pairs
