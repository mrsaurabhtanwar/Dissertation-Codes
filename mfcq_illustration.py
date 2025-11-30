# mfcq_illustration.py
# Academic illustration of Mangasarian-Fromovitz Constraint Qualification (MFCQ)
# Shows equality constraint h(x)=0, active inequality g(x)=0, and feasible direction d
# Requires: numpy, matplotlib
# Output: mfcq_illustration.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def h(x, y):
    """Equality constraint: h(x,y) = 0 (a curved line)"""
    return y - (0.3 * x**2 + 0.5)

def g(x, y):
    """Inequality constraint: g(x,y) <= 0 (region below a tilted line)"""
    return y - (-0.5 * x + 1.2)

def compute_grid(xmin=-1.0, xmax=2.5, ymin=-0.5, ymax=2.5, n=800):
    xs = np.linspace(xmin, xmax, n)
    ys = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(xs, ys)
    return X, Y, h(X, Y), g(X, Y)

def gradient_h(x, y):
    """Gradient of h: ∇h = (∂h/∂x, ∂h/∂y) = (0.6x, 1)"""
    return np.array([0.6 * x, 1.0])

def gradient_g(x, y):
    """Gradient of g: ∇g = (∂g/∂x, ∂g/∂y) = (-0.5, 1)"""
    return np.array([-0.5, 1.0])

def main():
    # Find intersection point x* where h(x,y)=0 and g(x,y)=0 meet
    # h: y = 0.3x² + 0.5
    # g: y = -0.5x + 1.2
    # Solving: 0.3x² + 0.5 = -0.5x + 1.2
    # 0.3x² + 0.5x - 0.7 = 0
    # x = (-0.5 ± sqrt(0.25 + 0.84)) / 0.6 = (-0.5 ± 1.044) / 0.6
    # x ≈ 0.907 (positive root)
    x_star_x = 0.907
    x_star_y = 0.3 * x_star_x**2 + 0.5  # ≈ 0.747
    x_star = np.array([x_star_x, x_star_y])
    
    # Compute gradients at x*
    grad_h = gradient_h(x_star[0], x_star[1])
    grad_g = gradient_g(x_star[0], x_star[1])
    
    # Normalize gradients for display
    grad_h_norm = grad_h / np.linalg.norm(grad_h) * 0.55
    grad_g_norm = grad_g / np.linalg.norm(grad_g) * 0.55
    
    # Find feasible direction d:
    # Must satisfy: ∇h(x*)ᵀd = 0 (tangent to equality constraint)
    #               ∇g(x*)ᵀd < 0 (strictly decreasing inequality)
    # d perpendicular to ∇h: if ∇h = (a, b), then d = (-b, a) or (b, -a)
    # Choose the one where ∇g·d < 0
    d_candidate1 = np.array([-grad_h[1], grad_h[0]])  # perpendicular to ∇h
    d_candidate2 = np.array([grad_h[1], -grad_h[0]])  # opposite perpendicular
    
    # Check which satisfies ∇g·d < 0
    if np.dot(grad_g, d_candidate1) < 0:
        d = d_candidate1
    else:
        d = d_candidate2
    
    d_norm = d / np.linalg.norm(d) * 0.6  # Normalize for display
    
    # Grid for plotting
    X, Y, H, G = compute_grid()
    
    # Feasible region: h(x,y) = 0 (on the curve) AND g(x,y) <= 0
    # For visualization, we shade g <= 0 region
    feasible_ineq = (G <= 0).astype(float)
    
    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(-0.2, 2.3)
    
    # Subtle grid
    ax.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#666666')
    
    # Color scheme: muted blue/gray academic style
    feasible_color = '#e8eef5'
    
    # Shade the inequality feasible region (g <= 0)
    ax.contourf(X, Y, feasible_ineq, levels=[0.5, 1.5], colors=[feasible_color], alpha=0.6)
    
    # Draw constraint boundaries
    # Equality constraint h(x,y) = 0 - solid dark line
    ax.contour(X, Y, H, levels=[0], colors=['#1a365d'], linewidths=2.5, linestyles='-')
    
    # Inequality constraint g(x,y) = 0 - solid line (boundary of feasible region)
    ax.contour(X, Y, G, levels=[0], colors=['#2c3e50'], linewidths=2.0, linestyles='-')
    
    # Highlight the feasible part of h=0 (where g <= 0)
    # This is the actual feasible set for this problem
    x_curve = np.linspace(-0.3, x_star_x + 0.05, 200)
    y_curve = 0.3 * x_curve**2 + 0.5
    # Keep only points where g <= 0
    mask = (y_curve <= -0.5 * x_curve + 1.2)
    ax.plot(x_curve[mask], y_curve[mask], color='#0d47a1', linewidth=4, 
            zorder=5, solid_capstyle='round', label='Feasible set')
    
    # Mark the critical point x*
    ax.plot(x_star[0], x_star[1], 'o', color='#1a1a2e', markersize=12, zorder=15)
    ax.annotate(r'$\mathbf{x}^*$', xy=(x_star[0], x_star[1]), 
                xytext=(x_star[0] + 0.12, x_star[1] - 0.12),
                fontsize=15, fontweight='bold', color='#1a1a2e')
    
    # Arrow style for vectors
    arrow_style = dict(arrowstyle='-|>', mutation_scale=20, lw=2.5)
    
    # Draw ∇h(x*) - gradient of equality constraint (perpendicular to curve)
    arrow_h = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_h_norm[0], x_star[1] + grad_h_norm[1]),
        color='#6a1b9a',  # Purple
        **arrow_style,
        zorder=12
    )
    ax.add_patch(arrow_h)
    ax.text(x_star[0] + grad_h_norm[0] + 0.08, x_star[1] + grad_h_norm[1] + 0.08,
            r'$\nabla h(\mathbf{x}^*)$', fontsize=13, color='#6a1b9a', fontweight='bold')
    
    # Draw ∇g(x*) - gradient of inequality constraint (pointing outward)
    arrow_g = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_g_norm[0], x_star[1] + grad_g_norm[1]),
        color='#c0392b',  # Red
        **arrow_style,
        zorder=12
    )
    ax.add_patch(arrow_g)
    ax.text(x_star[0] + grad_g_norm[0] - 0.25, x_star[1] + grad_g_norm[1] + 0.1,
            r'$\nabla g(\mathbf{x}^*)$', fontsize=13, color='#c0392b', fontweight='bold')
    
    # Draw feasible direction d
    arrow_d = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + d_norm[0], x_star[1] + d_norm[1]),
        color='#2e7d32',  # Green
        **arrow_style,
        zorder=12
    )
    ax.add_patch(arrow_d)
    ax.text(x_star[0] + d_norm[0] + 0.05, x_star[1] + d_norm[1] - 0.12,
            r'$\mathbf{d}$', fontsize=15, color='#2e7d32', fontweight='bold')
    
    # Labels for constraints on the curves
    ax.text(1.8, 1.55, r'$h(\mathbf{x}) = 0$', fontsize=12, color='#1a365d',
            fontweight='bold', rotation=35,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.9))
    ax.text(1.9, 0.35, r'$g(\mathbf{x}) = 0$', fontsize=12, color='#2c3e50',
            fontweight='bold', rotation=-25,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.9))
    
    # Label for feasible region
    ax.text(0.3, 0.3, r'$g(\mathbf{x}) \leq 0$', fontsize=11, ha='center', va='center',
            color='#34495e', fontstyle='italic', alpha=0.8)
    
    # MFCQ explanation box
    explanation_text = (
        r"$\mathbf{MFCQ\ Conditions}$" + "\n\n"
        r"$\nabla h(\mathbf{x}^*)^\top \mathbf{d} = 0$" + "\n"
        r"(tangent to equality)" + "\n\n"
        r"$\nabla g(\mathbf{x}^*)^\top \mathbf{d} < 0$" + "\n"
        r"(into feasible region)"
    )
    ax.text(1.45, 2.15, explanation_text, fontsize=10, ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.6', fc='#f8f9fa', ec='#2c3e50',
                     linewidth=1.5, alpha=0.95),
            linespacing=1.3)
    
    # Show the tangent line at x* (for h=0) to illustrate ∇h⊥d
    tangent_dir = np.array([-grad_h[1], grad_h[0]])
    tangent_dir = tangent_dir / np.linalg.norm(tangent_dir)
    t_extent = 0.4
    ax.plot([x_star[0] - tangent_dir[0]*t_extent, x_star[0] + tangent_dir[0]*t_extent],
            [x_star[1] - tangent_dir[1]*t_extent, x_star[1] + tangent_dir[1]*t_extent],
            '--', color='#7f8c8d', linewidth=1.2, alpha=0.6, zorder=3)
    
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
    outname = "mfcq_illustration.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
