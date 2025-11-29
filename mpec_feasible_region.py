# mpec_feasible_region.py
# Produces a geometric illustration for complementarity feasible set
# Requires: numpy, matplotlib
# Run: python mpec_feasible_region.py
# Output: mpec_feasible_region.png

import numpy as np
import matplotlib.pyplot as plt

def G(x, y):
    # circle-like boundary centered at (0, 0.5)
    return x**2 + (y - 0.5)**2 - 1.0

def H(x, y):
    # upward-opening parabola shifted so H=0 is y = x^2 - 0.2
    return y - (x**2 - 0.2)

def compute_grid(xmin=-1.8, xmax=1.8, ymin=-1.2, ymax=2.0, n=800):
    xs = np.linspace(xmin, xmax, n)
    ys = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(xs, ys)
    Gvals = G(X, Y)
    Hvals = H(X, Y)
    return X, Y, Gvals, Hvals

def main():
    X, Y, Gvals, Hvals = compute_grid()

    # boolean masks for inequality regions
    mask_G_ge0 = (Gvals >= 0)
    mask_H_ge0 = (Hvals >= 0)
    mask_both = mask_G_ge0 & mask_H_ge0

    # tolerance for "on the boundary" selection
    tol = 1e-3
    on_G = np.abs(Gvals) <= tol
    on_H = np.abs(Hvals) <= tol

    # complementarity feasible parts:
    # (G == 0 and H >= 0)  OR  (H == 0 and G >= 0)
    comp_Gpart = on_G & (Hvals >= 0)
    comp_Hpart = on_H & (Gvals >= 0)

    # --- plotting ---
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_xlim(X.min(), X.max())
    ax.set_ylim(Y.min(), Y.max())
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # faint shading of G>=0 (green) and H>=0 (orange)
    ax.contourf(X, Y, mask_G_ge0, levels=[-0.5, 0.5, 1.5],
                colors=["none", "#b2df8a"], alpha=0.25)
    ax.contourf(X, Y, mask_H_ge0, levels=[-0.5, 0.5, 1.5],
                colors=["none", "#fdbf6f"], alpha=0.25)

    # faint shading of intersection region (both >= 0) darker
    ax.contourf(X, Y, mask_both, levels=[-0.5, 0.5, 1.5],
                colors=["none", "#a6cee3"], alpha=0.30)

    # draw contours for G=0 and H=0
    contour_G = ax.contour(X, Y, Gvals, levels=[0], colors=["#1b9e77"], linewidths=2.5)
    contour_H = ax.contour(X, Y, Hvals, levels=[0], colors=["#d95f02"], linewidths=2.5)

    # highlight the complementarity feasible curve segments:
    # we'll plot scatter points where comp_Gpart / comp_Hpart are True
    # sample down points for faster plotting
    step = max(1, int(X.shape[0] / 1200))
    Xs = X[::step, ::step]; Ys = Y[::step, ::step]
    cg = comp_Gpart[::step, ::step]
    ch = comp_Hpart[::step, ::step]

    ax.scatter(Xs[cg], Ys[cg], s=10, color="#006d2c", label=r"$G=0,\ H\geq 0$ (feasible segment)", zorder=5)
    ax.scatter(Xs[ch], Ys[ch], s=10, color="#b30000", label=r"$H=0,\ G\geq 0$ (feasible segment)", zorder=5)

    # Add annotations to explain shape
    ax.text(-1.5, 1.8, r"$G(x,y)=0$ (circle)", color="#1b9e77", fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#1b9e77", alpha=0.9))
    ax.text( 1.05, -0.9, r"$H(x,y)=0$ (parabola)", color="#d95f02", fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#d95f02", alpha=0.9))
    ax.text(0.0, 0.6, "Intersection segments\nselected by complementarity\nform 'faces' (L-shaped)", fontsize=11,
            ha='center', fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="black", linewidth=1.5, alpha=0.9))

    # legend and labels
    ax.legend(loc='upper left', frameon=True, fontsize=11, framealpha=0.95, edgecolor='black')
    ax.set_xlabel("x", fontsize=13, fontweight='bold')
    ax.set_ylabel("y", fontsize=13, fontweight='bold')

    plt.tight_layout()
    outname = "mpec_feasible_region.png"
    fig.savefig(outname, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved figure: {outname}")

if __name__ == "__main__":
    main()
