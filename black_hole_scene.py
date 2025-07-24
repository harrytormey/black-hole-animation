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
        
        # Spacetime label
        self.spacetime_label = Text("Spacetime", color=BLUE, font_size=36)
        self.spacetime_label.to_corner(UL)
        self.add_fixed_in_frame_mobjects(self.spacetime_label)
        
        # Animate grid appearing
        self.play(Create(self.spacetime_grid), run_time=2)
        self.play(Write(self.spacetime_label))
        self.wait(1)
    
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
            resolution=(30, 30),
            fill_opacity=0.3,
            stroke_color=BLUE,
            stroke_width=1
        )
        
        # Black hole sphere
        self.black_hole = Sphere(radius=0.7, resolution=(20, 20))
        self.black_hole.set_fill(BLACK, opacity=1)
        self.black_hole.set_stroke(WHITE, width=0.5)
        self.black_hole.move_to([0, 0, -0.5])
        
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
    
    def show_event_horizon(self):
        # Event horizon as orange wireframe sphere
        self.event_horizon = Sphere(radius=1.2, resolution=(15, 15))
        self.event_horizon.set_stroke(ORANGE, width=2)
        self.event_horizon.set_fill(ORANGE, opacity=0.1)
        self.event_horizon.move_to([0, 0, -0.3])
        
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
        self.orbiter_2.move_to([orbit_radius_2, 0, 0.2])
        
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
        
        # Animate orbital motion
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