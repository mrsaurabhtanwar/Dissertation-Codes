# mpec_licq.py
# Academic illustration of MPEC-LICQ structure
# Shows complementarity constraints and index sets I_0+, I_+0, I_00
# Indicates which gradients are included in the MPEC-LICQ condition
# Requires: numpy, matplotlib
# Output: mpec_licq.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D

def main():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Color scheme
    color_included = '#1565c0'      # Blue - included in LICQ
    color_excluded = '#9e9e9e'      # Gray - excluded
    color_I0plus = '#c62828'        # Red for I_0+
    color_Iplus0 = '#2e7d32'        # Green for I_+0
    color_I00 = '#6a1b9a'           # Purple for I_00
    box_bg = '#fafafa'
    
    # =========================================
    # Title
    # =========================================
    ax.text(7, 9.5, r'$\mathbf{MPEC\text{-}LICQ\ Structure}$', fontsize=18, 
            ha='center', fontweight='bold', color='#1a1a2e')
    
    # Complementarity condition
    ax.text(7, 8.8, r'Complementarity: $0 \leq G(\mathbf{x}) \perp H(\mathbf{x}) \geq 0$',
            fontsize=13, ha='center', color='#37474f')
    
    # =========================================
    # Three index set boxes
    # =========================================
    box_width = 3.8
    box_height = 5.5
    box_y = 2.0
    
    # Box positions
    box1_x = 0.8    # I_0+
    box2_x = 5.1    # I_+0
    box3_x = 9.4    # I_00
    
    # --- Box 1: I_0+ (G active, H inactive) ---
    box1 = FancyBboxPatch((box1_x, box_y), box_width, box_height,
                           boxstyle="round,pad=0.05,rounding_size=0.2",
                           facecolor='#ffebee', edgecolor=color_I0plus,
                           linewidth=2, alpha=0.9)
    ax.add_patch(box1)
    
    # Title for I_0+
    ax.text(box1_x + box_width/2, box_y + box_height - 0.4,
            r'$I_{0+}$', fontsize=16, ha='center', fontweight='bold', color=color_I0plus)
    ax.text(box1_x + box_width/2, box_y + box_height - 0.9,
            r'$G_i(\mathbf{x}^*) = 0,\ H_i(\mathbf{x}^*) > 0$',
            fontsize=10, ha='center', color='#424242')
    
    # Content for I_0+
    y_pos = box_y + box_height - 1.6
    
    # G gradient - INCLUDED
    ax.annotate('', xy=(box1_x + 2.8, y_pos), xytext=(box1_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_included, lw=2.5,
                               mutation_scale=15))
    ax.text(box1_x + 2.0, y_pos + 0.35, r'$\nabla G_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_included, fontweight='bold')
    ax.text(box1_x + 2.0, y_pos - 0.4, r'$\checkmark$ Included',
            fontsize=9, ha='center', color=color_included)
    
    # H gradient - EXCLUDED
    y_pos -= 1.4
    ax.annotate('', xy=(box1_x + 2.8, y_pos), xytext=(box1_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_excluded, lw=2,
                               mutation_scale=12, linestyle='--'))
    ax.text(box1_x + 2.0, y_pos + 0.35, r'$\nabla H_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_excluded)
    ax.text(box1_x + 2.0, y_pos - 0.4, r'$\times$ Excluded',
            fontsize=9, ha='center', color=color_excluded)
    
    # Reason
    ax.text(box1_x + box_width/2, box_y + 0.6,
            r'$H_i > 0 \Rightarrow$ constraint',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    ax.text(box1_x + box_width/2, box_y + 0.25,
            r'not active for $H$',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    
    # --- Box 2: I_+0 (G inactive, H active) ---
    box2 = FancyBboxPatch((box2_x, box_y), box_width, box_height,
                           boxstyle="round,pad=0.05,rounding_size=0.2",
                           facecolor='#e8f5e9', edgecolor=color_Iplus0,
                           linewidth=2, alpha=0.9)
    ax.add_patch(box2)
    
    # Title for I_+0
    ax.text(box2_x + box_width/2, box_y + box_height - 0.4,
            r'$I_{+0}$', fontsize=16, ha='center', fontweight='bold', color=color_Iplus0)
    ax.text(box2_x + box_width/2, box_y + box_height - 0.9,
            r'$G_i(\mathbf{x}^*) > 0,\ H_i(\mathbf{x}^*) = 0$',
            fontsize=10, ha='center', color='#424242')
    
    # Content for I_+0
    y_pos = box_y + box_height - 1.6
    
    # G gradient - EXCLUDED
    ax.annotate('', xy=(box2_x + 2.8, y_pos), xytext=(box2_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_excluded, lw=2,
                               mutation_scale=12, linestyle='--'))
    ax.text(box2_x + 2.0, y_pos + 0.35, r'$\nabla G_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_excluded)
    ax.text(box2_x + 2.0, y_pos - 0.4, r'$\times$ Excluded',
            fontsize=9, ha='center', color=color_excluded)
    
    # H gradient - INCLUDED
    y_pos -= 1.4
    ax.annotate('', xy=(box2_x + 2.8, y_pos), xytext=(box2_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_included, lw=2.5,
                               mutation_scale=15))
    ax.text(box2_x + 2.0, y_pos + 0.35, r'$\nabla H_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_included, fontweight='bold')
    ax.text(box2_x + 2.0, y_pos - 0.4, r'$\checkmark$ Included',
            fontsize=9, ha='center', color=color_included)
    
    # Reason
    ax.text(box2_x + box_width/2, box_y + 0.6,
            r'$G_i > 0 \Rightarrow$ constraint',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    ax.text(box2_x + box_width/2, box_y + 0.25,
            r'not active for $G$',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    
    # --- Box 3: I_00 (Both active - degenerate) ---
    box3 = FancyBboxPatch((box3_x, box_y), box_width, box_height,
                           boxstyle="round,pad=0.05,rounding_size=0.2",
                           facecolor='#f3e5f5', edgecolor=color_I00,
                           linewidth=2, alpha=0.9)
    ax.add_patch(box3)
    
    # Title for I_00
    ax.text(box3_x + box_width/2, box_y + box_height - 0.4,
            r'$I_{00}$', fontsize=16, ha='center', fontweight='bold', color=color_I00)
    ax.text(box3_x + box_width/2, box_y + box_height - 0.9,
            r'$G_i(\mathbf{x}^*) = 0,\ H_i(\mathbf{x}^*) = 0$',
            fontsize=10, ha='center', color='#424242')
    ax.text(box3_x + box_width/2, box_y + box_height - 1.2,
            r'(Biactive / Degenerate)',
            fontsize=9, ha='center', color=color_I00, fontstyle='italic')
    
    # Content for I_00
    y_pos = box_y + box_height - 1.8
    
    # G gradient - INCLUDED
    ax.annotate('', xy=(box3_x + 2.8, y_pos), xytext=(box3_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_included, lw=2.5,
                               mutation_scale=15))
    ax.text(box3_x + 2.0, y_pos + 0.35, r'$\nabla G_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_included, fontweight='bold')
    ax.text(box3_x + 2.0, y_pos - 0.4, r'$\checkmark$ Included',
            fontsize=9, ha='center', color=color_included)
    
    # H gradient - INCLUDED
    y_pos -= 1.4
    ax.annotate('', xy=(box3_x + 2.8, y_pos), xytext=(box3_x + 1.2, y_pos),
                arrowprops=dict(arrowstyle='-|>', color=color_included, lw=2.5,
                               mutation_scale=15))
    ax.text(box3_x + 2.0, y_pos + 0.35, r'$\nabla H_i(\mathbf{x}^*)$',
            fontsize=11, ha='center', color=color_included, fontweight='bold')
    ax.text(box3_x + 2.0, y_pos - 0.4, r'$\checkmark$ Included',
            fontsize=9, ha='center', color=color_included)
    
    # Reason
    ax.text(box3_x + box_width/2, box_y + 0.6,
            r'Both constraints active',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    ax.text(box3_x + box_width/2, box_y + 0.25,
            r'$\Rightarrow$ both gradients needed',
            fontsize=9, ha='center', color='#616161', fontstyle='italic')
    
    # =========================================
    # MPEC-LICQ Definition Box
    # =========================================
    licq_box = FancyBboxPatch((1.5, 0.3), 11, 1.4,
                               boxstyle="round,pad=0.05,rounding_size=0.15",
                               facecolor='#e3f2fd', edgecolor='#1565c0',
                               linewidth=2, alpha=0.95)
    ax.add_patch(licq_box)
    
    ax.text(7, 1.35, r'$\mathbf{MPEC\text{-}LICQ:}$ The following gradients are linearly independent:',
            fontsize=11, ha='center', fontweight='bold', color='#0d47a1')
    
    ax.text(7, 0.75,
            r'$\left\{ \nabla G_i(\mathbf{x}^*) \right\}_{i \in I_{0+} \cup I_{00}} \cup \left\{ \nabla H_i(\mathbf{x}^*) \right\}_{i \in I_{+0} \cup I_{00}}$',
            fontsize=12, ha='center', color='#1a237e')
    
    # =========================================
    # Legend
    # =========================================
    legend_elements = [
        Line2D([0], [0], marker='>', color=color_included, linestyle='-',
               markersize=10, linewidth=2.5, label='Included in MPEC-LICQ'),
        Line2D([0], [0], marker='>', color=color_excluded, linestyle='--',
               markersize=8, linewidth=2, label='Excluded (not active)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
              framealpha=0.95, edgecolor='#bdbdbd')
    
    plt.tight_layout()
    outname = "mpec_licq.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
