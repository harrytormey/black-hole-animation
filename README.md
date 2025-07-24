# How Black Holes Work – Manim Animation

This project visualizes how black holes warp spacetime and cause orbital motion using [Manim Community Edition](https://docs.manim.community/).

## 🖼️ Features
- Spacetime curvature grid
- Black hole with event horizon
- Orbiting bodies
- Smooth camera transitions

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
media/videos/black_hole_scene/480p15/HowBlackHolesWorkScene.mp4
```

## 🎬 Scene Overview
1. **Intro**: Blue 3D spacetime grid appears
2. **Spacetime Curvature**: Grid warps around central black hole
3. **Event Horizon**: Orange wireframe sphere with pulsing effect
4. **Orbital Motion**: Gray bodies orbit around the black hole
5. **Outro**: Grid resets to flat with final title