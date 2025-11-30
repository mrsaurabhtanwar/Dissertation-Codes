# mpec_feasible_region.py
# Produces a geometric illustration for complementarity feasible set
# Requires: numpy, matplotlib
# Run: python mpec_feasible_region.py
# Output: mpec_feasible_region.png

import numpy as np
import matplotlib.pyplot as plt

def G(x, y):
    """Circle-like boundary centered at (0, 0.5)"""
    return x**2 + (y - 0.5)**2 - 1.0

def H(x, y):
    """Upward-opening parabola: H=0 is y = x^2 - 0.2"""
    return y - (x**2 - 0.2)

def compute_grid(xmin=-2.2, xmax=2.2, ymin=-1.5, ymax=2.5, n=1000):
    """
    n controls grid resolution: higher n gives smoother contours but slower computation
    n=1000 is good for publication quality
    """
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
    
    for path in contour_set.get_paths():
        verts = path.vertices
        if len(verts) < 2:
            continue
        
        x_pts = verts[:, 0]
        y_pts = verts[:, 1]
        cond_vals = condition_func(x_pts, y_pts)
        
        # Find where condition is satisfied
        valid = cond_vals >= -1e-6
        
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
    mask_G_ge0 = (Gvals >= 0).astype(float)
    mask_H_ge0 = (Hvals >= 0).astype(float)
    mask_both = mask_G_ge0 * mask_H_ge0

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-1.5, 2.5)
    
    # Subtle grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='gray')

    # Region shading with professional academic colors
    # G >= 0 region (outside circle) - very light blue-gray
    ax.contourf(X, Y, mask_G_ge0, levels=[0.5, 1.5], colors=["#e3f2fd"], alpha=0.7)
    
    # H >= 0 region (above parabola) - very light amber
    ax.contourf(X, Y, mask_H_ge0, levels=[0.5, 1.5], colors=["#fff8e1"], alpha=0.7)
    
    # Intersection region (both >= 0) - clean white
    ax.contourf(X, Y, mask_both, levels=[0.5, 1.5], colors=["white"], alpha=1.0)

    # Draw full constraint boundaries as dashed lines
    ax.contour(X, Y, Gvals, levels=[0], colors=["#1976d2"], linewidths=2.0, 
               alpha=0.5, linestyles='--')
    ax.contour(X, Y, Hvals, levels=[0], colors=["#e64a19"], linewidths=2.0, 
               alpha=0.5, linestyles='--')

    # Extract contour paths for feasible segment highlighting
    contour_G = ax.contour(X, Y, Gvals, levels=[0], colors=["none"], linewidths=0)
    contour_H = ax.contour(X, Y, Hvals, levels=[0], colors=["none"], linewidths=0)

    # Get feasible segments
    G_segments = get_feasible_contour_segments(contour_G, H)  # G=0 where H>=0
    H_segments = get_feasible_contour_segments(contour_H, G)  # H=0 where G>=0

    # Plot feasible segments with bold solid lines
    for i, (xs, ys) in enumerate(G_segments):
        label = r"$G(x,y)=0$ where $H \geq 0$" if i == 0 else None
        ax.plot(xs, ys, color="#0d47a1", linewidth=4.5, label=label, 
                zorder=6, solid_capstyle='round')

    for i, (xs, ys) in enumerate(H_segments):
        label = r"$H(x,y)=0$ where $G \geq 0$" if i == 0 else None
        ax.plot(xs, ys, color="#bf360c", linewidth=4.5, label=label, 
                zorder=6, solid_capstyle='round')

    # Mark the origin
    ax.plot(0, 0, 'ko', markersize=10, zorder=10)
    ax.annotate('Origin (0, 0)', xy=(0, 0), xytext=(0.12, 0.12), fontsize=11,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="black", 
                         linewidth=1.5, alpha=0.95))

    # Annotations for constraints - positioned to avoid overlaps
    ax.text(0.0, 2.3, r"$G(x,y) = x^2 + (y-0.5)^2 - 1$", 
            color="#0d47a1", fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#0d47a1", 
                     linewidth=2, alpha=0.95))
    
    ax.text(0.0, -1.3, r"$H(x,y) = y - x^2 + 0.2$", 
            color="#bf360c", fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#bf360c", 
                     linewidth=2, alpha=0.95))
    
    # Central explanation box
    ax.text(0.0, 0.75, 
            "Complementarity Feasible Set\n" + 
            r"$G(x,y) \cdot H(x,y) = 0$" + "\n" +
            r"$G(x,y) \geq 0,\ H(x,y) \geq 0$",
            fontsize=11, ha='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="#fffde7", ec="#424242", 
                     linewidth=2, alpha=0.95))

    # Legend - positioned in lower right to avoid curve overlap
    ax.legend(loc='lower right', frameon=True, fontsize=10, 
              framealpha=0.95, edgecolor='black', fancybox=True)
    
    # Axis labels
    ax.set_xlabel("x", fontsize=14, fontweight='bold')
    ax.set_ylabel("y", fontsize=14, fontweight='bold')
    ax.tick_params(labelsize=11)

    plt.tight_layout()
    outname = "mpec_feasible_region.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
