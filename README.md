# How Black Holes Work – Manim Animation

This project is an attempt at recreating the stunning black hole spacetime visualization from [this viral tweet](https://x.com/trq212/status/1947706205172068624) using [Manim Community Edition](https://docs.manim.community/).

## 🌌 Features
- **Professional black background** with bold, readable text
- **Blue wireframe spacetime grid** that dynamically warps around the black hole
- **Smaller blue wireframe black hole** positioned in a deeper spacetime well
- **Orange wireframe event horizon** with pulsing animation effects
- **Realistic orbital motion** using Kepler's laws with multiple white particles
- **Progressive animation sequence** that builds each physics concept step-by-step
- **Advanced labels** including "Accretion Disk" and "Gravitational Lens"

## 🛠 Requirements
- Python 3.8+
- [uv](https://github.com/astral-sh/uv)
- manim, numpy

## 🚀 Usage

```bash
# Install dependencies
uv pip install -r requirements.txt

# Render animation (low quality for preview)
uv run python -m manim -pql black_hole_scene.py HowBlackHolesWorkScene

# Render high quality (1080p)
uv run python -m manim -p --quality=1080p black_hole_scene.py HowBlackHolesWorkScene

# Use OpenGL renderer for better performance
uv run python -m manim -p --renderer=opengl black_hole_scene.py HowBlackHolesWorkScene
```

## 📦 Output
Find the rendered video in:
```
media/videos/black_hole_scene/1080p60/HowBlackHolesWorkScene.mp4  # High quality
media/videos/black_hole_scene/480p15/HowBlackHolesWorkScene.mp4   # Preview quality
```

## 🎬 Enhanced Scene Overview
1. **Intro**: "How Black Holes Work" title and blue wireframe spacetime grid appears
2. **Spacetime Curvature**: Grid dramatically warps with deeper curvature around smaller blue wireframe black hole
3. **Event Horizon**: Orange wireframe sphere appears behind text with pulsing animation
4. **Orbital Motion**: Multiple white particles demonstrate realistic orbital physics using Kepler's laws
5. **Advanced Features**: "Accretion Disk" and "Gravitational Lens" labels appear for complete visualization
6. **Outro**: Final wide camera shot with orbital particles fading

## 🎨 Visual Design
- **Black space background** for professional appearance
- **Bold, larger text** (28-48px) for better readability
- **Reduced grid density** (15x15) with thicker lines for clarity
- **Deeper spacetime warping** for dramatic effect
- **5 orbital particles** with realistic physics and slight wobble motion