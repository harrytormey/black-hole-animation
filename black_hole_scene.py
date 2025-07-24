from manim import *
import numpy as np


class HowBlackHolesWorkScene(ThreeDScene):
    def construct(self):
        # Set black background
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES)
        
        # Scene sequence with proper animation flow
        self.intro_grid()
        self.add_black_hole()
        self.show_event_horizon()
        self.demonstrate_orbital_motion()
        self.outro()
    
    def intro_grid(self):
        # Main title appears first
        self.main_title = Text("How Black Holes Work", color=WHITE, font_size=42)
        self.main_title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.main_title)
        
        # Blue 3D spacetime grid - larger and more detailed
        self.spacetime_grid = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-8, 8],
            v_range=[-8, 8],
            resolution=(25, 25),
            fill_opacity=0.0,  # No fill, just wireframe
            stroke_color=BLUE,
            stroke_width=1.5
        )
        
        # Spacetime label
        self.spacetime_label = Text("Spacetime", color=BLUE, font_size=32)
        self.spacetime_label.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.spacetime_label)
        
        # Animate title, grid and label appearing
        self.play(Write(self.main_title), run_time=2)
        self.play(Create(self.spacetime_grid), run_time=3)
        self.play(Write(self.spacetime_label), run_time=1)
        self.wait(1)
    
    def add_black_hole(self):
        # Create warped spacetime grid
        def warped_surface(u, v):
            r_squared = u**2 + v**2
            # More dramatic warping effect
            warp_factor = 4 / (1 + r_squared/3)
            z = -warp_factor * np.exp(-r_squared/6)
            return np.array([u, v, z])
        
        self.warped_grid = Surface(
            warped_surface,
            u_range=[-8, 8],
            v_range=[-8, 8],
            resolution=(35, 35),
            fill_opacity=0.0,  # Wireframe only
            stroke_color=BLUE,
            stroke_width=1.5
        )
        
        # Black hole as blue wireframe sphere (like in screenshots)
        self.black_hole = Sphere(radius=0.8, resolution=(15, 15))
        self.black_hole.set_fill(opacity=0)  # Transparent fill
        self.black_hole.set_stroke(BLUE, width=2)
        self.black_hole.move_to([0, 0, -1.2])
        
        # Spacetime curvature label
        self.curvature_label = Text("Spacetime Curvature", color=YELLOW, font_size=28)
        self.curvature_label.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.curvature_label)
        
        # Black hole label
        self.black_hole_label = Text("Black Hole", color=WHITE, font_size=28)
        self.black_hole_label.next_to([0, 0, -2], DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(self.black_hole_label)
        
        # Animate spacetime warping
        self.play(
            Transform(self.spacetime_grid, self.warped_grid),
            run_time=3
        )
        self.play(Write(self.curvature_label), run_time=1)
        
        # Black hole appears
        self.play(FadeIn(self.black_hole), run_time=2)
        self.play(Write(self.black_hole_label), run_time=1)
        self.wait(2)
    
    def show_event_horizon(self):
        # Event horizon as orange wireframe sphere (like in screenshots)
        self.event_horizon = Sphere(radius=1.4, resolution=(18, 18))
        self.event_horizon.set_stroke(ORANGE, width=2.5)
        self.event_horizon.set_fill(opacity=0)  # Completely transparent
        self.event_horizon.move_to([0, 0, -0.8])
        
        # Event horizon label
        self.horizon_label = Text("Event Horizon", color=ORANGE, font_size=26)
        self.horizon_label.move_to([-3, 0.5, 0])
        self.add_fixed_in_frame_mobjects(self.horizon_label)
        
        # Animate event horizon appearance with pulsing effect
        self.play(
            Create(self.event_horizon),
            Write(self.horizon_label),
            run_time=2
        )
        
        # Pulsing effect
        self.play(
            self.event_horizon.animate.scale(1.1),
            rate_func=rate_functions.there_and_back,
            run_time=1
        )
        self.wait(1)
    
    def demonstrate_orbital_motion(self):
        # Orbital motion label
        self.orbital_label = Text("Orbital Motion", color=ORANGE, font_size=28)
        self.orbital_label.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.orbital_label)
        
        # Create multiple white orbital particles (like in screenshots)
        self.orbiters = []
        orbit_radii = [2.8, 3.5, 4.2, 5.0]
        
        for i, radius in enumerate(orbit_radii):
            # White dots for orbital particles
            orbiter = Dot(radius=0.08, color=WHITE)
            orbiter.set_fill(WHITE, opacity=1)
            # Position at different angles and heights
            angle = i * PI/2
            z_offset = 0.1 * (i - 1.5)
            orbiter.move_to([radius * np.cos(angle), radius * np.sin(angle), z_offset])
            self.orbiters.append(orbiter)
        
        # Show orbital motion label
        self.play(Write(self.orbital_label), run_time=1)
        
        # Add orbiters with staggered appearance
        for orbiter in self.orbiters:
            self.play(FadeIn(orbiter), run_time=0.3)
        
        # Animate orbital motion with different speeds
        def create_orbit_updater(radius, speed):
            def orbit_updater(mob, dt):
                # Orbital motion around the black hole
                current_pos = mob.get_center()
                angle = np.arctan2(current_pos[1], current_pos[0])
                angle += dt * speed
                z = current_pos[2]
                mob.move_to([radius * np.cos(angle), radius * np.sin(angle), z])
            return orbit_updater
        
        # Apply different orbital speeds (closer = faster)
        speeds = [1.2, 0.9, 0.7, 0.5]
        for orbiter, radius, speed in zip(self.orbiters, orbit_radii, speeds):
            orbiter.add_updater(create_orbit_updater(radius, speed))
        
        # Camera movement for better view
        self.move_camera(theta=-10 * DEGREES, run_time=2)
        
        # Let orbits run to show the motion
        self.wait(4)
        
        # Remove updaters
        for orbiter in self.orbiters:
            orbiter.clear_updaters()
    
    def outro(self):
        # Add final advanced labels (like in screenshot 4)
        self.accretion_label = Text("Accretion Disk", color=YELLOW, font_size=24)
        self.accretion_label.to_edge(LEFT, buff=0.5).to_edge(DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(self.accretion_label)
        
        self.lens_label = Text("Gravitational Lens", color=WHITE, font_size=24)
        self.lens_label.to_edge(RIGHT, buff=0.5).to_edge(UP, buff=2.5)
        self.add_fixed_in_frame_mobjects(self.lens_label)
        
        # Show advanced labels with animation
        self.play(Write(self.accretion_label), run_time=1.5)
        self.wait(0.5)
        self.play(Write(self.lens_label), run_time=1.5)
        
        # Reset camera for final wide shot
        self.move_camera(phi=70 * DEGREES, theta=-20 * DEGREES, run_time=2)
        
        # Keep everything visible for final shot
        self.wait(3)
        
        # Final fade with all elements still orbiting
        self.play(
            *[FadeOut(orbiter, shift=DOWN*0.5) for orbiter in self.orbiters],
            run_time=2
        )
        self.wait(2)