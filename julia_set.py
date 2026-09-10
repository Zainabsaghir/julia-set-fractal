# ============================================================
# CELL 1 — Imports
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

# ============================================================
# CELL 2 — Julia set core function
# ============================================================
def julia_set(c, width=900, height=900, x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), max_iter=300):
    """
    Computes a smooth escape-time Julia set for a given complex constant c.
    Returns a 2D array of escape values used to color each pixel.
    """
    x = np.linspace(x_range[0], x_range[1], width)
    y = np.linspace(y_range[0], y_range[1], height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    div_time = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = np.abs(Z) > 2
        newly_escaped = escaped & mask
        # smooth coloring formula (avoids banding)
        div_time[newly_escaped] = i + 1 - np.log(np.log(np.abs(Z[newly_escaped]) + 1e-9)) / np.log(2)
        mask &= ~escaped

    div_time[mask] = max_iter
    return div_time


def render_to_array(div_time, cmap='twilight_shifted'):
    """Renders the div_time grid to an RGB image array using a Matplotlib colormap."""
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    ax.imshow(div_time, cmap=cmap, extent=(-1.5, 1.5, -1.5, 1.5))
    ax.axis('off')
    fig.tight_layout(pad=0)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert('RGB')


# ============================================================
# CELL 3 — Render one high-resolution Julia set (for README screenshot / T-shirt design)
# ============================================================
c_main = complex(-0.7, 0.27015)   # classic, visually striking Julia constant
div_time = julia_set(c_main, width=1000, height=1000, max_iter=300)
img = render_to_array(div_time, cmap='twilight_shifted')
img.save('julia_set.png')
print("Saved julia_set.png")

# ============================================================
# CELL 4 — Animate across multiple Julia constants (goes beyond a static image)
# ============================================================
c_values = [
    complex(-0.70176, -0.3842),
    complex(-0.8, 0.156),
    complex(-0.7, 0.27015),
    complex(0.285, 0.01),
    complex(-0.4, 0.6),
    complex(-0.835, -0.2321),
]

frames = []
for c in c_values:
    dt = julia_set(c, width=500, height=500, max_iter=150)
    frame = render_to_array(dt, cmap='twilight_shifted')
    frames.append(frame)

# ping-pong the sequence so the GIF loops smoothly back to the start
frames_loop = frames + frames[::-1][1:-1]

frames_loop[0].save(
    'julia_animation.gif',
    save_all=True,
    append_images=frames_loop[1:],
    duration=350,
    loop=0
)
print("Saved julia_animation.gif")
