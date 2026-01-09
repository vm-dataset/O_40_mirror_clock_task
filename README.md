# Mirror Clock Task Data Generator 🕐

This task generator follows the [template-data-generator](https://github.com/vm-dataset/template-data-generator.git) format and is compatible with [VMEvalKit](https://github.com/Video-Reason/VMEvalKit.git).

Repository: [O_40_mirror_clock_task](https://github.com/vm-dataset/O_40_mirror_clock_task)

---

A data generator for mirror clock reasoning tasks. Generates tasks that combine spatial reasoning (mirror transformations) with temporal reasoning (future time prediction).

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/vm-dataset/O_40_mirror_clock_task.git
cd O_40_mirror_clock_task

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python3 examples/generate.py --num-samples 50
```

---

## 📁 Structure

```
mirror-clock-task-data-generator/
├── core/                    # ✅ KEEP: Standard utilities
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # ⚠️ CUSTOMIZE: Mirror clock task logic
│   ├── generator.py        # Mirror clock task generator
│   ├── prompts.py          # Mirror clock prompt templates
│   └── config.py           # Mirror clock configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## 📦 Output Format

Every generator produces:

```
data/questions/mirror_clock_task/{task_id}/
├── first_frame.png          # Mirrored clock (horizontally flipped)
├── final_frame.png          # Future time clock (original time + delta)
├── prompt.txt               # Instructions (REQUIRED)
└── ground_truth.mp4         # Solution video (OPTIONAL)
```

---

## 🎯 Task Description

The Mirror Clock Reasoning Task evaluates video generation models' ability to combine:
1. **Spatial Reasoning**: Understanding horizontal mirror transformations
2. **Temporal Reasoning**: Calculating future time by adding a specified duration

### Example:
- **First Frame**: Mirrored clock showing flipped 3:00
- **Prompt**: "This is a mirrored clock. If the original clock moves forward by 2 hours, what time will it show?"
- **Final Frame**: Clock showing 5:00 (the answer)

### Difficulty Levels:
- **Easy**: Exact hours (3:00, 6:00), full hours only (1-3 hours)
- **Medium**: 5-minute intervals (2:30, 4:15), hours with 30-minute intervals
- **Hard**: Any minute (3:25, 7:47), any time combination (0-3 hours, 0-59 minutes)

---

## 📝 Configuration

The generator supports balanced difficulty distribution across easy/medium/hard levels.

**Key Configuration** (`src/config.py`):

```python
class TaskConfig(GenerationConfig):
    domain: str = Field(default="mirror_clock")
    image_size: tuple[int, int] = Field(default=(500, 500))
    clock_size: int = Field(default=500)
    balanced_difficulty: bool = Field(default=True)
    generate_videos: bool = Field(default=True)
    video_fps: int = Field(default=10)
```

**Single entry point:** `python3 examples/generate.py --num-samples 50`

---

## 🎨 Customization

The generator is built on a flexible framework. To customize:

### 1. Modify `src/generator.py`
- Adjust clock rendering (font, colors, size)
- Change time generation logic
- Customize video generation parameters

### 2. Update `src/prompts.py`
- Add or modify prompt templates
- Adjust time delta formatting

### 3. Configure `src/config.py`
- Adjust clock size and image dimensions
- Modify difficulty distributions
- Enable/disable video generation

---

## 🔧 Usage Examples

```bash
# Generate 50 tasks with balanced difficulty
python3 examples/generate.py --num-samples 50

# Generate 100 tasks with specific output directory
python3 examples/generate.py --num-samples 100 --output data/my_output

# Generate with random seed for reproducibility
python3 examples/generate.py --num-samples 50 --seed 42

# Generate without videos
python3 examples/generate.py --num-samples 50 --no-videos
```

---

## 📊 Generated Data

Each task includes:
- **first_frame.png**: Clock viewed through a mirror (horizontally flipped)
- **final_frame.png**: Clock showing the calculated future time
- **prompt.txt**: Natural language instruction with time delta
- **ground_truth.mp4**: Solution video showing the reasoning process (optional)

### Ground Truth Video

The ground truth video (`ground_truth.mp4`) demonstrates the complete reasoning process:

1. **Initial State**: Shows the mirrored clock (horizontally flipped)
2. **Transition**: Smooth crossfade animation from mirrored clock to future time
3. **Final State**: Displays the calculated future time clock

The video uses a crossfade transition with:
- 10 frames holding the initial mirrored clock
- 20 frames for smooth transition
- 10 frames holding the final future time clock
- Default frame rate: 10 fps

This provides a visual reference for the expected reasoning sequence that video generation models should produce.

---

## 🧠 Cognitive Abilities Tested

1. **Spatial Reasoning**: Understanding horizontal mirror transformations
2. **Visual Processing**: Interpreting mirrored clock hand positions
3. **Mental Arithmetic**: Adding hours and minutes with carryover
4. **Multi-Step Reasoning**: Combining spatial and temporal reasoning
5. **Abstract Thinking**: Managing two transformations (mirror + time addition)

---

## 📄 License

See LICENSE file for details.
