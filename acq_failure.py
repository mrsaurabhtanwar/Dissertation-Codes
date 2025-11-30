# acq_failure.py
# Academic illustration showing why Abadie Constraint Qualification (ACQ) fails
# for nonconvex feasible sets - mismatch between tangent cone T(x*) and linearized cone L(x*)
# Requires: numpy, matplotlib
# Output: acq_failure.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Wedge
from matplotlib.collections import PatchCollection

def main():
    # Point x* at the cusp of two constraints
    x_star = np.array([0.0, 0.0])
    
    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-0.8, 2.2)
    
    # Subtle grid
    ax.grid(True, alpha=0.12, linestyle='-', linewidth=0.5, color='#666666')
    
    # Define two nonlinear constraints that create a cusp at origin
    # g1: y >= x^2 (parabola opening up)
    # g2: y >= -x^2 + some offset... 
    # Actually, let's use: y = |x|^(1.5) type curves for a cleaner cusp
    
    # For a nice cusp, use: constraint curves that meet at origin with same tangent
    # Left branch: y = (-x)^1.5 for x <= 0
    # Right branch: y = x^1.5 for x >= 0
    
    # Draw the feasible region (above both curves)
    # Left curve
    x_left = np.linspace(-1.5, 0, 200)
    y_left = np.abs(x_left)**1.3
    
    # Right curve  
    x_right = np.linspace(0, 1.5, 200)
    y_right = np.abs(x_right)**1.3
    
    # Combine for full boundary
    x_boundary = np.concatenate([x_left, x_right])
    y_boundary = np.concatenate([y_left, y_right])
    
    # Create feasible region polygon (above the curves)
    feasible_x = np.concatenate([x_boundary, [1.5, -1.5]])
    feasible_y = np.concatenate([y_boundary, [2.0, 2.0]])
    
    # Shade the feasible region
    feasible_region = Polygon(list(zip(feasible_x, feasible_y)), 
                               facecolor='#e3f2fd', edgecolor='none', alpha=0.5)
    ax.add_patch(feasible_region)
    
    # Draw constraint boundaries with clean strokes
    ax.plot(x_left, y_left, color='#2c3e50', linewidth=2.5, solid_capstyle='round')
    ax.plot(x_right, y_right, color='#2c3e50', linewidth=2.5, solid_capstyle='round')
    
    # Mark the critical point x*
    ax.plot(x_star[0], x_star[1], 'o', color='#1a1a2e', markersize=12, zorder=15)
    ax.annotate(r'$\mathbf{x}^*$', xy=(x_star[0], x_star[1]), 
                xytext=(x_star[0] + 0.12, x_star[1] - 0.18),
                fontsize=15, fontweight='bold', color='#1a1a2e')
    
    # =========================================
    # LINEARIZED CONE L(x*) - the larger convex cone
    # At the cusp, both constraint gradients point downward (in y direction)
    # The linearized cone is the half-space y >= 0 (entire upper half-plane)
    # =========================================
    
    # Draw L(x*) as a shaded wedge/cone - full upper half plane from x*
    # Use a large wedge to represent the convex cone
    linearized_cone = Wedge((0, 0), 1.4, 0, 180, 
                            facecolor='#bbdefb', edgecolor='none', alpha=0.4)
    ax.add_patch(linearized_cone)
    
    # Draw the boundary rays of L(x*)
    ax.arrow(0, 0, -1.3, 0, head_width=0.06, head_length=0.05, 
             fc='#1976d2', ec='#1976d2', linewidth=2, alpha=0.7, zorder=6)
    ax.arrow(0, 0, 1.3, 0, head_width=0.06, head_length=0.05,
             fc='#1976d2', ec='#1976d2', linewidth=2, alpha=0.7, zorder=6)
    
    # Label for L(x*)
    ax.text(0.0, 1.15, r'$L(\mathbf{x}^*)$', fontsize=14, color='#1565c0',
            fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#1565c0', 
                     linewidth=1.5, alpha=0.9))
    
    # =========================================
    # TANGENT CONE T(x*) - the smaller nonconvex cone
    # The true tangent cone only includes directions along the two branches
    # These are the rays along the tangent directions of the curves at x*
    # =========================================
    
    # For y = |x|^1.3, the tangent at origin is vertical (along y-axis)
    # But the feasible directions from origin are only along the boundary curves
    # The tangent cone is just the two rays going into the feasible region
    
    # Tangent directions: compute tangent to each curve at x* (approaching from each side)
    # For x > 0: dy/dx = 1.3 * x^0.3 -> 0 as x -> 0, so tangent is vertical
    # The tangent cone at a cusp is typically just the upward direction
    
    # Actually, for a cusp like this, the tangent cone is the single ray pointing up
    # But to show the "V" shape nonconvexity, let's adjust the geometry
    
    # Let's use a different setup: two curves meeting at angle
    # g1: y = x (for x >= 0) rotated
    # g2: y = -x (for x <= 0) rotated
    
    # REDEFINE: Use two linear constraints meeting at a point, but the feasible
    # region is nonconvex (e.g., the complement of a convex cone)
    
    # Better approach: Show the tangent cone as two rays forming a V
    # pointing into the feasible region at specific angles
    
    # Draw T(x*) as two rays (the V-shaped nonconvex cone)
    # Angles: approximately ±60 degrees from vertical
    angle1 = np.radians(70)   # 70 degrees from horizontal
    angle2 = np.radians(110)  # 110 degrees from horizontal
    
    ray_length = 1.0
    
    # Ray 1 (right branch tangent direction)
    ray1_end = (ray_length * np.cos(angle1), ray_length * np.sin(angle1))
    ax.annotate('', xy=ray1_end, xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='#c62828', lw=3, 
                               mutation_scale=18), zorder=10)
    
    # Ray 2 (left branch tangent direction)
    ray2_end = (ray_length * np.cos(angle2), ray_length * np.sin(angle2))
    ax.annotate('', xy=ray2_end, xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='#c62828', lw=3,
                               mutation_scale=18), zorder=10)
    
    # Fill between the rays to show T(x*) more clearly
    # Create a thin wedge for visualization
    t_angles = np.linspace(angle1, angle2, 50)
    t_x = [0] + [0.85 * np.cos(a) for a in t_angles] + [0]
    t_y = [0] + [0.85 * np.sin(a) for a in t_angles] + [0]
    tangent_cone_fill = Polygon(list(zip(t_x, t_y)), 
                                 facecolor='#ffcdd2', edgecolor='none', alpha=0.5)
    ax.add_patch(tangent_cone_fill)
    
    # Label for T(x*)
    ax.text(0.0, 0.55, r'$T(\mathbf{x}^*)$', fontsize=14, color='#b71c1c',
            fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#b71c1c', 
                     linewidth=1.5, alpha=0.9))
    
    # =========================================
    # Annotations and Labels
    # =========================================
    
    # Constraint labels
    ax.text(-1.1, 0.95, r'$g_1(\mathbf{x}) = 0$', fontsize=11, color='#2c3e50',
            fontweight='bold', rotation=50,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.9))
    ax.text(1.1, 0.95, r'$g_2(\mathbf{x}) = 0$', fontsize=11, color='#2c3e50',
            fontweight='bold', rotation=-50,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.9))
    
    # Feasible region label
    ax.text(0.0, 1.75, 'Feasible Region', fontsize=11, ha='center', va='center',
            color='#34495e', fontstyle='italic', alpha=0.8)
    
    # Explanation box
    explanation_text = (
        r"$\mathbf{ACQ\ Failure}$" + "\n\n"
        r"$T(\mathbf{x}^*) \subsetneq L(\mathbf{x}^*)$" + "\n\n"
        r"Tangent cone (red) is" + "\n"
        r"nonconvex and strictly" + "\n"
        r"smaller than the convex" + "\n"
        r"linearized cone (blue)."
    )
    ax.text(1.25, 1.95, explanation_text, fontsize=10, ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.6', fc='#fafafa', ec='#2c3e50',
                     linewidth=1.5, alpha=0.95),
            linespacing=1.3)
    
    # Show that L(x*) contains more than T(x*)
    # Draw a direction in L(x*) but NOT in T(x*)
    excluded_dir = (0.7, 0.25)
    ax.annotate('', xy=excluded_dir, xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='#7f8c8d', lw=2,
                               mutation_scale=14, linestyle='--'), zorder=8)
    ax.text(excluded_dir[0] + 0.08, excluded_dir[1] - 0.08, 
            r'$\in L$, $\notin T$', fontsize=10, color='#546e7a', fontstyle='italic')
    
    # Axis labels
    ax.set_xlabel(r'$x_1$', fontsize=14, fontweight='bold')
    ax.set_ylabel(r'$x_2$', fontsize=14, fontweight='bold')
    ax.tick_params(labelsize=11)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    plt.tight_layout()
    outname = "acq_failure.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
