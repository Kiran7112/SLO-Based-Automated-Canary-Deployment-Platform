#!/usr/bin/env python3
"""Generate realistic, assumed-output screenshots for the SLO Canary platform.

The platform cannot be run on this machine (no Docker/Kubernetes), so these
images depict what the live tooling *would* show. Every image shares one dark,
branded theme (header band + footer + palette + fonts) so the set reads as a
single project, while the panel content is drawn to resemble the real tools:
Argo Rollouts CLI, Grafana, GitHub Actions, ArgoCD, Alertmanager/Slack.

Output: docs/images/*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

# --------------------------------------------------------------------------- #
# Shared theme — keep identical across every figure.
# --------------------------------------------------------------------------- #
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "images")

BG          = "#0d1117"   # canvas / app background (GitHub/Grafana dark)
PANEL       = "#161b22"   # panel surface
PANEL_HEAD  = "#1c2230"   # panel title strip
GRID        = "#27313f"
BORDER      = "#30363d"
BRAND       = "#0b3d91"   # deep blue header band (from the doc)
BRAND2      = "#11519c"
TEXT        = "#e6edf3"
MUTED       = "#8b949e"
BLUE        = "#2f81f7"
GREEN       = "#3fb950"
RED         = "#f85149"
AMBER       = "#d29922"
PURPLE      = "#a371f7"
CYAN        = "#39c5cf"

MONO = "DejaVu Sans Mono"
SANS = "DejaVu Sans"

FIG_W, FIG_H, DPI = 16, 10, 110          # identical canvas for the whole set
PROJECT = "SLO-Based Automated Canary Deployment Platform"


def base_canvas(image_label):
    """Create the shared branded canvas and return (fig, ax) in a 0..160 x 0..100 space."""
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.set_facecolor(BG)

    # Header band ---------------------------------------------------------- #
    ax.add_patch(Rectangle((0, 92), 160, 8, color=BRAND, zorder=2))
    ax.add_patch(Rectangle((0, 92), 160, 0.35, color=CYAN, zorder=3))
    # Logo mark: a target/canary ring.
    ax.add_patch(Circle((4.2, 96), 1.9, color="white", zorder=4, fill=False, lw=2.2))
    ax.add_patch(Circle((4.2, 96), 0.7, color=CYAN, zorder=4))
    ax.text(8, 96.7, PROJECT, color="white", fontsize=15, fontweight="bold",
            va="center", ha="left", family=SANS, zorder=4)
    ax.text(8, 94.2, "DevOps · Progressive Delivery · SRE", color="#cfe0ff",
            fontsize=9.5, va="center", ha="left", family=SANS, zorder=4)
    ax.text(156, 96, image_label, color="white", fontsize=11, fontweight="bold",
            va="center", ha="right", family=SANS, zorder=4)

    # Footer band ---------------------------------------------------------- #
    ax.add_patch(Rectangle((0, 0), 160, 4, color="#0a0d12", zorder=2))
    ax.add_patch(Rectangle((0, 4), 160, 0.2, color=BORDER, zorder=2))
    ax.text(2, 2, "Assumed / illustrative output — generated mock of live tooling",
            color=MUTED, fontsize=8.5, va="center", ha="left", family=SANS, zorder=3)
    ax.text(158, 2, "Kubernetes · Argo Rollouts · ArgoCD · Prometheus · Grafana",
            color=MUTED, fontsize=8.5, va="center", ha="right", family=SANS, zorder=3)
    return fig, ax


def panel(ax, x, y, w, h, title=None, icon_color=BLUE):
    """Draw a rounded dark panel; return the inner content box (x0,y0,x1,y1)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.7",
                                fc=PANEL, ec=BORDER, lw=1.2, zorder=3))
    if title is not None:
        ax.add_patch(Rectangle((x, y + h - 3), w, 3, color=PANEL_HEAD, zorder=3.5))
        ax.add_patch(Circle((x + 1.3, y + h - 1.5), 0.45, color=icon_color, zorder=4))
        ax.text(x + 2.4, y + h - 1.5, title, color=TEXT, fontsize=10.5,
                fontweight="bold", va="center", ha="left", family=SANS, zorder=4)
        return (x + 1.5, y + 1.5, x + w - 1.5, y + h - 4)
    return (x + 1.5, y + 1.5, x + w - 1.5, y + h - 1.5)


def status_pill(ax, x, y, text, color, w=None):
    w = w if w else 0.9 + 0.62 * len(text)
    ax.add_patch(FancyBboxPatch((x, y - 1.05), w, 2.1,
                                boxstyle="round,pad=0,rounding_size=1.05",
                                fc=color, ec="none", alpha=0.18, zorder=5))
    ax.add_patch(Circle((x + 1, y), 0.42, color=color, zorder=6))
    ax.text(x + 1.9, y, text, color=color, fontsize=9.5, fontweight="bold",
            va="center", ha="left", family=SANS, zorder=6)
    return w


def save(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.normpath(os.path.join(OUT_DIR, name))
    fig.savefig(path, facecolor=BG, dpi=DPI)
    plt.close(fig)
    print("wrote", path)


# --------------------------------------------------------------------------- #
# 1. Argo Rollouts CLI — healthy, fully promoted.
# --------------------------------------------------------------------------- #
def img_rollouts_cli():
    fig, ax = base_canvas("1 · Argo Rollouts — promote")
    inner = panel(ax, 6, 8, 148, 80, None)
    x0, y0, x1, y1 = 6, 8, 154, 88
    # terminal title bar
    ax.add_patch(Rectangle((x0, y1 - 3.2), x1 - x0, 3.2, color="#1c2230", zorder=4))
    for i, c in enumerate([RED, AMBER, GREEN]):
        ax.add_patch(Circle((x0 + 1.6 + i * 1.4, y1 - 1.6), 0.45, color=c, zorder=5))
    ax.text((x0 + x1) / 2, y1 - 1.6, "checkout@sre — kubectl argo rollouts get rollout checkout --watch",
            color=MUTED, fontsize=9.5, va="center", ha="center", family=MONO, zorder=5)

    lines = [
        ("$ kubectl argo rollouts get rollout checkout", TEXT, False),
        ("", TEXT, False),
        ("Name:            checkout", TEXT, False),
        ("Namespace:       checkout", TEXT, False),
        ("Status:          ✔ Healthy", GREEN, True),
        ("Strategy:        Canary", TEXT, False),
        ("  Step:          8/8", TEXT, False),
        ("  SetWeight:     100", TEXT, False),
        ("  ActualWeight:  100", TEXT, False),
        ("Images:          checkout:v2.3.0 (stable)", CYAN, False),
        ("Replicas:        Desired 4 | Updated 4 | Ready 4 | Available 4", TEXT, False),
        ("", TEXT, False),
        ("NAME                                   KIND         STATUS        AGE   INFO", MUTED, False),
        ("↻ checkout                             Rollout      ✔ Healthy     9d", GREEN, False),
        ("├──# revision:12", MUTED, False),
        ("│  └──■ checkout-846f (stable)           ReplicaSet   ✔ Healthy     7m    stable", GREEN, False),
        ("│     ├──□ checkout-846f-2xk9             Pod          ✔ Running     7m    ready:1/1", GREEN, False),
        ("│     ├──□ checkout-846f-7pq4             Pod          ✔ Running     7m    ready:1/1", GREEN, False),
        ("│     ├──□ checkout-846f-bf31             Pod          ✔ Running     7m    ready:1/1", GREEN, False),
        ("│     └──□ checkout-846f-q8mz             Pod          ✔ Running     7m    ready:1/1", GREEN, False),
        ("└──# revision:11", MUTED, False),
        ("   └──■ checkout-7d9f                    ReplicaSet   • ScaledDown   9d", MUTED, False),
        ("", TEXT, False),
        ("✔ AnalysisRun checkout-12-1  error-rate=0.31%  p99=212ms  payment=99.7%  → Successful", GREEN, True),
    ]
    yy = y1 - 5
    for txt, col, bold in lines:
        ax.text(x0 + 2, yy, txt, color=col, fontsize=9.2,
                fontweight="bold" if bold else "normal",
                va="center", ha="left", family=MONO, zorder=5)
        yy -= 3.05
    save(fig, "01_argo_rollouts_status.png")


# --------------------------------------------------------------------------- #
# helper: grafana-style timeseries inside a content box
# --------------------------------------------------------------------------- #
def _ts_axes(fig, box):
    x0, y0, x1, y1 = box
    axx = fig.add_axes([x0 / 160, y0 / 100, (x1 - x0) / 160, (y1 - y0) / 100])
    axx.set_facecolor(PANEL)
    for s in axx.spines.values():
        s.set_color(BORDER)
    axx.tick_params(colors=MUTED, labelsize=7.5)
    axx.grid(color=GRID, lw=0.6)
    return axx


# --------------------------------------------------------------------------- #
# 2. Grafana SLO dashboard — healthy canary vs stable.
# --------------------------------------------------------------------------- #
def img_grafana_dashboard():
    fig, ax = base_canvas("2 · Grafana — SLO dashboard")
    # Grafana sub-navbar
    ax.add_patch(Rectangle((0, 88), 160, 4, color="#181b1f", zorder=2))
    ax.text(2.5, 90, "▤  Checkout — Canary vs Stable (SLO)", color=TEXT,
            fontsize=11, fontweight="bold", va="center", family=SANS, zorder=3)
    ax.text(157.5, 90, "Last 15 minutes  ⟳ 10s", color=MUTED, fontsize=9,
            va="center", ha="right", family=SANS, zorder=3)

    t = np.linspace(0, 15, 200)
    rng = np.random.default_rng(7)

    # Panel A: error rate
    boxA = panel(ax, 4, 47, 75, 38, "5xx Error Rate  (SLO < 1%)", GREEN)
    axA = _ts_axes(fig, boxA)
    stable = 0.18 + 0.05 * np.sin(t) + rng.normal(0, 0.02, t.size)
    canary = 0.30 + 0.07 * np.sin(t + 1) + rng.normal(0, 0.03, t.size)
    axA.axhline(1.0, color=RED, lw=1.3, ls="--")
    axA.text(0.2, 1.05, "SLO 1%", color=RED, fontsize=7)
    axA.plot(t, stable.clip(0), color=BLUE, lw=1.8, label="stable")
    axA.plot(t, canary.clip(0), color=GREEN, lw=1.8, label="canary")
    axA.fill_between(t, canary.clip(0), color=GREEN, alpha=0.12)
    axA.set_ylim(0, 1.3); axA.set_xlim(0, 15)
    axA.set_yticks([0, 0.5, 1.0]); axA.set_yticklabels(["0%", "0.5%", "1%"])
    axA.legend(loc="upper left", fontsize=7, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

    # Panel B: latency
    boxB = panel(ax, 82, 47, 74, 38, "p99 Latency  (SLO < 500ms)", GREEN)
    axB = _ts_axes(fig, boxB)
    sl = 175 + 18 * np.sin(t * 0.8) + rng.normal(0, 6, t.size)
    cl = 205 + 22 * np.sin(t * 0.8 + 1) + rng.normal(0, 8, t.size)
    axB.axhline(500, color=RED, lw=1.3, ls="--")
    axB.text(0.2, 510, "SLO 500ms", color=RED, fontsize=7)
    axB.plot(t, sl, color=BLUE, lw=1.8, label="stable")
    axB.plot(t, cl, color=GREEN, lw=1.8, label="canary")
    axB.set_ylim(0, 600); axB.set_xlim(0, 15)
    axB.set_yticks([0, 250, 500]); axB.set_yticklabels(["0", "250ms", "500ms"])
    axB.legend(loc="upper left", fontsize=7, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

    # Panel C: payment success stat
    boxC = panel(ax, 4, 8, 36, 36, "Payment Success  (SLO ≥ 99%)", GREEN)
    ax.text(22, 28, "99.7%", color=GREEN, fontsize=30, fontweight="bold",
            va="center", ha="center", family=SANS, zorder=5)
    ax.text(22, 18, "baseline 99.8%", color=MUTED, fontsize=9,
            va="center", ha="center", family=SANS, zorder=5)
    status_pill(ax, 13, 13, "MEETING SLO", GREEN)

    # Panel D: canary weight progression (stacked step)
    boxD = panel(ax, 43, 8, 49, 36, "Canary Traffic Weight", BLUE)
    axD = _ts_axes(fig, boxD)
    steps_t = [0, 3, 3, 6, 6, 9, 9, 12, 12, 15]
    steps_w = [5, 5, 25, 25, 50, 50, 100, 100, 100, 100]
    axD.step(steps_t, steps_w, where="post", color=BLUE, lw=2.2)
    axD.fill_between(steps_t, steps_w, step="post", color=BLUE, alpha=0.15)
    axD.set_ylim(0, 110); axD.set_xlim(0, 15)
    axD.set_yticks([5, 25, 50, 100]); axD.set_yticklabels(["5%", "25%", "50%", "100%"])

    # Panel E: CPU stat
    boxE = panel(ax, 95, 8, 61, 36, "CPU Saturation  (pause > 80%)", AMBER)
    axE = _ts_axes(fig, boxE)
    cpu_s = 41 + 6 * np.sin(t) + rng.normal(0, 2, t.size)
    cpu_c = 47 + 7 * np.sin(t + 0.6) + rng.normal(0, 2.5, t.size)
    axE.axhline(80, color=AMBER, lw=1.3, ls="--")
    axE.text(0.2, 82, "pause 80%", color=AMBER, fontsize=7)
    axE.plot(t, cpu_s, color=BLUE, lw=1.8, label="stable")
    axE.plot(t, cpu_c, color=GREEN, lw=1.8, label="canary")
    axE.set_ylim(0, 100); axE.set_xlim(0, 15)
    axE.set_yticks([0, 40, 80]); axE.set_yticklabels(["0%", "40%", "80%"])
    axE.legend(loc="upper left", fontsize=7, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

    save(fig, "02_grafana_slo_dashboard.png")


# --------------------------------------------------------------------------- #
# 3. Automatic rollback — error spike + Slack alert.
# --------------------------------------------------------------------------- #
def img_rollback():
    fig, ax = base_canvas("3 · Automatic rollback")
    ax.add_patch(Rectangle((0, 88), 160, 4, color="#181b1f", zorder=2))
    ax.text(2.5, 90, "▤  Checkout — Incident: canary auto-rollback", color=TEXT,
            fontsize=11, fontweight="bold", va="center", family=SANS, zorder=3)

    t = np.linspace(0, 12, 200)
    rng = np.random.default_rng(3)

    # Left: error-rate spike crossing SLO
    boxA = panel(ax, 4, 47, 92, 38, "5xx Error Rate — canary breaches SLO", RED)
    axA = _ts_axes(fig, boxA)
    err = 0.3 + rng.normal(0, 0.03, t.size)
    spike = np.where(t > 6, (t - 6) * 1.8, 0)
    canary = (err + spike).clip(0)
    axA.axhline(1.0, color=RED, lw=1.3, ls="--"); axA.text(0.2, 1.15, "SLO 1%", color=RED, fontsize=7)
    axA.plot(t, 0.2 + rng.normal(0, 0.02, t.size), color=BLUE, lw=1.8, label="stable")
    axA.plot(t, canary, color=RED, lw=2.0, label="canary")
    axA.fill_between(t, canary, where=(canary > 1.0), color=RED, alpha=0.18)
    axA.axvline(6, color=AMBER, lw=1.2, ls=":")
    axA.annotate("rollback fired", xy=(6, 5.5), xytext=(7, 6.5), color=AMBER, fontsize=7.5,
                 arrowprops=dict(arrowstyle="->", color=AMBER))
    axA.set_ylim(0, 7); axA.set_xlim(0, 12)
    axA.set_yticks([0, 1, 3, 5]); axA.set_yticklabels(["0%", "1%", "3%", "5%"])
    axA.legend(loc="upper left", fontsize=7, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

    # Left-lower: traffic weight snapping to 0
    boxB = panel(ax, 4, 8, 92, 36, "Canary Traffic Weight — snapped back to 0%", BLUE)
    axB = _ts_axes(fig, boxB)
    wt_t = [0, 3, 3, 6, 6, 6.2, 12]
    wt_w = [5, 5, 25, 25, 25, 0, 0]
    axB.step(wt_t, wt_w, where="post", color=BLUE, lw=2.2)
    axB.fill_between(wt_t, wt_w, step="post", color=BLUE, alpha=0.15)
    axB.axvline(6, color=AMBER, lw=1.2, ls=":")
    axB.set_ylim(0, 60); axB.set_xlim(0, 12)
    axB.set_yticks([0, 25, 50]); axB.set_yticklabels(["0%", "25%", "50%"])

    # Right: Slack alert card
    bx, by, bw, bh = 100, 8, 56, 77
    panel(ax, bx, by, bw, bh, "#sre-oncall", PURPLE)
    ax.add_patch(FancyBboxPatch((bx + 2, by + bh - 24), bw - 4, 18,
                 boxstyle="round,pad=0,rounding_size=0.6", fc="#1f2530", ec=RED, lw=1.4, zorder=5))
    ax.add_patch(Rectangle((bx + 2, by + bh - 24), 0.7, 18, color=RED, zorder=6))
    ax.add_patch(Circle((bx + 5.5, by + bh - 9), 1.3, color=RED, zorder=6))
    ax.text(bx + 5.5, by + bh - 9, "!", color="white", fontsize=12, fontweight="bold",
            va="center", ha="center", zorder=7)
    ax.text(bx + 8, by + bh - 8, "Prometheus Alertmanager", color=TEXT, fontsize=9.5,
            fontweight="bold", va="center", ha="left", family=SANS, zorder=7)
    ax.text(bx + 8, by + bh - 10.6, "APP  10:42", color=MUTED, fontsize=7.5,
            va="center", ha="left", family=SANS, zorder=7)
    msg = [
        ("● [FIRING] CheckoutErrorRateHigh", RED, True),
        ("slo: error_rate   severity: critical", MUTED, False),
        ("Error rate 6.1% exceeds the 1% SLO.", TEXT, False),
        ("Canary v2.4.0 aborted; traffic shifted", TEXT, False),
        ("back to stable v2.3.0.", TEXT, False),
    ]
    yy = by + bh - 13.5
    for txt, col, bold in msg:
        ax.text(bx + 5, yy, txt, color=col, fontsize=8.3,
                fontweight="bold" if bold else "normal", va="center", ha="left",
                family=MONO, zorder=7)
        yy -= 2.4

    # Rollouts event line + resolution
    ax.text(bx + 4, by + 26, "Argo Rollouts events", color=TEXT, fontsize=9,
            fontweight="bold", va="center", ha="left", family=SANS, zorder=6)
    events = [
        ("10:42:03  RolloutAborted", RED),
        ("10:42:03  ScaleDownCanary  25→0%", AMBER),
        ("10:42:05  AnalysisRun Failed", RED),
        ("10:42:06  Status: Degraded", RED),
        ("10:42:31  ✔ Stable serving 100%", GREEN),
    ]
    yy = by + 22.5
    for txt, col in events:
        ax.text(bx + 4, yy, txt, color=col, fontsize=8.2, va="center", ha="left",
                family=MONO, zorder=6)
        yy -= 3.0
    save(fig, "03_automatic_rollback.png")


# --------------------------------------------------------------------------- #
# 4. GitHub Actions — CI run.
# --------------------------------------------------------------------------- #
def img_github_actions():
    fig, ax = base_canvas("4 · GitHub Actions — CI")
    ax.add_patch(Rectangle((0, 88), 160, 4, color="#161b22", zorder=2))
    ax.text(2.5, 90, "example/slo-canary-platform   •   ci  #128", color=TEXT,
            fontsize=11, fontweight="bold", va="center", family=SANS, zorder=3)

    # summary banner
    ax.add_patch(FancyBboxPatch((4, 79, ), 152, 6, boxstyle="round,pad=0,rounding_size=0.6",
                 fc="#12261a", ec=GREEN, lw=1.3, zorder=3))
    ax.add_patch(Circle((7, 82), 1.3, color=GREEN, zorder=4))
    ax.text(7, 82, "✔", color="white", fontsize=11, fontweight="bold", va="center", ha="center", zorder=5)
    ax.text(10, 82.7, "All checks have passed", color=TEXT, fontsize=11, fontweight="bold",
            va="center", ha="left", family=SANS, zorder=4)
    ax.text(10, 80.6, "4 successful checks  ·  release v2.3.0  ·  pushed by ci-bot", color=MUTED,
            fontsize=8.5, va="center", ha="left", family=SANS, zorder=4)

    # left job list
    panel(ax, 4, 8, 40, 68, "Jobs", BLUE)
    jobs = ["Build & unit test", "Trivy image scan", "Push & sign image", "Bump GitOps manifest"]
    times = ["38s", "1m 12s", "54s", "9s"]
    yy = 70
    for j, tm in zip(jobs, times):
        ax.add_patch(Circle((7, yy), 1.1, color=GREEN, zorder=5))
        ax.text(7, yy, "✔", color="white", fontsize=8, fontweight="bold", va="center", ha="center", zorder=6)
        ax.text(9.5, yy + 0.4, j, color=TEXT, fontsize=9.3, va="center", ha="left", family=SANS, zorder=5)
        ax.text(9.5, yy - 1.6, tm, color=MUTED, fontsize=8, va="center", ha="left", family=SANS, zorder=5)
        yy -= 7.5

    # main: step log of selected job
    panel(ax, 47, 8, 109, 68, "Trivy image scan  ·  ubuntu-latest", GREEN)
    steps = [
        ("✔ Set up job", GREEN, "2s"),
        ("✔ Checkout repository", GREEN, "3s"),
        ("✔ Build image (local, for scanning)", GREEN, "41s"),
        ("✔ Trivy vulnerability scan", GREEN, "26s"),
        ("", TEXT, ""),
        ("   checkout:5e1c9a   (alpine 3.20, distroless)", MUTED, ""),
        ("   Total: 0 (UNKNOWN: 0  LOW: 4  MEDIUM: 1  HIGH: 0  CRITICAL: 0)", TEXT, ""),
        ("   ✔ No fixable HIGH/CRITICAL vulnerabilities — gate passed", GREEN, ""),
        ("", TEXT, ""),
        ("✔ Push & sign image (cosign keyless)", GREEN, "54s"),
        ("   pushed ghcr.io/example/.../checkout:v2.3.0", MUTED, ""),
        ("   ✔ cosign signature uploaded (sigstore)", GREEN, ""),
        ("✔ Bump GitOps manifest → ArgoCD will sync", GREEN, "9s"),
        ("✔ Complete job", GREEN, "1s"),
    ]
    yy = 71
    for txt, col, tm in steps:
        if txt:
            ax.text(49.5, yy, txt, color=col, fontsize=9.0, va="center", ha="left",
                    family=MONO, zorder=5)
            if tm:
                ax.text(154, yy, tm, color=MUTED, fontsize=8, va="center", ha="right",
                        family=MONO, zorder=5)
        yy -= 4.3
    save(fig, "04_github_actions_ci.png")


# --------------------------------------------------------------------------- #
# 5. ArgoCD — application view (synced + healthy resource tree).
# --------------------------------------------------------------------------- #
def img_argocd():
    fig, ax = base_canvas("5 · ArgoCD — GitOps")
    ax.add_patch(Rectangle((0, 88), 160, 4, color="#181b1f", zorder=2))
    ax.text(2.5, 90, "Applications  /  checkout", color=TEXT, fontsize=11,
            fontweight="bold", va="center", family=SANS, zorder=3)

    # app summary bar with pills
    panel(ax, 4, 78, 152, 7, None)
    ax.text(7, 81.5, "checkout", color=TEXT, fontsize=12, fontweight="bold",
            va="center", ha="left", family=SANS, zorder=5)
    px = 28
    px += status_pill(ax, px, 81.5, "Synced", GREEN) + 3
    px += status_pill(ax, px, 81.5, "Healthy", GREEN) + 3
    ax.text(155, 82.4, "repo: github.com/example/slo-canary-platform", color=MUTED,
            fontsize=8.2, va="center", ha="right", family=MONO, zorder=5)
    ax.text(155, 80.2, "path: deploy/k8s   target: main   auto-sync ✔  self-heal ✔",
            color=MUTED, fontsize=8.2, va="center", ha="right", family=MONO, zorder=5)

    # resource tree as connected node cards
    panel(ax, 4, 8, 152, 67, "Resource Tree", BLUE)

    def node(cx, cy, kind, name, color=GREEN, w=26):
        ax.add_patch(FancyBboxPatch((cx, cy - 2.6), w, 5.2,
                     boxstyle="round,pad=0,rounding_size=0.5", fc="#1b212b",
                     ec=BORDER, lw=1.1, zorder=6))
        ax.add_patch(Circle((cx + 2, cy + 0.9), 0.55, color=color, zorder=7))
        ax.text(cx + 3.6, cy + 1.0, kind, color=MUTED, fontsize=7.3, va="center",
                ha="left", family=SANS, zorder=7)
        ax.text(cx + 2, cy - 1.2, name, color=TEXT, fontsize=8.6, fontweight="bold",
                va="center", ha="left", family=MONO, zorder=7)
        return (cx, cy, w)

    def link(a, b):
        ax.add_patch(FancyArrowPatch((a[0] + a[2], a[1]), (b[0], b[1]),
                     connectionstyle="arc3,rad=0", arrowstyle="-", color=BORDER,
                     lw=1.2, zorder=5))

    app = node(8, 41, "Application", "checkout", GREEN)
    roll = node(40, 41, "Rollout", "checkout", GREEN)
    link(app, roll)
    rs_new = node(72, 58, "ReplicaSet", "checkout-846f", GREEN)
    rs_old = node(72, 24, "ReplicaSet", "checkout-7d9f", MUTED)
    svc = node(72, 41, "Service", "checkout-stable", GREEN)
    link(roll, rs_new); link(roll, rs_old); link(roll, svc)
    pods_y = [66, 60, 54, 48]
    for i, py in enumerate(pods_y):
        p = node(104, py, "Pod", f"846f-{['2xk9','7pq4','bf31','q8mz'][i]}", GREEN, w=22)
        link(rs_new, p)
    ana = node(104, 41, "AnalysisRun", "checkout-12-1", GREEN, w=24)
    link(svc, ana)
    ing = node(104, 30, "Ingress", "checkout", GREEN, w=22)
    link(svc, ing)
    # analysis result note (footnote inside the tree panel)
    ax.text(8, 13, "✔ SLO gate (AnalysisRun checkout-12-1): error 0.31% · p99 212ms · payment 99.7% — all within SLO",
            color=GREEN, fontsize=8.6, va="center", ha="left", family=MONO, zorder=7)
    save(fig, "05_argocd_application.png")


# --------------------------------------------------------------------------- #
# 6. Canary promotion timeline.
# --------------------------------------------------------------------------- #
def img_promotion_timeline():
    fig, ax = base_canvas("6 · Canary promotion timeline")
    panel(ax, 6, 40, 148, 46, "Progressive promotion  5% → 25% → 50% → 100%", BLUE)

    stages = [("5%", "10:18"), ("25%", "10:20"), ("50%", "10:22"), ("100%", "10:24")]
    xs = [26, 60, 94, 128]
    base_y = 58
    # connecting rail
    ax.add_patch(Rectangle((20, base_y - 0.4), 116, 0.8, color=BORDER, zorder=3))
    for i, ((label, ts), x) in enumerate(zip(stages, xs)):
        ax.add_patch(Circle((x, base_y), 5.4, color=PANEL, ec=GREEN, lw=2.4, zorder=4))
        ax.text(x, base_y + 0.4, label, color=TEXT, fontsize=13, fontweight="bold",
                va="center", ha="center", family=SANS, zorder=5)
        ax.text(x, base_y - 8.5, ts, color=MUTED, fontsize=9, va="center", ha="center",
                family=MONO, zorder=5)
        ax.text(x, base_y + 9, "weight", color=MUTED, fontsize=8, va="center",
                ha="center", family=SANS, zorder=5)
        # SLO PASS gate between stages
        if i < len(stages) - 1:
            gx = (x + xs[i + 1]) / 2
            ax.add_patch(FancyBboxPatch((gx - 7, base_y + 12), 14, 5,
                         boxstyle="round,pad=0,rounding_size=0.6", fc="#12261a",
                         ec=GREEN, lw=1.2, zorder=4))
            ax.text(gx, base_y + 14.5, "✔ SLO PASS", color=GREEN, fontsize=8.5,
                    fontweight="bold", va="center", ha="center", family=SANS, zorder=5)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((x + 6, base_y), (xs[i + 1] - 6, base_y),
                         arrowstyle="-|>", color=GREEN, lw=2.0, mutation_scale=14, zorder=4))

    ax.text(80, 44, "Each step bakes for 2m while the AnalysisRun checks the SLOs; "
            "all gates passed → full promotion, zero human intervention.",
            color=MUTED, fontsize=9.5, va="center", ha="center", family=SANS, zorder=4)

    # SLO summary strip
    panel(ax, 6, 8, 148, 28, "SLO gates evaluated this release", GREEN)
    cols = [
        ("5xx error rate", "0.31%", "< 1%", GREEN),
        ("p99 latency", "212 ms", "< 500 ms", GREEN),
        ("payment success", "99.7%", "≥ 99%", GREEN),
        ("CPU saturation", "47%", "< 80%", GREEN),
    ]
    cw = 35
    for i, (name, val, slo, col) in enumerate(cols):
        cx = 12 + i * 36
        ax.add_patch(FancyBboxPatch((cx, 11), cw, 19, boxstyle="round,pad=0,rounding_size=0.6",
                     fc="#1b212b", ec=BORDER, lw=1.1, zorder=4))
        ax.text(cx + cw / 2, 26, name, color=MUTED, fontsize=9, va="center", ha="center",
                family=SANS, zorder=5)
        ax.text(cx + cw / 2, 21, val, color=col, fontsize=17, fontweight="bold",
                va="center", ha="center", family=SANS, zorder=5)
        ax.text(cx + cw / 2, 16, f"SLO {slo}", color=MUTED, fontsize=8.5, va="center",
                ha="center", family=SANS, zorder=5)
        status_pill(ax, cx + cw / 2 - 5, 13, "PASS", GREEN, w=10)
    save(fig, "06_canary_promotion_timeline.png")


def main():
    img_rollouts_cli()
    img_grafana_dashboard()
    img_rollback()
    img_github_actions()
    img_argocd()
    img_promotion_timeline()
    print("\nAll images written to", os.path.normpath(OUT_DIR))


if __name__ == "__main__":
    main()
