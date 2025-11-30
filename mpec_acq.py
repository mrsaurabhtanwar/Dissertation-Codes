# mpec_acq.py
# Academic illustration of MPEC-ACQ: Tangent Cone vs MPEC-Linearized Cone
# Shows equality T(x*) = T^{MPEC}_{lin}(x*) when MPEC-ACQ holds
# Requires: numpy, matplotlib
# Output: mpec_acq.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Wedge, Arc
from matplotlib.lines import Line2D

def main():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # Color scheme - muted academic style
    color_G = '#c62828'          # Red for G=0 boundary
    color_H = '#1565c0'          # Blue for H=0 boundary
    color_tangent = '#5e35b1'    # Purple for true tangent cone
    color_lin = '#00897b'        # Teal for linearized cone
    color_region = '#e8eaf6'     # Light purple-gray for feasible region
    color_ray = '#37474f'        # Dark gray for rays
    
    # =========================================
    # Left Panel: True Tangent Cone T(x*)
    # =========================================
    ax1 = axes[0]
    ax1.set_aspect('equal')
    ax1.set_xlim(-0.5, 3.0)
    ax1.set_ylim(-0.5, 2.8)
    ax1.axis('off')
    
    # Point x* at origin of the cone visualization
    x_star = np.array([1.2, 1.0])
    
    # Draw G=0 and H=0 boundaries through x*
    # G=0: slope -0.4
    g_x = np.array([0.0, 2.8])
    g_y = x_star[1] - 0.4 * (g_x - x_star[0])
    ax1.plot(g_x, g_y, color=color_G, linewidth=2.5, solid_capstyle='round', zorder=3)
    
    # H=0: slope 1.5
    h_x = np.array([0.5, 2.0])
    h_y = x_star[1] + 1.5 * (h_x - x_star[0])
    ax1.plot(h_x, h_y, color=color_H, linewidth=2.5, solid_capstyle='round', zorder=3)
    
    # True tangent cone - nonconvex union of rays
    # At biactive point (I_00), tangent cone is union of two half-spaces
    # Ray 1: along G=0 (tangent direction)
    # Ray 2: along H=0 (tangent direction)
    # Plus rays into feasible region
    
    # Tangent cone visualization as shaded wedges
    # The tangent cone at I_00 is the union: (T_G ∩ {H≥0}) ∪ (T_H ∩ {G≥0})
    
    # Wedge 1: Rays along G=0 direction (into H≥0 region)
    tangent_G_dir = np.array([1.0, -0.4])
    tangent_G_dir = tangent_G_dir / np.linalg.norm(tangent_G_dir)
    angle_G = np.degrees(np.arctan2(tangent_G_dir[1], tangent_G_dir[0]))
    
    # Wedge 2: Rays along H=0 direction (into G≥0 region)
    tangent_H_dir = np.array([1.0, 1.5])
    tangent_H_dir = tangent_H_dir / np.linalg.norm(tangent_H_dir)
    angle_H = np.degrees(np.arctan2(tangent_H_dir[1], tangent_H_dir[0]))
    
    # Draw the tangent cone as union of two wedges
    # First wedge: from tangent to G=0 going into H>0 region
    cone_radius = 1.2
    
    # Create polygon for tangent cone (nonconvex shape)
    # This shows the union structure
    n_pts = 30
    
    # First branch: along and below G=0 (into H≥0)
    theta1_start = angle_G - 90  # perpendicular into feasible
    theta1_end = angle_G
    
    # Second branch: along and above H=0 (into G≥0)  
    theta2_start = angle_H
    theta2_end = angle_H + 90  # perpendicular into feasible
    
    # Draw first cone section (lower)
    angles1 = np.linspace(np.radians(theta1_start), np.radians(theta1_end), n_pts)
    cone1_x = x_star[0] + cone_radius * np.cos(angles1)
    cone1_y = x_star[1] + cone_radius * np.sin(angles1)
    cone1_pts = [(x_star[0], x_star[1])] + list(zip(cone1_x, cone1_y))
    cone1_poly = Polygon(cone1_pts, facecolor=color_tangent, alpha=0.25, 
                         edgecolor='none', zorder=2)
    ax1.add_patch(cone1_poly)
    
    # Draw second cone section (upper)
    angles2 = np.linspace(np.radians(theta2_start), np.radians(theta2_end), n_pts)
    cone2_x = x_star[0] + cone_radius * np.cos(angles2)
    cone2_y = x_star[1] + cone_radius * np.sin(angles2)
    cone2_pts = [(x_star[0], x_star[1])] + list(zip(cone2_x, cone2_y))
    cone2_poly = Polygon(cone2_pts, facecolor=color_tangent, alpha=0.25,
                         edgecolor='none', zorder=2)
    ax1.add_patch(cone2_poly)
    
    # Draw representative rays
    arrow_style = dict(arrowstyle='-|>', mutation_scale=14, lw=2)
    
    # Ray along G=0 (both directions for tangent)
    ray_len = 0.9
    arrow1 = FancyArrowPatch(
        x_star, x_star + tangent_G_dir * ray_len,
        color=color_ray, **arrow_style, zorder=8
    )
    ax1.add_patch(arrow1)
    
    # Ray along H=0
    arrow2 = FancyArrowPatch(
        x_star, x_star + tangent_H_dir * ray_len,
        color=color_ray, **arrow_style, zorder=8
    )
    ax1.add_patch(arrow2)
    
    # Ray into interior (diagonal)
    interior_dir = tangent_G_dir + tangent_H_dir
    interior_dir = interior_dir / np.linalg.norm(interior_dir)
    arrow3 = FancyArrowPatch(
        x_star, x_star + interior_dir * ray_len * 0.8,
        color=color_ray, alpha=0.6, **arrow_style, zorder=8
    )
    ax1.add_patch(arrow3)
    
    # Mark x*
    ax1.plot(x_star[0], x_star[1], 'ko', markersize=10, zorder=15)
    ax1.text(x_star[0] + 0.12, x_star[1] - 0.2, r'$\mathbf{x}^*$',
             fontsize=13, fontweight='bold', color='#1a1a2e')
    
    # Labels - positioned away from cone
    ax1.text(2.5, 0.25, r'$G = 0$', fontsize=11, color=color_G, fontweight='bold')
    ax1.text(1.65, 2.35, r'$H = 0$', fontsize=11, color=color_H, fontweight='bold')
    
    # Cone label - positioned inside upper cone region
    ax1.text(0.35, 1.65, r'$T(\mathbf{x}^*)$', fontsize=14, color=color_tangent, 
             fontweight='bold', fontstyle='italic')
    
    # Panel title
    ax1.text(1.25, 2.6, r'$\mathbf{True\ Tangent\ Cone}$', fontsize=14,
             ha='center', fontweight='bold', color='#1a1a2e')
    
    # Annotation: nonconvex union
    ax1.text(0.1, 0.1, r'Nonconvex union', fontsize=9, color='#616161',
             fontstyle='italic', alpha=0.8)
    
    # =========================================
    # Right Panel: MPEC-Linearized Cone T^{MPEC}_{lin}(x*)
    # =========================================
    ax2 = axes[1]
    ax2.set_aspect('equal')
    ax2.set_xlim(-0.5, 3.0)
    ax2.set_ylim(-0.5, 2.8)
    ax2.axis('off')
    
    # Same point x*
    x_star2 = np.array([1.2, 1.0])
    
    # Draw G=0 and H=0 boundaries
    ax2.plot(g_x, g_y, color=color_G, linewidth=2.5, solid_capstyle='round', zorder=3)
    ax2.plot(h_x, h_y, color=color_H, linewidth=2.5, solid_capstyle='round', zorder=3)
    
    # MPEC-Linearized cone
    # For MPEC-ACQ: T^{MPEC}_{lin}(x*) accounts for complementarity structure
    # It's defined by: d such that for each i in I_00:
    #   ∇G_i'd ≥ 0 AND ∇H_i'd ≥ 0  (both can increase), OR
    #   ∇G_i'd ≥ 0 AND ∇H_i'd = 0  (G increases, H stays), OR
    #   ∇G_i'd = 0 AND ∇H_i'd ≥ 0  (G stays, H increases)
    # This exactly matches the tangent cone structure when MPEC-ACQ holds
    
    # Draw the same cone structure to show equality
    # First branch
    cone1_poly2 = Polygon(cone1_pts, facecolor=color_lin, alpha=0.25,
                          edgecolor='none', zorder=2)
    ax2.add_patch(cone1_poly2)
    
    # Second branch
    cone2_poly2 = Polygon(cone2_pts, facecolor=color_lin, alpha=0.25,
                          edgecolor='none', zorder=2)
    ax2.add_patch(cone2_poly2)
    
    # Draw the same representative rays with complementarity labels
    arrow1b = FancyArrowPatch(
        x_star2, x_star2 + tangent_G_dir * ray_len,
        color=color_ray, **arrow_style, zorder=8
    )
    ax2.add_patch(arrow1b)
    
    arrow2b = FancyArrowPatch(
        x_star2, x_star2 + tangent_H_dir * ray_len,
        color=color_ray, **arrow_style, zorder=8
    )
    ax2.add_patch(arrow2b)
    
    arrow3b = FancyArrowPatch(
        x_star2, x_star2 + interior_dir * ray_len * 0.8,
        color=color_ray, alpha=0.6, **arrow_style, zorder=8
    )
    ax2.add_patch(arrow3b)
    
    # Mark x*
    ax2.plot(x_star2[0], x_star2[1], 'ko', markersize=10, zorder=15)
    ax2.text(x_star2[0] + 0.12, x_star2[1] - 0.2, r'$\mathbf{x}^*$',
             fontsize=13, fontweight='bold', color='#1a1a2e')
    
    # Labels - positioned away from cone
    ax2.text(2.5, 0.25, r'$G = 0$', fontsize=11, color=color_G, fontweight='bold')
    ax2.text(1.65, 2.35, r'$H = 0$', fontsize=11, color=color_H, fontweight='bold')
    
    # Cone label - positioned inside upper cone region
    ax2.text(0.25, 1.65, r'$T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)$', 
             fontsize=12, color=color_lin, fontweight='bold', fontstyle='italic')
    
    # Panel title
    ax2.text(1.25, 2.6, r'$\mathbf{MPEC\text{-}Linearized\ Cone}$', fontsize=14,
             ha='center', fontweight='bold', color='#1a1a2e')
    
    # Annotation: complementarity structure
    ax2.text(0.1, 0.1, r'Complementarity-aware', fontsize=9, color='#616161',
             fontstyle='italic', alpha=0.8)
    
    # =========================================
    # Add small complementarity condition labels - positioned away from boundaries
    # =========================================
    # Label for ray along G=0 direction (lower ray)
    ax2.text(2.25, 0.7, r'$\nabla G^\top d = 0$', fontsize=9, color=color_G, 
             alpha=0.9, bbox=dict(fc='white', ec='none', alpha=0.8, pad=1))
    
    # Label for ray along H=0 direction (upper ray)  
    ax2.text(0.55, 2.0, r'$\nabla H^\top d = 0$', fontsize=9, color=color_H,
             alpha=0.9, bbox=dict(fc='white', ec='none', alpha=0.8, pad=1))
    
    # =========================================
    # Central equality annotation
    # =========================================
    fig.text(0.5, 0.08, 
             r'$\mathbf{MPEC\text{-}ACQ\ holds:}\ \ T(\mathbf{x}^*) = T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)$',
             fontsize=14, ha='center', fontweight='bold', color='#1a237e')
    
    # =========================================
    # Main title
    # =========================================
    fig.suptitle(r'$\mathbf{MPEC\text{-}ACQ:\ Tangent\ Cone\ Equality}$', 
                 fontsize=16, fontweight='bold', y=0.96, color='#1a1a2e')
    
    # =========================================
    # Legend
    # =========================================
    legend_elements = [
        Line2D([0], [0], color=color_G, linewidth=2.5, label=r'$G(\mathbf{x}) = 0$'),
        Line2D([0], [0], color=color_H, linewidth=2.5, label=r'$H(\mathbf{x}) = 0$'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=color_tangent, 
               markersize=12, alpha=0.5, label=r'$T(\mathbf{x}^*)$'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=color_lin,
               markersize=12, alpha=0.5, label=r'$T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)$'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10,
               framealpha=0.95, edgecolor='#bdbdbd', bbox_to_anchor=(0.5, 0.01))
    
    plt.tight_layout(rect=[0, 0.12, 1, 0.94])
    outname = "mpec_acq.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
