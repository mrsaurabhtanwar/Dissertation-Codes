# mpec_mfcq.py
# Academic illustration of MPEC-MFCQ geometry
# Shows feasible direction d satisfying complementarity-aware MFCQ conditions
# Requires: numpy, matplotlib
# Output: mpec_mfcq.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D

def main():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-0.8, 3.5)
    ax.set_ylim(-1.0, 3.2)
    ax.axis('off')
    
    # Color scheme
    color_G = '#c62828'          # Red for G constraints
    color_H = '#1565c0'          # Blue for H constraints
    color_d = '#2e7d32'          # Green for feasible direction
    color_region = '#e3f2fd'     # Light blue for feasible region
    color_boundary = '#37474f'   # Dark gray for boundaries
    
    # =========================================
    # Define the geometry - repositioned for clarity
    # =========================================
    # Point x* at intersection of G=0 and H=0
    x_star = np.array([1.5, 1.2])
    
    # G(x) = 0 curve: a line with slope -0.5 passing through x*
    # G(x) = y - (-0.5*x + 1.6) = y + 0.5x - 1.6
    # ∇G = (0.5, 1) normalized
    
    # H(x) = 0 curve: a line with slope 1.2 passing through x*
    # H(x) = y - (1.2*x - 0.44) = y - 1.2x + 0.44
    # ∇H = (-1.2, 1) normalized
    
    # Draw feasible region (where G >= 0 and H >= 0, with complementarity)
    # The feasible region is the "corner" formed by the two constraint boundaries
    
    # Create shaded feasible region
    feasible_vertices = [
        (-0.3, 2.0),      # Upper left
        x_star,           # The corner point
        (3.2, 1.2 - 0.4*(3.2 - 1.5)),  # Along G=0 to right
        (3.5, 3.2),       # Upper right corner
        (-0.8, 3.2),      # Top left
    ]
    feasible_poly = Polygon(feasible_vertices, facecolor=color_region, 
                            edgecolor='none', alpha=0.4, zorder=1)
    ax.add_patch(feasible_poly)
    
    # Draw G(x) = 0 boundary - flatter angle
    g_x = np.array([-0.3, 3.3])
    g_y = 1.2 - 0.4 * (g_x - 1.5)  # Slope -0.4 through x_star
    ax.plot(g_x, g_y, color=color_G, linewidth=2.5, solid_capstyle='round', 
            zorder=3, label=r'$G(x) = 0$')
    
    # Draw H(x) = 0 boundary - steeper angle  
    h_x = np.array([0.5, 2.5])
    h_y = 1.2 + 1.5 * (h_x - 1.5)  # Slope 1.5 through x_star
    ax.plot(h_x, h_y, color=color_H, linewidth=2.5, solid_capstyle='round',
            zorder=3, label=r'$H(x) = 0$')
    
    # Mark x*
    ax.plot(x_star[0], x_star[1], 'ko', markersize=12, zorder=15)
    ax.text(x_star[0] + 0.12, x_star[1] - 0.15, r'$\mathbf{x}^*$',
            fontsize=15, fontweight='bold', color='#1a1a2e')
    
    # =========================================
    # Gradient vectors - repositioned for clarity
    # =========================================
    arrow_style = dict(arrowstyle='-|>', mutation_scale=18, lw=2.5)
    
    # ∇G(x*) - perpendicular to G=0, pointing into G>0 region (upward-left)
    grad_G = np.array([-0.4, 1.0])  # Perpendicular to slope -0.4
    grad_G_norm = grad_G / np.linalg.norm(grad_G) * 0.7
    
    arrow_G = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_G_norm[0], x_star[1] + grad_G_norm[1]),
        color=color_G, **arrow_style, zorder=10
    )
    ax.add_patch(arrow_G)
    ax.text(x_star[0] + grad_G_norm[0] - 0.1, x_star[1] + grad_G_norm[1] + 0.15,
            r'$\nabla G_i(\mathbf{x}^*)$', fontsize=12, color=color_G, fontweight='bold')
    
    # ∇H(x*) - perpendicular to H=0, pointing into H>0 region (right-upward)
    grad_H = np.array([1.5, 1.0])  # Perpendicular to slope 1.5
    grad_H_norm = grad_H / np.linalg.norm(grad_H) * 0.7
    
    arrow_H = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + grad_H_norm[0], x_star[1] + grad_H_norm[1]),
        color=color_H, **arrow_style, zorder=10
    )
    ax.add_patch(arrow_H)
    ax.text(x_star[0] + grad_H_norm[0] + 0.1, x_star[1] + grad_H_norm[1] + 0.1,
            r'$\nabla H_i(\mathbf{x}^*)$', fontsize=12, color=color_H, fontweight='bold')
    
    # =========================================
    # Feasible direction d
    # =========================================
    # For MPEC-MFCQ, d must satisfy:
    # - ∇G_i(x*)ᵀd = 0 for i ∈ I_0+ (tangent to active G)
    # - ∇H_i(x*)ᵀd = 0 for i ∈ I_+0 (tangent to active H)
    # - For I_00 (biactive): more complex conditions
    
    # In this illustration, assume we're at a point where G=0 (active) and H=0 (active)
    # This is I_00 case - d must satisfy ∇Gᵀd ≤ 0 OR ∇Hᵀd ≤ 0 (complementarity)
    
    # Find a direction tangent to G=0 that also goes into H>0
    # Tangent to G: perpendicular to ∇G = (0.5, 1) → tangent = (-1, 0.5) or (1, -0.5)
    d_tangent_G = np.array([1.0, -0.5])
    d_tangent_G = d_tangent_G / np.linalg.norm(d_tangent_G)
    
    # Check: ∇Hᵀd should be < 0 (going into feasible for H, or staying on boundary)
    # ∇H = (-1.2, 1), d = (1, -0.5) normalized
    # ∇Hᵀd = -1.2*1 + 1*(-0.5) = -1.7 < 0 ✓
    
    d = d_tangent_G * 0.7
    
    arrow_d = FancyArrowPatch(
        (x_star[0], x_star[1]),
        (x_star[0] + d[0], x_star[1] + d[1]),
        color=color_d, arrowstyle='-|>', mutation_scale=20, lw=3.5, zorder=12
    )
    ax.add_patch(arrow_d)
    ax.text(x_star[0] + d[0] + 0.1, x_star[1] + d[1] - 0.12,
            r'$\mathbf{d}$', fontsize=16, color=color_d, fontweight='bold')
    
    # =========================================
    # Show tangent line to G=0 at x*
    # =========================================
    tangent_len = 0.5
    tangent_dir = np.array([-1, 0.5]) / np.linalg.norm(np.array([-1, 0.5]))
    ax.plot([x_star[0] - tangent_dir[0]*tangent_len, x_star[0] + tangent_dir[0]*tangent_len],
            [x_star[1] - tangent_dir[1]*tangent_len, x_star[1] + tangent_dir[1]*tangent_len],
            '--', color='#9e9e9e', linewidth=1.5, alpha=0.6, zorder=2)
    
    # =========================================
    # Labels for constraint boundaries
    # =========================================
    ax.text(2.6, 0.65, r'$G(\mathbf{x}) = 0$', fontsize=11, color=color_G,
            fontweight='bold', rotation=-22,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9))
    ax.text(2.0, 2.05, r'$H(\mathbf{x}) = 0$', fontsize=12, color=color_H,
            fontweight='bold', rotation=50,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.9))
    
    # Feasible region label
    ax.text(0.4, 2.2, 'Feasible\nRegion', fontsize=11, ha='center',
            color='#455a64', fontstyle='italic', alpha=0.8)
    
    # =========================================
    # MPEC-MFCQ Conditions Box - positioned above the red line
    # =========================================
    conditions_box = FancyBboxPatch((2.5, 1.6), 0.85, 0.65,
                                     boxstyle="round,pad=0.03,rounding_size=0.08",
                                     facecolor='#fafafa', edgecolor='#37474f',
                                     linewidth=1.2, alpha=0.95, zorder=20)
    ax.add_patch(conditions_box)
    
    ax.text(2.92, 2.12, r'$\mathbf{MPEC\text{-}MFCQ}$', fontsize=9,
            ha='center', fontweight='bold', color='#1a237e', zorder=21)
    ax.text(2.92, 1.92, r'$\nabla G_i^\top \mathbf{d} = 0$', fontsize=8,
            ha='center', color=color_G, zorder=21)
    ax.text(2.92, 1.72, r'$\nabla H_i^\top \mathbf{d} < 0$', fontsize=8,
            ha='center', color=color_H, zorder=21)
    
    # =========================================
    # Index set annotation
    # =========================================
    index_box = FancyBboxPatch((-0.4, -0.4), 1.5, 0.75,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#fff8e1', edgecolor='#f57c00',
                                linewidth=1.5, alpha=0.95, zorder=20)
    ax.add_patch(index_box)
    
    ax.text(0.35, 0.2, r'At $\mathbf{x}^* \in I_{00}$:', fontsize=10,
            ha='center', fontweight='bold', color='#e65100', zorder=21)
    ax.text(0.35, -0.05, r'$G_i(\mathbf{x}^*) = 0$', fontsize=9,
            ha='center', color='#424242', zorder=21)
    ax.text(0.35, -0.25, r'$H_i(\mathbf{x}^*) = 0$', fontsize=9,
            ha='center', color='#424242', zorder=21)
    
    # =========================================
    # Visual indicators for direction properties
    # =========================================
    # Show that d is tangent to G=0 (perpendicular symbol)
    perp_size = 0.08
    # Small perpendicular mark at x* showing d ⊥ ∇G
    
    # Angle arc showing d makes with ∇G
    from matplotlib.patches import Arc
    # The angle between d and the tangent to G
    
    # =========================================
    # Legend
    # =========================================
    legend_elements = [
        Line2D([0], [0], color=color_G, linewidth=2.5, label=r'$G(\mathbf{x}) = 0$ boundary'),
        Line2D([0], [0], color=color_H, linewidth=2.5, label=r'$H(\mathbf{x}) = 0$ boundary'),
        Line2D([0], [0], marker='>', color=color_G, linestyle='-', markersize=8, 
               linewidth=2, label=r'$\nabla G_i(\mathbf{x}^*)$'),
        Line2D([0], [0], marker='>', color=color_H, linestyle='-', markersize=8,
               linewidth=2, label=r'$\nabla H_i(\mathbf{x}^*)$'),
        Line2D([0], [0], marker='>', color=color_d, linestyle='-', markersize=10,
               linewidth=3, label=r'Feasible direction $\mathbf{d}$'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              framealpha=0.95, edgecolor='#bdbdbd')
    
    # Title - moved to top center
    ax.text(1.35, 3.0, r'$\mathbf{Geometry\ of\ MPEC\text{-}MFCQ}$', fontsize=16,
            ha='center', fontweight='bold', color='#1a1a2e')
    
    plt.tight_layout()
    outname = "mpec_mfcq.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
