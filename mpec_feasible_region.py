# mpec_feasible_region.py
# Geometric illustration for complementarity feasible set
# Example: Parabola vs Circle
#   G(x,y) = y + x^2 - 1  (G >= 0 means above the parabola y = 1 - x^2)
#   H(x,y) = x^2 + (y-1)^2 - 1  (H >= 0 means outside/on the circle centered at (0,1) with radius 1)
# Complementarity: G >= 0, H >= 0, G·H = 0
# Requires: numpy, matplotlib
# Output: mpec_feasible_region.png

import numpy as np
import matplotlib.pyplot as plt

def G(x, y):
    """Parabola boundary: G=0 is y = 1 - x^2
       G >= 0 means points ABOVE the parabola (y >= 1 - x^2)
    """
    return y + x**2 - 1

def H(x, y):
    """Circle boundary centered at (0, 1) with radius 1: H=0 is x^2 + (y-1)^2 = 1
       H >= 0 means points OUTSIDE or ON the circle (x^2 + (y-1)^2 >= 1)
    """
    return x**2 + (y - 1)**2 - 1

def compute_grid(xmin=-2.0, xmax=2.0, ymin=-1.5, ymax=2.5, n=1000):
    xs = np.linspace(xmin, xmax, n)
    ys = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(xs, ys)
    Gvals = G(X, Y)
    Hvals = H(X, Y)
    return X, Y, Gvals, Hvals

def get_feasible_contour_segments(contour_set, condition_func):
    """
    Extract contour paths and filter to segments where condition_func(x,y) >= 0.
    Returns list of (x_array, y_array) tuples.
    """
    segments = []
    threshold = 0.01  # Small positive threshold to avoid numerical issues at boundaries
    
    for path in contour_set.get_paths():
        verts = path.vertices
        if len(verts) < 2:
            continue
        
        x_pts = verts[:, 0]
        y_pts = verts[:, 1]
        cond_vals = condition_func(x_pts, y_pts)
        
        # Find where condition is satisfied (strictly inside feasible region)
        valid = cond_vals >= threshold
        
        # Split into continuous valid segments
        in_segment = False
        seg_x, seg_y = [], []
        
        for i in range(len(x_pts)):
            if valid[i]:
                seg_x.append(x_pts[i])
                seg_y.append(y_pts[i])
                in_segment = True
            else:
                if in_segment and len(seg_x) > 1:
                    segments.append((np.array(seg_x), np.array(seg_y)))
                seg_x, seg_y = [], []
                in_segment = False
        
        # Don't forget last segment
        if in_segment and len(seg_x) > 1:
            segments.append((np.array(seg_x), np.array(seg_y)))
    
    return segments

def main():
    X, Y, Gvals, Hvals = compute_grid()

    # Boolean masks for inequality regions
    mask_G_ge0 = (Gvals >= 0).astype(float)  # Above parabola
    mask_H_ge0 = (Hvals >= 0).astype(float)  # Outside circle
    mask_both = mask_G_ge0 * mask_H_ge0

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(12, 11))
    ax.set_aspect('equal')
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-1.8, 2.8)
    
    # Subtle grid
    ax.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='gray')

    # Region shading with professional academic colors
    # Layer 1: Base background
    ax.set_facecolor('#fafafa')
    
    # Layer 2: H >= 0 region (outside circle) - light amber/orange
    ax.contourf(X, Y, mask_H_ge0, levels=[0.5, 1.5], colors=["#fff3e0"], alpha=0.8)
    
    # Layer 3: G >= 0 region (above parabola) - light blue  
    ax.contourf(X, Y, mask_G_ge0, levels=[0.5, 1.5], colors=["#e3f2fd"], alpha=0.6)
    
    # Layer 4: Intersection region (both >= 0) - light green
    ax.contourf(X, Y, mask_both, levels=[0.5, 1.5], colors=["#c8e6c9"], alpha=0.7)
    
    # Layer 5: Inside circle (H < 0) - white to show it's excluded from H>=0
    mask_H_lt0 = (Hvals < 0).astype(float)
    ax.contourf(X, Y, mask_H_lt0, levels=[0.5, 1.5], colors=["white"], alpha=1.0)

    # Draw full constraint boundaries as dashed lines
    ax.contour(X, Y, Gvals, levels=[0], colors=["#1976d2"], linewidths=2.0, 
               alpha=0.5, linestyles='--')
    ax.contour(X, Y, Hvals, levels=[0], colors=["#e64a19"], linewidths=2.0, 
               alpha=0.5, linestyles='--')

    # Extract contour paths for feasible segment highlighting
    contour_G = ax.contour(X, Y, Gvals, levels=[0], colors=["none"], linewidths=0)
    contour_H = ax.contour(X, Y, Hvals, levels=[0], colors=["none"], linewidths=0)

    # Get feasible segments
    # G=0 (parabola) where H>=0 (outside circle) - the "wings" of parabola
    G_segments = get_feasible_contour_segments(contour_G, H)
    # H=0 (circle) where G>=0 (above parabola) - upper arc of circle only
    H_segments = get_feasible_contour_segments(contour_H, G)

    # Plot feasible segments with bold solid lines
    for i, (xs, ys) in enumerate(G_segments):
        label = r"$G=0$ where $H \geq 0$ (parabola arc)" if i == 0 else None
        ax.plot(xs, ys, color="#0d47a1", linewidth=4.5, label=label, 
                zorder=6, solid_capstyle='round')

    for i, (xs, ys) in enumerate(H_segments):
        label = r"$H=0$ where $G \geq 0$ (circle arc)" if i == 0 else None
        ax.plot(xs, ys, color="#bf360c", linewidth=4.5, label=label, 
                zorder=6, solid_capstyle='round')

    # =========================================
    # Mark the intersection points
    # =========================================
    # From the analysis: t = (sqrt(5) - 1)/2 ≈ 0.618034
    # x = ±sqrt(t) ≈ ±0.786151
    # y = 1 - t = (3 - sqrt(5))/2 ≈ 0.381966
    t = (np.sqrt(5) - 1) / 2
    x_int = np.sqrt(t)
    y_int = 1 - t
    
    # Plot intersection points
    ax.plot(x_int, y_int, 'ko', markersize=12, zorder=15)
    ax.plot(-x_int, y_int, 'ko', markersize=12, zorder=15)
    
    # White fill for visibility
    ax.plot(x_int, y_int, 'o', color='white', markersize=8, zorder=14)
    ax.plot(-x_int, y_int, 'o', color='white', markersize=8, zorder=14)
    
    # Annotate intersection points
    ax.annotate(f'$({x_int:.3f},\\, {y_int:.3f})$', 
                xy=(x_int, y_int), xytext=(x_int + 0.35, y_int - 0.35), 
                fontsize=10, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#424242', lw=1.5),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#424242", 
                         linewidth=1.5, alpha=0.95))
    
    ax.annotate(f'$({-x_int:.3f},\\, {y_int:.3f})$', 
                xy=(-x_int, y_int), xytext=(-x_int - 0.35, y_int - 0.35), 
                fontsize=10, fontweight='bold', ha='right',
                arrowprops=dict(arrowstyle='->', color='#424242', lw=1.5),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#424242", 
                         linewidth=1.5, alpha=0.95))

    # =========================================
    # Region labels - positioned in corners
    # =========================================
    # Label for G >= 0 region (top-left corner)
    ax.text(-2.1, 2.5, r"$G \geq 0$" + "\n" + r"(above parabola)", 
            color="#1565c0", fontsize=10, fontweight='bold', ha='left', va='top',
            bbox=dict(boxstyle="round,pad=0.4", fc="#e3f2fd", ec="#1565c0", 
                     linewidth=1.5, alpha=0.95))
    
    # Label for H >= 0 region (bottom-right corner)
    ax.text(2.1, -1.5, r"$H \geq 0$" + "\n" + r"(outside circle)", 
            color="#e65100", fontsize=10, fontweight='bold', ha='right', va='bottom',
            bbox=dict(boxstyle="round,pad=0.4", fc="#fff3e0", ec="#e65100", 
                     linewidth=1.5, alpha=0.95))

    # =========================================
    # Constraint equation labels
    # =========================================
    ax.text(0.0, -1.55, r"$G(x,y) = y + x^2 - 1$  (Parabola: $y = 1 - x^2$)", 
            color="#0d47a1", fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#0d47a1", 
                     linewidth=1.5, alpha=0.95))
    
    ax.text(0.0, 2.25, r"$H(x,y) = x^2 + (y-1)^2 - 1$  (Circle: center $(0,1)$, $r=1$)", 
            color="#bf360c", fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#bf360c", 
                     linewidth=1.5, alpha=0.95))
    
    # =========================================
    # Central complementarity condition box - positioned at top center
    # =========================================
    ax.text(0.0, 2.55, 
            r"$\mathbf{Complementarity\ Feasible\ Set:}\ \ 0 \leq G \perp H \geq 0$",
            fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", fc="#fffde7", ec="#424242", 
                     linewidth=2, alpha=0.95))

    # =========================================
    # Mark center of circle
    # =========================================
    ax.plot(0, 1, 'o', color='#bf360c', markersize=8, zorder=12)
    ax.plot(0, 1, 'o', color='white', markersize=4, zorder=13)
    ax.text(0.12, 0.88, r'$(0,1)$', fontsize=9, color='#bf360c', fontweight='bold')

    # =========================================
    # Legend - positioned in lower left
    # =========================================
    ax.legend(loc='lower left', frameon=True, fontsize=9, 
              framealpha=0.95, edgecolor='black', fancybox=True)
    
    # Axis labels
    ax.set_xlabel("$x$", fontsize=14, fontweight='bold')
    ax.set_ylabel("$y$", fontsize=14, fontweight='bold')
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    outname = "mpec_feasible_region.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
