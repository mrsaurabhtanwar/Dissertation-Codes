# mpec_cq_hierarchy.py
# Academic Hasse diagram showing MPEC constraint qualification hierarchy
# Shows implication relationships: LICQ → MFCQ → ACQ → GCQ, LICQ → CRCQ → CPLD
# Requires: numpy, matplotlib
# Output: mpec_cq_hierarchy.png

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
from matplotlib.lines import Line2D

def main():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-1, 11)
    ax.set_ylim(-0.5, 9.5)
    ax.axis('off')
    
    # Color scheme - muted blue/gray academic palette
    color_node_fill = '#e3f2fd'       # Light blue fill
    color_node_edge = '#1565c0'       # Blue edge
    color_arrow = '#37474f'           # Dark gray arrows
    color_text = '#1a1a2e'            # Near-black text
    color_strong = '#0d47a1'          # Strong blue for top node
    color_weak = '#78909c'            # Gray for weaker CQs
    
    # Node positions (x, y) - Hasse diagram layout
    # Top: MPEC-LICQ
    # Second row: MPEC-MFCQ, MPEC-CRCQ
    # Third row: MPEC-ACQ, MPEC-CPLD
    # Fourth row: MPEC-GCQ (center, receives from ACQ)
    
    nodes = {
        'LICQ':  (5.0, 8.5),
        'MFCQ':  (3.0, 6.5),
        'CRCQ':  (7.0, 6.5),
        'ACQ':   (3.0, 4.5),
        'CPLD':  (7.0, 4.5),
        'GCQ':   (5.0, 2.5),
    }
    
    # Node labels with MPEC prefix
    labels = {
        'LICQ': r'$\mathbf{MPEC\text{-}LICQ}$',
        'MFCQ': r'$\mathbf{MPEC\text{-}MFCQ}$',
        'CRCQ': r'$\mathbf{MPEC\text{-}CRCQ}$',
        'ACQ':  r'$\mathbf{MPEC\text{-}ACQ}$',
        'CPLD': r'$\mathbf{MPEC\text{-}CPLD}$',
        'GCQ':  r'$\mathbf{MPEC\text{-}GCQ}$',
    }
    
    # Full names for subtitle
    full_names = {
        'LICQ': 'Linear Independence CQ',
        'MFCQ': 'Mangasarian-Fromovitz CQ',
        'CRCQ': 'Constant Rank CQ',
        'ACQ':  'Abadie CQ',
        'CPLD': 'Constant Positive Linear Dependence',
        'GCQ':  'Guignard CQ',
    }
    
    # Implications (from → to)
    implications = [
        ('LICQ', 'MFCQ'),
        ('LICQ', 'CRCQ'),
        ('MFCQ', 'ACQ'),
        ('CRCQ', 'CPLD'),
        ('ACQ', 'GCQ'),
        ('CPLD', 'GCQ'),
    ]
    
    # Draw nodes as rounded rectangles
    node_width = 2.2
    node_height = 0.9
    
    for key, (x, y) in nodes.items():
        # Determine node color based on strength
        if key == 'LICQ':
            fill_color = '#bbdefb'  # Stronger blue for strongest CQ
            edge_color = color_strong
        elif key == 'GCQ':
            fill_color = '#eceff1'  # Light gray for weakest CQ
            edge_color = color_weak
        else:
            fill_color = color_node_fill
            edge_color = color_node_edge
        
        # Draw rounded rectangle node
        node_box = FancyBboxPatch(
            (x - node_width/2, y - node_height/2),
            node_width, node_height,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor=fill_color, edgecolor=edge_color,
            linewidth=2, zorder=5
        )
        ax.add_patch(node_box)
        
        # Add label
        ax.text(x, y + 0.05, labels[key], fontsize=12, ha='center', va='center',
                color=color_text, fontweight='bold', zorder=10)
        
        # Add subtitle (full name) below main label
        ax.text(x, y - 0.28, full_names[key], fontsize=8, ha='center', va='center',
                color='#616161', fontstyle='italic', zorder=10)
    
    # Draw implication arrows
    arrow_style = dict(
        arrowstyle='-|>',
        mutation_scale=15,
        lw=1.8,
        color=color_arrow,
        connectionstyle='arc3,rad=0'
    )
    
    for (from_node, to_node) in implications:
        x1, y1 = nodes[from_node]
        x2, y2 = nodes[to_node]
        
        # Calculate arrow start and end points (from node edge to node edge)
        # Direction vector
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        # Normalize
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Offset from node centers to edges
        # For vertical/diagonal arrows, offset based on node dimensions
        if abs(dy_norm) > abs(dx_norm):
            # More vertical - offset from top/bottom
            start_offset = node_height / 2 + 0.05
            end_offset = node_height / 2 + 0.05
        else:
            # More horizontal - offset from sides
            start_offset = node_width / 2 + 0.05
            end_offset = node_width / 2 + 0.05
        
        # Calculate actual start and end
        x1_arrow = x1 + dx_norm * start_offset
        y1_arrow = y1 + dy_norm * start_offset
        x2_arrow = x2 - dx_norm * end_offset
        y2_arrow = y2 - dy_norm * end_offset
        
        arrow = FancyArrowPatch(
            (x1_arrow, y1_arrow),
            (x2_arrow, y2_arrow),
            **arrow_style, zorder=3
        )
        ax.add_patch(arrow)
    
    # Add "implies" symbol annotations on some arrows
    # LICQ → MFCQ
    ax.text(3.7, 7.6, r'$\Rightarrow$', fontsize=10, ha='center', va='center',
            color='#757575', rotation=-30)
    # LICQ → CRCQ
    ax.text(6.3, 7.6, r'$\Rightarrow$', fontsize=10, ha='center', va='center',
            color='#757575', rotation=30)
    
    # =========================================
    # Title
    # =========================================
    ax.text(5.0, 9.3, r'$\mathbf{Hierarchy\ of\ MPEC\ Constraint\ Qualifications}$',
            fontsize=16, ha='center', fontweight='bold', color=color_text)
    
    # =========================================
    # Strength indicator
    # =========================================
    # Add vertical arrow showing "Stronger → Weaker"
    ax.annotate('', xy=(10.0, 3.0), xytext=(10.0, 8.0),
                arrowprops=dict(arrowstyle='-|>', color='#9e9e9e', lw=1.5))
    ax.text(10.0, 8.3, 'Stronger', fontsize=9, ha='center', color='#757575', fontstyle='italic')
    ax.text(10.0, 2.7, 'Weaker', fontsize=9, ha='center', color='#757575', fontstyle='italic')
    
    # =========================================
    # Legend / Key
    # =========================================
    ax.text(0.5, 1.2, r'$A \rightarrow B$: $A$ implies $B$', fontsize=10,
            ha='left', color='#616161',
            bbox=dict(fc='white', ec='#bdbdbd', alpha=0.9, pad=4))
    
    # Branch labels
    ax.text(2.0, 5.5, 'Main\nBranch', fontsize=8, ha='center', color='#1565c0',
            fontstyle='italic', alpha=0.7)
    ax.text(8.0, 5.5, 'Rank\nBranch', fontsize=8, ha='center', color='#1565c0',
            fontstyle='italic', alpha=0.7)
    
    # =========================================
    # Notes
    # =========================================
    note_text = (
        r"All implications are strict in general." + "\n" +
        r"MPEC-LICQ is the strongest; MPEC-GCQ is the weakest."
    )
    ax.text(5.0, 0.5, note_text, fontsize=9, ha='center', color='#757575',
            fontstyle='italic', linespacing=1.5)
    
    plt.tight_layout()
    outname = "mpec_cq_hierarchy.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
