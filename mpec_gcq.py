# mpec_gcq.py
# Academic illustration of MPEC-GCQ: Tangent and Polar Cone Equality
# Shows (T^{MPEC}_{lin}(x*))° = T(x*)° when MPEC-GCQ holds
# Requires: numpy, matplotlib
# Output: mpec_gcq.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Wedge
from matplotlib.lines import Line2D

def main():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # Color scheme - minimalistic grayscale with accent
    color_primal = '#37474f'      # Dark gray for primal cones
    color_polar = '#78909c'       # Medium gray for polar cones
    color_tangent = '#455a64'     # Tangent cone fill
    color_lin = '#607d8b'         # Linearized cone fill
    color_accent = '#1565c0'      # Blue accent for equality
    color_boundary = '#263238'    # Very dark gray for boundaries
    
    # =========================================
    # Left Panel: Primal Cones T(x*) and T^{MPEC}_{lin}(x*)
    # =========================================
    ax1 = axes[0]
    ax1.set_aspect('equal')
    ax1.set_xlim(-0.3, 2.8)
    ax1.set_ylim(-0.3, 2.8)
    ax1.axis('off')
    
    # Origin point (vertex of cones)
    origin = np.array([0.8, 0.8])
    
    # Define cone angles for MPEC tangent cone
    # Nonconvex union structure: two wedges
    cone_radius = 1.6
    n_pts = 40
    
    # First wedge: lower branch (along G=0 direction)
    theta1_start = -30
    theta1_end = 15
    
    # Second wedge: upper branch (along H=0 direction)
    theta2_start = 50
    theta2_end = 95
    
    # Draw tangent cone T(x*) - first wedge
    angles1 = np.linspace(np.radians(theta1_start), np.radians(theta1_end), n_pts)
    cone1_x = origin[0] + cone_radius * np.cos(angles1)
    cone1_y = origin[1] + cone_radius * np.sin(angles1)
    cone1_pts = [(origin[0], origin[1])] + list(zip(cone1_x, cone1_y))
    cone1_poly = Polygon(cone1_pts, facecolor=color_tangent, alpha=0.35,
                         edgecolor=color_boundary, linewidth=1.5, zorder=3)
    ax1.add_patch(cone1_poly)
    
    # Draw tangent cone T(x*) - second wedge
    angles2 = np.linspace(np.radians(theta2_start), np.radians(theta2_end), n_pts)
    cone2_x = origin[0] + cone_radius * np.cos(angles2)
    cone2_y = origin[1] + cone_radius * np.sin(angles2)
    cone2_pts = [(origin[0], origin[1])] + list(zip(cone2_x, cone2_y))
    cone2_poly = Polygon(cone2_pts, facecolor=color_tangent, alpha=0.35,
                         edgecolor=color_boundary, linewidth=1.5, zorder=3)
    ax1.add_patch(cone2_poly)
    
    # Draw MPEC-linearized cone (same shape, showing equality)
    # Overlay with slightly different style to show it matches
    cone1_lin = Polygon(cone1_pts, facecolor='none', alpha=0.8,
                        edgecolor=color_accent, linewidth=2, linestyle='--', zorder=4)
    ax1.add_patch(cone1_lin)
    cone2_lin = Polygon(cone2_pts, facecolor='none', alpha=0.8,
                        edgecolor=color_accent, linewidth=2, linestyle='--', zorder=4)
    ax1.add_patch(cone2_lin)
    
    # Draw representative direction arrows
    arrow_style = dict(arrowstyle='-|>', mutation_scale=14, lw=2)
    
    # Direction in first wedge
    dir1_angle = np.radians((theta1_start + theta1_end) / 2)
    dir1 = np.array([np.cos(dir1_angle), np.sin(dir1_angle)])
    arrow1 = FancyArrowPatch(
        origin, origin + dir1 * 1.2,
        color=color_boundary, **arrow_style, zorder=6
    )
    ax1.add_patch(arrow1)
    
    # Direction in second wedge
    dir2_angle = np.radians((theta2_start + theta2_end) / 2)
    dir2 = np.array([np.cos(dir2_angle), np.sin(dir2_angle)])
    arrow2 = FancyArrowPatch(
        origin, origin + dir2 * 1.2,
        color=color_boundary, **arrow_style, zorder=6
    )
    ax1.add_patch(arrow2)
    
    # Mark origin
    ax1.plot(origin[0], origin[1], 'ko', markersize=8, zorder=10)
    ax1.text(origin[0] - 0.15, origin[1] - 0.18, r'$\mathbf{x}^*$',
             fontsize=12, fontweight='bold', color='#1a1a2e')
    
    # Labels for primal cones
    ax1.text(1.9, 0.7, r'$T(\mathbf{x}^*)$', fontsize=13, color=color_tangent,
             fontweight='bold', fontstyle='italic')
    ax1.text(1.05, 2.1, r'$T_{\mathrm{lin}}^{\mathrm{MPEC}}$', fontsize=11, 
             color=color_accent, fontweight='bold', fontstyle='italic')
    
    # Panel title
    ax1.text(1.25, 2.6, r'$\mathbf{Primal\ Cones}$', fontsize=14,
             ha='center', fontweight='bold', color='#1a1a2e')
    
    # Annotation
    ax1.text(0.1, 0.15, r'$T(\mathbf{x}^*) = T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)$', 
             fontsize=10, color='#424242', fontstyle='italic',
             bbox=dict(fc='white', ec='#bdbdbd', alpha=0.9, pad=3))
    
    # =========================================
    # Right Panel: Polar Cones T(x*)° and (T^{MPEC}_{lin}(x*))°
    # =========================================
    ax2 = axes[1]
    ax2.set_aspect('equal')
    ax2.set_xlim(-0.3, 2.8)
    ax2.set_ylim(-0.3, 2.8)
    ax2.axis('off')
    
    # Origin for polar cones
    origin2 = np.array([0.8, 0.8])
    
    # Polar cone of a nonconvex union is the intersection of polar cones
    # Polar of wedge [θ1, θ2] is the wedge [θ1 + 90°, θ2 + 90°] rotated
    # For polar: directions d such that <d, v> ≤ 0 for all v in primal cone
    
    # The polar cone is the "opposite" region
    # For the union of two wedges, polar is intersection of their polars
    # This creates a single convex cone in the "gap" region
    
    # Polar cone angles (perpendicular to primal, pointing opposite)
    # Gap between primal wedges: from theta1_end to theta2_start
    # Polar fills: from theta2_end + 90 to theta1_start + 90 (mod 360)
    
    polar_start = theta1_end + 90  # = 105°
    polar_end = theta2_start + 90   # = 140°
    
    # Draw polar cone T(x*)°
    angles_polar = np.linspace(np.radians(polar_start), np.radians(polar_end), n_pts)
    polar_x = origin2[0] + cone_radius * np.cos(angles_polar)
    polar_y = origin2[1] + cone_radius * np.sin(angles_polar)
    polar_pts = [(origin2[0], origin2[1])] + list(zip(polar_x, polar_y))
    polar_poly = Polygon(polar_pts, facecolor=color_polar, alpha=0.4,
                         edgecolor=color_boundary, linewidth=1.5, zorder=3)
    ax2.add_patch(polar_poly)
    
    # Draw (T^{MPEC}_{lin})° - same shape, dashed overlay
    polar_lin = Polygon(polar_pts, facecolor='none', alpha=0.8,
                        edgecolor=color_accent, linewidth=2, linestyle='--', zorder=4)
    ax2.add_patch(polar_lin)
    
    # Draw representative direction in polar cone
    polar_mid_angle = np.radians((polar_start + polar_end) / 2)
    polar_dir = np.array([np.cos(polar_mid_angle), np.sin(polar_mid_angle)])
    arrow_polar = FancyArrowPatch(
        origin2, origin2 + polar_dir * 1.2,
        color=color_boundary, **arrow_style, zorder=6
    )
    ax2.add_patch(arrow_polar)
    
    # Show the "excluded" regions (primal cones) with light shading
    # First primal wedge (ghost)
    cone1_ghost = Polygon(cone1_pts, facecolor='#eceff1', alpha=0.3,
                          edgecolor='#b0bec5', linewidth=1, linestyle=':', zorder=1)
    ax2.add_patch(cone1_ghost)
    # Second primal wedge (ghost)
    cone2_ghost = Polygon(cone2_pts, facecolor='#eceff1', alpha=0.3,
                          edgecolor='#b0bec5', linewidth=1, linestyle=':', zorder=1)
    ax2.add_patch(cone2_ghost)
    
    # Mark origin
    ax2.plot(origin2[0], origin2[1], 'ko', markersize=8, zorder=10)
    ax2.text(origin2[0] - 0.15, origin2[1] - 0.18, r'$\mathbf{x}^*$',
             fontsize=12, fontweight='bold', color='#1a1a2e')
    
    # Labels for polar cones
    ax2.text(0.3, 2.05, r'$T(\mathbf{x}^*)^\circ$', fontsize=13, color=color_polar,
             fontweight='bold', fontstyle='italic')
    ax2.text(1.35, 2.25, r'$(T_{\mathrm{lin}}^{\mathrm{MPEC}})^\circ$', fontsize=11,
             color=color_accent, fontweight='bold', fontstyle='italic')
    
    # Ghost labels
    ax2.text(1.85, 0.55, r'$T(\mathbf{x}^*)$', fontsize=9, color='#90a4ae',
             fontstyle='italic', alpha=0.7)
    
    # Panel title
    ax2.text(1.25, 2.6, r'$\mathbf{Polar\ Cones}$', fontsize=14,
             ha='center', fontweight='bold', color='#1a1a2e')
    
    # Annotation
    ax2.text(1.4, 0.15, r'$(T_{\mathrm{lin}}^{\mathrm{MPEC}})^\circ = T(\mathbf{x}^*)^\circ$',
             fontsize=10, color='#424242', fontstyle='italic',
             bbox=dict(fc='white', ec='#bdbdbd', alpha=0.9, pad=3))
    
    # =========================================
    # Central MPEC-GCQ statement
    # =========================================
    fig.text(0.5, 0.06,
             r'$\mathbf{MPEC\text{-}GCQ:}\ \ \left(T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)\right)^\circ = T(\mathbf{x}^*)^\circ$',
             fontsize=14, ha='center', fontweight='bold', color='#1a237e')
    
    # =========================================
    # Main title
    # =========================================
    fig.suptitle(r'$\mathbf{MPEC\text{-}GCQ:\ Guignard\ Constraint\ Qualification}$',
                 fontsize=16, fontweight='bold', y=0.96, color='#1a1a2e')
    
    # =========================================
    # Legend
    # =========================================
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor=color_tangent,
               markersize=12, alpha=0.5, label=r'$T(\mathbf{x}^*)$ (primal)'),
        Line2D([0], [0], color=color_accent, linewidth=2, linestyle='--',
               label=r'$T_{\mathrm{lin}}^{\mathrm{MPEC}}(\mathbf{x}^*)$'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=color_polar,
               markersize=12, alpha=0.5, label=r'$T(\mathbf{x}^*)^\circ$ (polar)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#eceff1',
               markeredgecolor='#b0bec5', markersize=12, alpha=0.5, 
               label=r'Primal cone (ghost)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=9,
               framealpha=0.95, edgecolor='#bdbdbd', bbox_to_anchor=(0.5, -0.01))
    
    plt.tight_layout(rect=[0, 0.10, 1, 0.94])
    outname = "mpec_gcq.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
