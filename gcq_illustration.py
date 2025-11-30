# gcq_illustration.py
# Academic illustration of Guignard Constraint Qualification (GCQ)
# Shows tangent cone T(x*), linearized cone L(x*), and their polar cones
# Key result: T(x*)° = L(x*)° defines GCQ
# Requires: numpy, matplotlib
# Output: gcq_illustration.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Arc
from matplotlib.lines import Line2D

def draw_cone(ax, origin, angle1, angle2, length, facecolor, edgecolor, 
              alpha=0.3, linewidth=2, label_pos=None, label=None, label_color='black'):
    """Draw a 2D cone as a filled wedge with boundary rays."""
    
    # Create cone boundary points
    n_points = 50
    angles = np.linspace(np.radians(angle1), np.radians(angle2), n_points)
    
    # Cone vertices
    x_pts = [origin[0]] + [origin[0] + length * np.cos(a) for a in angles] + [origin[0]]
    y_pts = [origin[1]] + [origin[1] + length * np.sin(a) for a in angles] + [origin[1]]
    
    # Draw filled cone
    cone = Polygon(list(zip(x_pts, y_pts)), facecolor=facecolor, 
                   edgecolor='none', alpha=alpha, zorder=2)
    ax.add_patch(cone)
    
    # Draw boundary rays
    ray1_end = (origin[0] + length * np.cos(np.radians(angle1)), 
                origin[1] + length * np.sin(np.radians(angle1)))
    ray2_end = (origin[0] + length * np.cos(np.radians(angle2)), 
                origin[1] + length * np.sin(np.radians(angle2)))
    
    ax.plot([origin[0], ray1_end[0]], [origin[1], ray1_end[1]], 
            color=edgecolor, linewidth=linewidth, solid_capstyle='round', zorder=3)
    ax.plot([origin[0], ray2_end[0]], [origin[1], ray2_end[1]], 
            color=edgecolor, linewidth=linewidth, solid_capstyle='round', zorder=3)
    
    # Add arrowheads
    arrow_len = 0.92
    for angle in [angle1, angle2]:
        end = (origin[0] + length * arrow_len * np.cos(np.radians(angle)),
               origin[1] + length * arrow_len * np.sin(np.radians(angle)))
        tip = (origin[0] + length * np.cos(np.radians(angle)),
               origin[1] + length * np.sin(np.radians(angle)))
        ax.annotate('', xy=tip, xytext=end,
                    arrowprops=dict(arrowstyle='-|>', color=edgecolor, lw=linewidth,
                                   mutation_scale=12), zorder=4)
    
    # Add label
    if label and label_pos:
        ax.text(label_pos[0], label_pos[1], label, fontsize=13, color=label_color,
                fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=label_color,
                         linewidth=1.5, alpha=0.95))
    
    return cone

def main():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # =========================================
    # LEFT PANEL: Primal Cones T(x*) and L(x*)
    # =========================================
    ax1 = axes[0]
    ax1.set_aspect('equal')
    ax1.set_xlim(-0.3, 2.8)
    ax1.set_ylim(-0.5, 2.3)
    ax1.axis('off')
    
    # Origin point x*
    origin = (0.2, 0.2)
    
    # Tangent cone T(x*) - narrower, nonconvex-ish appearance
    # Red/coral color scheme
    t_angle1, t_angle2 = 25, 75
    draw_cone(ax1, origin, t_angle1, t_angle2, 1.6,
              facecolor='#ffcdd2', edgecolor='#c62828', alpha=0.4,
              label_pos=(1.0, 1.55), label=r'$T(\mathbf{x}^*)$', label_color='#b71c1c')
    
    # Linearized cone L(x*) - wider, contains T(x*)
    # Blue color scheme, semi-transparent overlay
    l_angle1, l_angle2 = 10, 90
    draw_cone(ax1, origin, l_angle1, l_angle2, 1.8,
              facecolor='#bbdefb', edgecolor='#1565c0', alpha=0.25, linewidth=1.5,
              label_pos=(1.85, 0.85), label=r'$L(\mathbf{x}^*)$', label_color='#0d47a1')
    
    # Mark x*
    ax1.plot(origin[0], origin[1], 'ko', markersize=10, zorder=10)
    ax1.text(origin[0] - 0.15, origin[1] - 0.15, r'$\mathbf{x}^*$', 
             fontsize=14, fontweight='bold', ha='center')
    
    # Panel title
    ax1.text(1.3, 2.1, 'Primal Cones', fontsize=14, fontweight='bold', 
             ha='center', color='#37474f')
    
    # Show inclusion T ⊆ L
    ax1.text(1.3, -0.3, r'$T(\mathbf{x}^*) \subseteq L(\mathbf{x}^*)$', 
             fontsize=12, ha='center', color='#546e7a', fontstyle='italic')
    
    # =========================================
    # RIGHT PANEL: Polar Cones T(x*)° and L(x*)°
    # =========================================
    ax2 = axes[1]
    ax2.set_aspect('equal')
    ax2.set_xlim(-0.3, 2.8)
    ax2.set_ylim(-0.5, 2.3)
    ax2.axis('off')
    
    # Origin for polar cones
    origin2 = (0.2, 0.2)
    
    # Polar cone of T(x*): T(x*)°
    # The polar of a cone with angles [25°, 75°] has angles [90°+25°, 90°+75°] = [115°, 165°]
    # Actually, polar cone is perpendicular: if T spans [θ1, θ2], then T° spans [θ2+90°, θ1+90°+180°]
    # For T in [25°, 75°], polar T° contains vectors v where v·t ≤ 0 for all t in T
    # This means T° is in the half-plane opposite to T
    # Polar of cone [25°, 75°] is approximately [165°, 205°] (perpendicular + opposite)
    
    # Simplified: polar cone is "behind" the primal cone
    # T° spans from (75+90)° to (25+90+180)° = 165° to 295°
    # But we want the acute polar, so: perpendicular to the cone boundaries
    
    # For a cone spanning [α, β], its polar spans [β+90, α+270] mod 360
    # T: [25, 75] -> T°: [75+90, 25+90+180] = [165, 295] - but this is reflex
    # Take the "normal" polar: [90+75, 90+25+180] -> simplify to [165, 295]
    
    # Let's use: T° perpendicular region
    t_polar_angle1, t_polar_angle2 = 165, 245  # Adjusted for visual clarity
    
    # Draw T(x*)° - same red color to show connection
    draw_cone(ax2, origin2, t_polar_angle1, t_polar_angle2, 1.5,
              facecolor='#ffcdd2', edgecolor='#c62828', alpha=0.4,
              label_pos=(0.0, 1.5), label=r'$T(\mathbf{x}^*)^\circ$', label_color='#b71c1c')
    
    # Polar cone of L(x*): L(x*)°
    # L: [10, 90] -> L°: perpendicular opposite region
    l_polar_angle1, l_polar_angle2 = 180, 260  # Wider than T° since L is wider than T
    
    # For GCQ: T° = L° (they are equal!)
    # So we draw them overlapping with the same boundaries
    # The key insight: even though T ⊆ L, we have T° = L° when GCQ holds
    
    # Draw L(x*)° with slight offset/transparency to show equality
    # Using purple/mixed color to show T° = L°
    draw_cone(ax2, origin2, t_polar_angle1, t_polar_angle2, 1.5,
              facecolor='#e1bee7', edgecolor='#7b1fa2', alpha=0.3, linewidth=1.5,
              label_pos=(0.85, 0.4), label=r'$L(\mathbf{x}^*)^\circ$', label_color='#6a1b9a')
    
    # Mark origin
    ax2.plot(origin2[0], origin2[1], 'ko', markersize=10, zorder=10)
    ax2.text(origin2[0] + 0.15, origin2[1] - 0.15, r'$\mathbf{0}$', 
             fontsize=14, fontweight='bold', ha='center')
    
    # Panel title
    ax2.text(1.3, 2.1, 'Polar Cones', fontsize=14, fontweight='bold', 
             ha='center', color='#37474f')
    
    # GCQ condition - the key equality
    ax2.text(1.3, -0.3, r'$\mathbf{GCQ:}\ T(\mathbf{x}^*)^\circ = L(\mathbf{x}^*)^\circ$', 
             fontsize=12, ha='center', color='#4a148c', fontweight='bold')
    
    # =========================================
    # Central explanation
    # =========================================
    fig.text(0.5, 0.02, 
             r'Guignard CQ holds when the polar cones coincide: $T(\mathbf{x}^*)^\circ = L(\mathbf{x}^*)^\circ$',
             fontsize=11, ha='center', va='bottom', color='#37474f', fontstyle='italic')
    
    # Add connecting arrow between panels
    fig.patches.append(plt.Arrow(0.48, 0.5, 0.04, 0, width=0.03, 
                                  transform=fig.transFigure, color='#78909c', alpha=0.6))
    
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    outname = "gcq_illustration.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
