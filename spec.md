# Black Hole Spacetime Visualization - Complete Implementation Spec

## Project Overview
Create a 60-90 second animated Manim video demonstrating how black holes curve spacetime and cause orbital motion. This implementation recreates the professional black hole visualization inspired by educational physics videos, featuring:

- **Black background** with **bold, readable text**
- **Blue wireframe spacetime grid** that warps dynamically
- **Smaller blue wireframe black hole** with **deeper spacetime curvature**
- **Orange wireframe event horizon** positioned behind text
- **Realistic orbital motion** with multiple white particles using Kepler's laws
- **Progressive animation sequence** building each concept step-by-step

This spec provides complete step-by-step instructions for recreating the project from scratch.

## Prerequisites & Setup

### 1. System Dependencies (macOS)
```bash
# Install required system libraries via Homebrew
brew install cairo pkg-config cmake
```

### 2. Python Environment Setup
```bash
# Create project directory
mkdir black-hole && cd black-hole

# Create requirements.txt
echo "manim\nnumpy" > requirements.txt

# Install dependencies using uv
uv pip install -r requirements.txt
```

## Implementation Steps

### Step 1: Create Main Scene File (`black_hole_scene.py`)

Create a ThreeDScene class with the following structure:

```python
from manim import *
import numpy as np

class HowBlackHolesWorkScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Scene sequence
        self.intro_grid()
        self.add_black_hole()
        self.show_event_horizon()
        self.demonstrate_orbital_motion()
        self.outro()
```

### Step 2: Implement Intro Grid Method

```python
def intro_grid(self):
    # Blue 3D spacetime grid
    self.spacetime_grid = Surface(
        lambda u, v: np.array([u, v, 0]),
        u_range=[-6, 6],
        v_range=[-6, 6],
        resolution=(20, 20),
        fill_opacity=0.3,
        stroke_color=BLUE,
        stroke_width=1
    )
    
    # Spacetime label (fixed in frame for 3D scenes)
    self.spacetime_label = Text("Spacetime", color=BLUE, font_size=36)
    self.spacetime_label.to_corner(UL)
    self.add_fixed_in_frame_mobjects(self.spacetime_label)
    
    # Animate grid appearing
    self.play(Create(self.spacetime_grid), run_time=2)
    self.play(Write(self.spacetime_label))
    self.wait(1)
```

**Key Implementation Notes:**
- Use `Surface` with flat lambda function for initial grid
- Use `add_fixed_in_frame_mobjects()` instead of deprecated `fix_in_frame()`
- Set appropriate resolution (20x20) for performance

### Step 3: Implement Black Hole and Spacetime Curvature

```python
def add_black_hole(self):
    # Create warped spacetime grid
    def warped_surface(u, v):
        r_squared = u**2 + v**2
        # Avoid division by zero and create smooth curvature
        warp_factor = 3 / (1 + r_squared/2)
        z = -warp_factor * np.exp(-r_squared/8)
        return np.array([u, v, z])
    
    self.warped_grid = Surface(
        warped_surface,
        u_range=[-6, 6],
        v_range=[-6, 6],
        resolution=(30, 30),  # Higher resolution for curved surface
        fill_opacity=0.3,
        stroke_color=BLUE,
        stroke_width=1
    )
    
    # Black hole sphere
    self.black_hole = Sphere(radius=0.7, resolution=(20, 20))
    self.black_hole.set_fill(BLACK, opacity=1)
    self.black_hole.set_stroke(WHITE, width=0.5)
    self.black_hole.move_to([0, 0, -0.5])  # Position in warped area
    
    # Labels
    self.curvature_label = Text("Spacetime Curvature", color=YELLOW, font_size=36)
    self.curvature_label.to_corner(UR)
    self.add_fixed_in_frame_mobjects(self.curvature_label)
    
    self.black_hole_label = Text("Black Hole", color=WHITE, font_size=32)
    self.black_hole_label.next_to(self.black_hole, DOWN, buff=1)
    self.add_fixed_in_frame_mobjects(self.black_hole_label)
    
    # Transform grid and add black hole
    self.play(
        Transform(self.spacetime_grid, self.warped_grid),
        FadeIn(self.black_hole),
        run_time=3
    )
    self.play(
        Write(self.curvature_label),
        Write(self.black_hole_label)
    )
    self.wait(2)
```

**Key Implementation Notes:**
- Use mathematical warping function with exponential decay
- Increase resolution to 30x30 for smoother curved surface
- Position black hole at z=-0.5 to sit in the warped depression

### Step 4: Implement Event Horizon

```python
def show_event_horizon(self):
    # Event horizon as orange wireframe sphere
    self.event_horizon = Sphere(radius=1.2, resolution=(15, 15))
    self.event_horizon.set_stroke(ORANGE, width=2)
    self.event_horizon.set_fill(ORANGE, opacity=0.1)
    self.event_horizon.move_to([0, 0, -0.3])  # Slightly above black hole
    
    # Event horizon label with arrow
    self.horizon_label = Text("Event Horizon", color=ORANGE, font_size=32)
    self.horizon_label.to_edge(LEFT)
    self.add_fixed_in_frame_mobjects(self.horizon_label)
    
    # Arrow pointing to event horizon
    self.horizon_arrow = Arrow(
        start=self.horizon_label.get_right() + RIGHT * 0.5,
        end=[0, 0, 0],
        color=ORANGE
    )
    self.add_fixed_in_frame_mobjects(self.horizon_arrow)
    
    # Animate event horizon appearance with pulsing effect
    self.play(
        Create(self.event_horizon),
        Write(self.horizon_label),
        Create(self.horizon_arrow),
        run_time=2
    )
    
    # Pulsing effect
    self.play(
        self.event_horizon.animate.scale(1.1),
        rate_func=rate_functions.there_and_back,
        run_time=1
    )
    self.wait(1)
```

**Key Implementation Notes:**
- Make event horizon larger than black hole (radius 1.2 vs 0.7)
- Use semi-transparent fill with visible stroke
- Use `there_and_back` rate function for pulsing effect

### Step 5: Implement Orbital Motion

```python
def demonstrate_orbital_motion(self):
    # Create orbital paths at different radii
    orbit_radius_1 = 2.5
    orbit_radius_2 = 3.5
    
    # Orbital bodies
    self.orbiter_1 = Sphere(radius=0.15, resolution=(8, 8))
    self.orbiter_1.set_fill(GRAY, opacity=0.8)
    self.orbiter_1.move_to([orbit_radius_1, 0, 0])
    
    self.orbiter_2 = Sphere(radius=0.12, resolution=(8, 8))
    self.orbiter_2.set_fill(GRAY_C, opacity=0.8)
    self.orbiter_2.move_to([orbit_radius_2, 0, 0.2])  # Slight z offset
    
    # Orbital motion label
    self.orbital_label = Text("Orbital Motion", color=ORANGE, font_size=32)
    self.orbital_label.to_corner(DR)
    self.add_fixed_in_frame_mobjects(self.orbital_label)
    
    # Add orbiters and label
    self.play(
        FadeIn(self.orbiter_1),
        FadeIn(self.orbiter_2),
        Write(self.orbital_label),
        run_time=1
    )
    
    # Animate orbital motion using updaters
    def orbit_updater_1(mob, dt):
        mob.rotate(dt * 0.8, axis=UP, about_point=ORIGIN)
    
    def orbit_updater_2(mob, dt):
        mob.rotate(dt * 0.6, axis=UP, about_point=ORIGIN)
    
    self.orbiter_1.add_updater(orbit_updater_1)
    self.orbiter_2.add_updater(orbit_updater_2)
    
    # Camera movement for better view
    self.move_camera(theta=45 * DEGREES, run_time=2)
    
    # Let orbits run
    self.wait(4)
    
    # Remove updaters
    self.orbiter_1.remove_updater(orbit_updater_1)
    self.orbiter_2.remove_updater(orbit_updater_2)
```

**Key Implementation Notes:**
- Use different rotation speeds (0.8 vs 0.6) for realistic orbital mechanics
- Position orbiters at different z-heights to avoid collision
- Use updater functions for continuous rotation
- Remember to remove updaters to prevent memory leaks

### Step 6: Implement Outro

```python
def outro(self):
    # Reset camera
    self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)
    
    # Fade out all elements except grid
    elements_to_fade = [
        self.black_hole, self.event_horizon, self.orbiter_1, self.orbiter_2,
        self.spacetime_label, self.curvature_label, self.black_hole_label,
        self.horizon_label, self.horizon_arrow, self.orbital_label
    ]
    
    self.play(*[FadeOut(element) for element in elements_to_fade], run_time=2)
    
    # Reset grid to flat
    flat_grid = Surface(
        lambda u, v: np.array([u, v, 0]),
        u_range=[-6, 6],
        v_range=[-6, 6],
        resolution=(20, 20),
        fill_opacity=0.3,
        stroke_color=BLUE,
        stroke_width=1
    )
    
    self.play(Transform(self.spacetime_grid, flat_grid), run_time=2)
    
    # Final title
    final_title = Text("How Black Holes Work", color=WHITE, font_size=48)
    self.add_fixed_in_frame_mobjects(final_title)
    
    self.play(Write(final_title), run_time=2)
    self.wait(2)
```

## Critical Implementation Details

### 1. 3D Scene Text Positioning
- **Always use** `self.add_fixed_in_frame_mobjects()` for text in ThreeDScene
- **Never use** `fix_in_frame()` (deprecated in current Manim version)

### 2. Surface Resolution Optimization
- Flat surfaces: 20x20 resolution for performance
- Curved surfaces: 30x30 resolution for smoothness
- Spheres: Vary resolution based on size and importance

### 3. Mathematical Warping Function (Enhanced)
```python
def warped_surface(u, v):
    r_squared = u**2 + v**2
    # Much deeper warping effect for dramatic visualization
    warp_factor = 6 / (1 + r_squared/2)  # Increased from 3 to 6
    z = -warp_factor * np.exp(-r_squared/4)  # Deeper curve (4 instead of 8)
    return np.array([u, v, z])
```

### 4. Realistic Orbital Physics
```python
def create_orbit_updater(radius, initial_angle):
    def orbit_updater(mob, dt):
        # Kepler's laws approximation (closer orbits = faster)
        speed = 1.5 / np.sqrt(radius)
        current_pos = mob.get_center()
        angle = np.arctan2(current_pos[1], current_pos[0])
        angle += dt * speed
        z = current_pos[2]
        # Add slight wobble for realistic motion
        wobble = 0.05 * np.sin(angle * 3)
        new_radius = radius + wobble
        mob.move_to([new_radius * np.cos(angle), new_radius * np.sin(angle), z])
    return orbit_updater
```

### 4. Visual Design Specifications
- **Background**: `self.camera.background_color = BLACK`
- **Camera**: Initial position `phi=65°, theta=-30°`
- **Grid**: Reduced resolution (15x15 flat, 20x20 warped) with thicker strokes (2.0)
- **Black hole**: Smaller radius (0.6) positioned deeper (z=-1.8)
- **Text**: All labels use `weight=BOLD` and larger font sizes (28-48px)
- **Event horizon**: Positioned at z=-1.2 (behind black hole label)

### 5. Camera and Animation Timing
- Use `self.move_camera()` instead of `self.camera.frame.animate` in ThreeDScene
- Smooth transitions: 2-3 seconds
- Orbital motion: 5 seconds with realistic physics
- Total duration: ~60-90 seconds

## Common Troubleshooting

### macOS Cairo Issues
If you get Cairo/pkg-config errors:
```bash
brew install cairo pkg-config cmake
```

### Missing ffmpeg Warning
The warning about ffmpeg can be ignored for basic rendering, but install for advanced features:
```bash
brew install ffmpeg
```

### Text Not Appearing in 3D
Always use `add_fixed_in_frame_mobjects()` for any text or 2D elements in ThreeDScene.

### Camera Control Issues
In ThreeDScene, use `self.move_camera()` instead of `self.camera.frame.animate`. The correct syntax is:
```python
# Correct for ThreeDScene
self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)

# Incorrect (will cause AttributeError)
self.play(self.camera.frame.animate.set_phi(75 * DEGREES))
```

## File Structure
```
black-hole/
├── black_hole_scene.py    # Main animation file
├── requirements.txt       # Dependencies (manim, numpy)
├── README.md             # Usage instructions
├── spec.md               # This specification
└── media/                # Generated video output (created by Manim)
    └── videos/
        └── black_hole_scene/
            └── 480p15/
                └── HowBlackHolesWorkScene.mp4
```

## Git Repository Setup

### 1. Initialize Git Repository
```bash
# Initialize git repository
git init

# Add all source files (excluding generated content via .gitignore)
git add .
git commit -m "Initial commit: Black hole spacetime visualization

🔧 Features:
- 3D spacetime grid with curvature warping
- Black hole sphere with event horizon
- Orbital motion animation with camera movements
- Complete Manim implementation with proper 3D controls

🚀 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 2. Optional: Add Remote Repository
```bash
# If you want to push to GitHub/GitLab
git remote add origin https://github.com/username/black-hole-animation.git
git branch -M main
git push -u origin main
```

This spec provides everything needed to recreate the black hole visualization from scratch, including all the implementation challenges and solutions discovered during development.