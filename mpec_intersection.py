"""
Save as: mpec_intersection.py
Requires: matplotlib
Run: python mpec_intersection.py
This will create 'mpec_intersection.png' in the same folder.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def draw_mpec_venn(filename="mpec_intersection.png", figsize=(12,10), dpi=300):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.axis('off')

    # Circle parameters: (x, y), radius - larger radius for better visibility
    radius = 1.2
    c1 = Circle((-0.65, 0.0), radius, facecolor="#66c2a5", alpha=0.6, edgecolor='#2d5c4a', linewidth=2.5)
    c2 = Circle(( 0.65, 0.0), radius, facecolor="#fc8d62", alpha=0.6, edgecolor='#8b4a2d', linewidth=2.5)
    c3 = Circle((0.0, 0.9), radius, facecolor="#8da0cb", alpha=0.6, edgecolor='#3d4d6b', linewidth=2.5)

    for c in (c1, c2, c3):
        ax.add_patch(c)

    # Labels for the three main sets - positioned properly aligned in each circle
    ax.text(-1.0, -0.5, "Optimization\nTheory", fontsize=14, ha='center', va='center', 
            fontweight='bold', color='#1a3d2e')
    ax.text( 1.0, -0.5, "Variational\nAnalysis", fontsize=14, ha='center', va='center',
            fontweight='bold', color='#5a2d18')
    ax.text( 0.0,  1.5, "Equilibrium\nModeling", fontsize=14, ha='center', va='center',
            fontweight='bold', color='#2a3650')

    # Central label for the triple intersection - larger and more prominent
    ax.text(0.0, 0.35, "MPEC", fontsize=22, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2, alpha=0.9))
    
    # Caption with better positioning - closer to image
    ax.text(0.0, -1.85,
            "The central region (MPEC) represents Mathematical Programs with Equilibrium Constraints,\n"
            "which combine complementarity and equilibrium conditions from all three foundational areas.",
            fontsize=11, ha='center', style='italic', 
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', alpha=0.7))

    # Set better axis limits - tighter spacing
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.4, 2.7)
    
    # Save with high quality
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved diagram to {filename}")

if __name__ == "__main__":
    draw_mpec_venn()
