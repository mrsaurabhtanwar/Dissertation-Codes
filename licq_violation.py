# licq_violation.py
# Academic illustration showing violation of LICQ (Linear Independence Constraint Qualification)
# Two active constraints with collinear gradients at the intersection point
# Requires: numpy, matplotlib
# Output: licq_violation.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

def g1(x, y):
    """First constraint: g1(x,y) <= 0 (curved boundary)"""
    return (x - 0.5)**2 + (y - 1.5)**2 - 1.0

def g2(x, y):
    """Second constraint: g2(x,y) <= 0 (another curved boundary, tangent to g1)"""
    return (x - 0.5)**2 + (y + 0.5)**2 - 1.0

def compute_grid(xmin=-1.0, xmax=2.0, ymin=-0.5, ymax=2.5, n=800):
    xs = np.linspace(xmin, xmax, n)
    ys = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(xs, ys)
    return X, Y, g1(X, Y), g2(X, Y)

def gradient_g1(x, y):
    """Gradient of g1"""
    return np.array([2*(x - 0.5), 2*(y - 1.5)])

def gradient_g2(x, y):
    """Gradient of g2"""
    return np.array([2*(x - 0.5), 2*(y + 0.5)])

def main():
    # The point where both constraints are active (intersection)
    # For these two circles centered at (0.5, 1.5) and (0.5, -0.5) with radius 1,
    # they intersect at x = 0.5, y = 0.5 (on the line x = 0.5)
    x_star = np.array([0.5, 0.5])
    
    # Compute gradients at x*
    grad_g1 = gradient_g1(x_star[0], x_star[1])
    grad_g2 = gradient_g2(x_star[0], x_star[1])
    
    # Normalize for display
    grad_g1_norm = grad_g1 / np.linalg.norm(grad_g1) * 0.6
    grad_g2_norm = grad_g2 / np.linalg.norm(grad_g2) * 0.5
    
    # Grid for plotting
    X, Y, G1, G2 = compute_grid()
    
    # Feasible region: g1 <= 0 AND g2 <= 0
    feasible = ((G1 <= 0) & (G2 <= 0)).astype(float)
    
    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(10, 11))
    ax.set_aspect('equal')
    ax.set_xlim(-0.8, 2.0)
    ax.set_ylim(-0.5, 2.8)
    
    # Subtle grid
    ax.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#666666')
    
    # Color scheme: muted blue/gray academic style
    feasible_color = '#e8eef5'  # Very light blue-gray for feasible region
    
    # Shade the feasible region
    ax.contourf(X, Y, feasible, levels=[0.5, 1.5], colors=[feasible_color], alpha=0.8)
    
    # Draw constraint boundaries with clean thin strokes
    ax.contour(X, Y, G1, levels=[0], colors=['#2c3e50'], linewidths=2.0, linestyles='-')
    ax.contour(X, Y, G2, levels=[0], colors=['#2c3e50'], linewidths=2.0, linestyles='-')
    
    # Mark the critical point x*
    ax.plot(x_star[0], x_star[1], 'o', color='#1a1a2e', markersize=10, zorder=10)
    ax.annotate(r'$\mathbf{x}^*$', xy=(x_star[0], x_star[1]), 
                xytext=(x_star[0] + 0.15, x_star[1] + 0.08),
                fontsize=14, fontweight='bold', color='#1a1a2e')
    
    # Draw gradient vectors - COLLINEAR (both point in same direction along y-axis)
    # At x* = (0.5, 0.5):
    # ∇g1 = (0, -2) pointing down (towards center of circle 1)
    # ∇g2 = (0, 2) pointing up (towards center of circle 2)
    # These are collinear (on the same line) - LICQ violation!
    
    arrow_style = dict(arrowstyle='-|>', mutation_scale=18, lw=2.5)
    
    # Gradient 1 (pointing towards center of circle 1, i.e., upward from x*)
    arrow1 = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_g1_norm[0], x_star[1] + grad_g1_norm[1]),
        color='#c0392b',  # Muted red
        **arrow_style,
        zorder=8
    )
    ax.add_patch(arrow1)
    
    # Gradient 2 (pointing towards center of circle 2, i.e., downward from x*)
    arrow2 = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_g2_norm[0], x_star[1] + grad_g2_norm[1]),
        color='#2980b9',  # Muted blue
        **arrow_style,
        zorder=8
    )
    ax.add_patch(arrow2)
    
    # Labels for gradients
    ax.text(x_star[0] + 0.12, x_star[1] - 0.72, r'$\nabla g_1(\mathbf{x}^*)$',
            fontsize=13, color='#c0392b', fontweight='bold', ha='center')
    ax.text(x_star[0] + 0.12, x_star[1] + 0.72, r'$\nabla g_2(\mathbf{x}^*)$',
            fontsize=13, color='#2980b9', fontweight='bold', ha='center')
    
    # Constraint labels on the curves
    ax.text(1.4, 1.9, r'$g_1(\mathbf{x}) = 0$', fontsize=12, color='#2c3e50',
            fontweight='bold', rotation=-45,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.9))
    ax.text(1.4, 0.1, r'$g_2(\mathbf{x}) = 0$', fontsize=12, color='#2c3e50',
            fontweight='bold', rotation=45,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.9))
    
    # Label for feasible region
    ax.text(0.5, 1.0, 'Feasible\nRegion', fontsize=11, ha='center', va='center',
            color='#34495e', fontstyle='italic', alpha=0.8)
    
    # Annotation box explaining LICQ violation - moved to avoid overlap
    explanation_text = (
        r"$\mathbf{LICQ\ Violation}$" + "\n\n"
        r"At $\mathbf{x}^*$, the gradients" + "\n"
        r"$\nabla g_1(\mathbf{x}^*)$ and $\nabla g_2(\mathbf{x}^*)$" + "\n"
        r"are collinear (linearly dependent)." + "\n\n"
        r"$\Rightarrow$ Lagrange multipliers" + "\n"
        r"may not be unique."
    )
    ax.text(1.15, 2.6, explanation_text, fontsize=10, ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.6', fc='#f8f9fa', ec='#2c3e50',
                     linewidth=1.5, alpha=0.95),
            linespacing=1.4)
    
    # Draw a thin dashed line showing collinearity
    line_extent = 0.85
    ax.plot([x_star[0], x_star[0]], 
            [x_star[1] - line_extent, x_star[1] + line_extent],
            '--', color='#7f8c8d', linewidth=1.5, alpha=0.7, zorder=3)
    
    # Axis labels
    ax.set_xlabel(r'$x_1$', fontsize=14, fontweight='bold')
    ax.set_ylabel(r'$x_2$', fontsize=14, fontweight='bold')
    ax.tick_params(labelsize=11)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    plt.tight_layout()
    outname = "licq_violation.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
