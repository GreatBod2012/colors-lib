# color.py
# ANSI color and style definitions
# Works in terminals that support ANSI escape codes
# Library " colors_lib.py " for colors in python !
# usage ( replace _ with your color & secondary style ( bold , dim , italic , underline , blink , reverse , hidden & strike ) & make sure they are all capitallized ) : print (_+"hello!")  
ESC = "\x1b["

# Reset
RESET = ESC + "0m"

# Styles
BOLD       = ESC + "1m"
DIM        = ESC + "2m"
ITALIC     = ESC + "3m"
UNDERLINE  = ESC + "4m"
BLINK      = ESC + "5m"
REVERSE    = ESC + "7m"
HIDDEN     = ESC + "8m"
STRIKE     = ESC + "9m"

# Foreground colors (standard)
BLACK   = ESC + "30m"
RED     = ESC + "31m"
GREEN   = ESC + "32m"
YELLOW  = ESC + "33m"
BLUE    = ESC + "34m"
MAGENTA = ESC + "35m"
CYAN    = ESC + "36m"
WHITE   = ESC + "37m"

# Foreground colors (bright)
BRIGHT_BLACK   = ESC + "90m"
BRIGHT_RED     = ESC + "91m"
BRIGHT_GREEN   = ESC + "92m"
BRIGHT_YELLOW  = ESC + "93m"
BRIGHT_BLUE    = ESC + "94m"
BRIGHT_MAGENTA = ESC + "95m"
BRIGHT_CYAN    = ESC + "96m"
BRIGHT_WHITE   = ESC + "97m"

# Background colors (standard)
BG_BLACK   = ESC + "40m"
BG_RED     = ESC + "41m"
BG_GREEN   = ESC + "42m"
BG_YELLOW  = ESC + "43m"
BG_BLUE    = ESC + "44m"
BG_MAGENTA = ESC + "45m"
BG_CYAN    = ESC + "46m"
BG_WHITE   = ESC + "47m"

# Background colors (bright)
BG_BRIGHT_BLACK   = ESC + "100m"
BG_BRIGHT_RED     = ESC + "101m"
BG_BRIGHT_GREEN   = ESC + "102m"
BG_BRIGHT_YELLOW  = ESC + "103m"
BG_BRIGHT_BLUE    = ESC + "104m"
BG_BRIGHT_MAGENTA = ESC + "105m"
BG_BRIGHT_CYAN    = ESC + "106m"
BG_BRIGHT_WHITE   = ESC + "107m"

# 256-color helpers
def fg256(n: int) -> str:
    """Foreground 256-color (0â255)"""
    return f"{ESC}38;5;{n}m"

def bg256(n: int) -> str:
    """Background 256-color (0â255)"""
    return f"{ESC}48;5;{n}m"

# Truecolor (24-bit RGB) helpers
def rgb(r: int, g: int, b: int) -> str:
    """Foreground truecolor"""
    return f"{ESC}38;2;{r};{g};{b}m"

def bg_rgb(r: int, g: int, b: int) -> str:
    """Background truecolor"""
    return f"{ESC}48;2;{r};{g};{b}m"

# Utility
def wrap(text: str, *styles: str) -> str:
    """Wrap text with one or more ANSI styles"""
    return "".join(styles) + text + RESET
# ===============================
# Advanced Animated Color Effects
# ===============================

import sys, time, math

# --- HSV â RGB (internal helper) ---
def _hsv_to_rgb(h, s=1.0, v=1.0):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i %= 6
    r, g, b = {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
        5: (v, p, q),
    }[i]
    return int(r * 255), int(g * 255), int(b * 255)


# -------------------------------------------------
# shift(text) â whole text smoothly changes color
# -------------------------------------------------
def shift(text, speed=0.02, hue_speed=0.25):
    """
    Smoothly cycles the entire text through colors.
    Ctrl+C to stop.
    """
    start = time.time()
    try:
        while True:
            h = ((time.time() - start) * hue_speed) % 1.0
            r, g, b = _hsv_to_rgb(h)
            sys.stdout.write(
                "\r\033[K" + rgb(r, g, b) + text + RESET
            )
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


# -------------------------------------------------
# wave(text) â per-character moving color wave
# -------------------------------------------------
def wave(text, speed=0.03, spread=0.35):
    """
    Creates a flowing RGB wave across characters.
    Ctrl+C to stop.
    """
    start = time.time()
    try:
        while True:
            t = time.time() - start
            out = []
            for i, ch in enumerate(text):
                r = int(128 + 127 * math.sin(i * spread + t * 2))
                g = int(128 + 127 * math.sin(i * spread + t * 2 + 2.094))
                b = int(128 + 127 * math.sin(i * spread + t * 2 + 4.188))
                out.append(rgb(r, g, b) + ch)
            sys.stdout.write("\r\033[K" + "".join(out) + RESET)
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")
# ============================================================
# Effects Engine (auto-fallback: Truecolor -> 256 -> 16 colors)
# Add this at the END of colors.py
# ============================================================

import os, sys, time, math

# Color mode:
#   "auto" (default), "truecolor", "256", "16", "off"
_COLOR_MODE = "auto"


def set_color_mode(mode: str = "auto") -> None:
    """
    mode: "auto", "truecolor", "256", "16", "off"
    """
    global _COLOR_MODE
    mode = (mode or "").strip().lower()
    if mode not in ("auto", "truecolor", "256", "16", "off"):
        raise ValueError('mode must be one of: "auto", "truecolor", "256", "16", "off"')
    _COLOR_MODE = mode


def safe_mode() -> str:
    """
    Returns the best supported mode: "truecolor", "256", "16", or "off".
    Uses environment heuristics. You can override with set_color_mode().
    """
    # Respect explicit override
    if _COLOR_MODE != "auto":
        return _COLOR_MODE

    # If not a TTY, avoid ANSI noise
    if not sys.stdout.isatty():
        return "off"

    term = (os.environ.get("TERM") or "").lower()
    colorterm = (os.environ.get("COLORTERM") or "").lower()

    # Common truecolor indicators
    if "truecolor" in colorterm or "24bit" in colorterm:
        return "truecolor"

    # Most modern terminals w/ 256 color advertise it
    if "256color" in term:
        return "256"

    # Otherwise assume at least basic ANSI 16 colors
    if term:
        return "16"

    return "off"


def _clamp8(x: int) -> int:
    return 0 if x < 0 else 255 if x > 255 else int(x)


def _rgb_to_ansi16(r: int, g: int, b: int) -> str:
    """
    Rough mapping RGB -> nearest ANSI 16 fg.
    (Good enough as fallback.)
    """
    # Luma-ish thresholding + dominant channel
    r, g, b = _clamp8(r), _clamp8(g), _clamp8(b)
    mx = max(r, g, b)
    mn = min(r, g, b)

    if mx < 40:
        return BLACK

    # If close to gray, use white/bright black
    if mx - mn < 18:
        return BRIGHT_WHITE if mx > 160 else WHITE if mx > 90 else BRIGHT_BLACK

    # Dominant channel logic
    if r >= g and r >= b:
        return BRIGHT_RED if r > 160 else RED
    if g >= r and g >= b:
        return BRIGHT_GREEN if g > 160 else GREEN
    if b >= r and b >= g:
        return BRIGHT_BLUE if b > 160 else BLUE

    return WHITE


def _rgb_to_xterm256(r: int, g: int, b: int) -> int:
    """
    Map RGB -> xterm-256 index (approx).
    Uses 6x6x6 cube + grayscale.
    """
    r, g, b = _clamp8(r), _clamp8(g), _clamp8(b)

    # Check grayscale ramp
    if abs(r - g) < 10 and abs(g - b) < 10:
        gray = r  # ~same
        if gray < 8:
            return 16
        if gray > 248:
            return 231
        return 232 + int((gray - 8) / 10)

    # 6x6x6 cube
    def to_6(x):
        return int(round(x / 255 * 5))

    ri, gi, bi = to_6(r), to_6(g), to_6(b)
    return 16 + 36 * ri + 6 * gi + bi


def color(r: int, g: int, b: int) -> str:
    """
    Foreground color with auto-fallback.
    """
    mode = safe_mode()
    if mode == "off":
        return ""
    if mode == "truecolor":
        return rgb(_clamp8(r), _clamp8(g), _clamp8(b))
    if mode == "256":
        return fg256(_rgb_to_xterm256(r, g, b))
    # "16"
    return _rgb_to_ansi16(r, g, b)


def bg_color(r: int, g: int, b: int) -> str:
    """
    Background color with auto-fallback.
    """
    mode = safe_mode()
    if mode == "off":
        return ""
    if mode == "truecolor":
        return bg_rgb(_clamp8(r), _clamp8(g), _clamp8(b))
    if mode == "256":
        return bg256(_rgb_to_xterm256(r, g, b))
    # 16-color bg fallback: use closest-ish by reusing fg mapping then converting to bg
    fg = _rgb_to_ansi16(r, g, b)
    # Convert fg ESC 3Xm / 9Xm to bg ESC 4Xm / 10Xm approximately
    # Basic map:
    map_fg_to_bg = {
        BLACK: BG_BLACK, RED: BG_RED, GREEN: BG_GREEN, YELLOW: BG_YELLOW,
        BLUE: BG_BLUE, MAGENTA: BG_MAGENTA, CYAN: BG_CYAN, WHITE: BG_WHITE,
        BRIGHT_BLACK: BG_BRIGHT_BLACK, BRIGHT_RED: BG_BRIGHT_RED, BRIGHT_GREEN: BG_BRIGHT_GREEN,
        BRIGHT_YELLOW: BG_BRIGHT_YELLOW, BRIGHT_BLUE: BG_BRIGHT_BLUE, BRIGHT_MAGENTA: BG_BRIGHT_MAGENTA,
        BRIGHT_CYAN: BG_BRIGHT_CYAN, BRIGHT_WHITE: BG_BRIGHT_WHITE
    }
    return map_fg_to_bg.get(fg, BG_BLACK)


# --------------------
# HSV helpers (smooth)
# --------------------
def _hsv_to_rgb(h: float, s: float = 1.0, v: float = 1.0):
    h = h % 1.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i %= 6
    rr, gg, bb = {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
        5: (v, p, q),
    }[i]
    return int(rr * 255), int(gg * 255), int(bb * 255)


def _clear_line():
    # carriage return + clear-to-end-of-line
    sys.stdout.write("\r\033[K")


# ======================
# One-shot (non-animated)
# ======================
def rainbow(text: str, spread: float = 0.08) -> str:
    """
    Returns a rainbow-colored string (per-character).
    """
    out = []
    for i, ch in enumerate(text):
        r, g, b = _hsv_to_rgb(i * spread)
        out.append(color(r, g, b) + ch)
    return "".join(out) + RESET


def rainbow_print(text: str, spread: float = 0.08, end: str = "\n") -> None:
    print(rainbow(text, spread=spread), end=end)


def gradient_like(text: str, start_rgb=(0, 200, 255), end_rgb=(255, 0, 120)) -> str:
    """
    Static "gradient-like" effect without gradients: each character is colored.
    """
    if not text:
        return ""
    sr, sg, sb = start_rgb
    er, eg, eb = end_rgb
    n = max(1, len(text) - 1)
    out = []
    for i, ch in enumerate(text):
        t = i / n
        r = int(sr + (er - sr) * t)
        g = int(sg + (eg - sg) * t)
        b = int(sb + (eb - sb) * t)
        out.append(color(r, g, b) + ch)
    return "".join(out) + RESET


# =================
# Animated effects
# =================
def shift(text: str, speed: float = 0.02, hue_speed: float = 0.25) -> None:
    """
    Whole text smoothly changes color over time. Ctrl+C to stop.
    """
    start = time.time()
    try:
        while True:
            h = ((time.time() - start) * hue_speed) % 1.0
            r, g, b = _hsv_to_rgb(h, 1.0, 1.0)
            _clear_line()
            sys.stdout.write(color(r, g, b) + text + RESET)
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


def wave(text: str, speed: float = 0.03, spread: float = 0.35, freq: float = 2.0) -> None:
    """
    Per-character RGB wave that moves. Ctrl+C to stop.
    """
    start = time.time()
    try:
        while True:
            t = (time.time() - start) * freq
            out = []
            for i, ch in enumerate(text):
                r = int(128 + 127 * math.sin(i * spread + t))
                g = int(128 + 127 * math.sin(i * spread + t + 2.094))
                b = int(128 + 127 * math.sin(i * spread + t + 4.188))
                out.append(color(r, g, b) + ch)
            _clear_line()
            sys.stdout.write("".join(out) + RESET)
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


def pulse(text: str, speed: float = 0.02, hue: float = 0.55, min_v: float = 0.15, max_v: float = 1.0) -> None:
    """
    Pulsing brightness (breathing) on a fixed hue. Ctrl+C to stop.
    """
    start = time.time()
    try:
        while True:
            t = (time.time() - start) * 2.0
            v = (math.sin(t) + 1) / 2  # 0..1
            v = min_v + (max_v - min_v) * v
            r, g, b = _hsv_to_rgb(hue, 1.0, v)
            _clear_line()
            sys.stdout.write(color(r, g, b) + text + RESET)
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


def typewriter(text: str, delay: float = 0.03, style: str = "") -> None:
    """
    Typewriter print. Optional ANSI style (e.g., BOLD, DIM, UNDERLINE).
    """
    try:
        for ch in text:
            sys.stdout.write(style + ch + RESET)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


def typewriter_wave(text: str, delay: float = 0.01, spread: float = 0.14) -> None:
    """
    Typewriter + rainbow per character (static hue progression).
    """
    try:
        for i, ch in enumerate(text):
            r, g, b = _hsv_to_rgb(i * spread)
            sys.stdout.write(color(r, g, b) + ch + RESET)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")
# =========================
# Optional GUI (Tkinter)
# =========================

def gui_preview():
    """
    Opens a small Tkinter GUI to preview animated color effects.
    - Works even if your terminal doesn't support ANSI (because GUI uses real RGB).
    - No external libs needed (Tkinter is built-in on many Python installs).
    """
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception as e:
        raise RuntimeError("Tkinter is not available in this Python environment.") from e

    # --- helpers ---
    def _hex_rgb(r, g, b):
        return f"#{_clamp8(r):02x}{_clamp8(g):02x}{_clamp8(b):02x}"

    root = tk.Tk()
    root.title("colors.py â GUI Preview")
    root.geometry("680x340")
    root.configure(bg="#0b0f1a")

    # Layout
    frm = tk.Frame(root, bg="#0b0f1a")
    frm.pack(fill="both", expand=True, padx=14, pady=14)

    title = tk.Label(frm, text="colors.py GUI Preview", fg="#e5e7eb", bg="#0b0f1a",
                     font=("Segoe UI", 16, "bold"))
    title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    tk.Label(frm, text="Text:", fg="#9ca3af", bg="#0b0f1a", font=("Segoe UI", 11)).grid(
        row=1, column=0, sticky="w"
    )

    text_var = tk.StringVar(value="Hello from colors.py")
    entry = tk.Entry(frm, textvariable=text_var, font=("Segoe UI", 12),
                     bg="#111827", fg="#e5e7eb", insertbackground="#e5e7eb",
                     relief="flat")
    entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(10, 0), ipady=6)

    tk.Label(frm, text="Effect:", fg="#9ca3af", bg="#0b0f1a", font=("Segoe UI", 11)).grid(
        row=2, column=0, sticky="w", pady=(12, 0)
    )

    effect_var = tk.StringVar(value="shift")
    effect = ttk.Combobox(frm, textvariable=effect_var, state="readonly",
                          values=("shift", "pulse", "wave_static"))
    effect.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(12, 0))

    speed_var = tk.DoubleVar(value=0.02)
    tk.Label(frm, text="Speed:", fg="#9ca3af", bg="#0b0f1a", font=("Segoe UI", 11)).grid(
        row=3, column=0, sticky="w", pady=(12, 0)
    )
    speed = tk.Scale(frm, from_=0.005, to=0.08, resolution=0.001, orient="horizontal",
                     variable=speed_var, length=240, bg="#0b0f1a", fg="#e5e7eb",
                     troughcolor="#111827", highlightthickness=0)
    speed.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(12, 0))

    preview = tk.Label(frm, text="", fg="#e5e7eb", bg="#0b0f1a",
                       font=("Segoe UI", 26, "bold"))
    preview.grid(row=4, column=0, columnspan=3, sticky="w", pady=(22, 8))

    hint = tk.Label(frm, text="Tip: This is GUI RGB preview (not ANSI).",
                    fg="#6b7280", bg="#0b0f1a", font=("Segoe UI", 10))
    hint.grid(row=5, column=0, columnspan=3, sticky="w")

    frm.columnconfigure(1, weight=1)

    # Animation loop
    start = time.time()

    def tick():
        t = time.time() - start
        txt = text_var.get()

        eff = effect_var.get()
        spd = float(speed_var.get())

        if eff == "shift":
            # hue cycles
            h = (t * 0.25) % 1.0
            r, g, b = _hsv_to_rgb(h, 1.0, 1.0)
            preview.config(text=txt, fg=_hex_rgb(r, g, b))

        elif eff == "pulse":
            # fixed hue, breathing brightness
            hue = 0.55
            v = (math.sin(t * 2.0) + 1) / 2
            v = 0.15 + (1.0 - 0.15) * v
            r, g, b = _hsv_to_rgb(hue, 1.0, v)
            preview.config(text=txt, fg=_hex_rgb(r, g, b))

        else:  # "wave_static"
            # Tkinter Label can't color per-char easily without Text widget styling;
            # so we approximate by coloring the whole string using the first char phase.
            r = int(128 + 127 * math.sin(t * 2.0))
            g = int(128 + 127 * math.sin(t * 2.0 + 2.094))
            b = int(128 + 127 * math.sin(t * 2.0 + 4.188))
            preview.config(text=txt, fg=_hex_rgb(r, g, b))

        root.after(int(max(5, spd * 1000)), tick)

    tick()
    entry.focus()
    root.mainloop()
# ======================
# Pythonista UI SUPPORT
# ======================

try:
    import ui
except ImportError:
    ui = None
__APP_VIEW__ = None
def screen(title="App", background=WHITE, mode="sheet"):
    """
    Create and present the main screen.
    """
    global __APP_VIEW__
    
    if ui is None:
        raise RuntimeError("UI only works in Pythonista")

    v = ui.View()
    v.name = title
    v.background_color = _color(background)
    v.present(mode)
    
    __APP_VIEW__ = v
    return v
def button(
    text="Button",
    x=50,
    y=100,
    width=200,
    height=50,
    color=BLUE,
    text_color=WHITE,
    radius=12,
    on_click=None
):
    """
    Add a button to the active screen.
    """
    if ui is None:
        raise RuntimeError("UI only works in Pythonista")

    if __APP_VIEW__ is None:
        raise RuntimeError("Call screen() before adding buttons")

    b = ui.Button()
    b.title = text
    b.frame = (x, y, width, height)
    b.background_color = _color(color)
    b.tint_color = _color(text_color)
    b.corner_radius = radius

    if callable(on_click):
        b.action = on_click

    __APP_VIEW__.add_subview(b)
    return b
def _color(c):
    if isinstance(c, tuple):
        return c

    if c in (BLACK,):
        return (0, 0, 0)
    if c in (WHITE,):
        return (1, 1, 1)
    if c in (RED,):
        return (1, 0, 0)
    if c in (GREEN,):
        return (0, 1, 0)
    if c in (BLUE,):
        return (0, 0.45, 0.9)
    if c in (YELLOW,):
        return (1, 0.8, 0)
    
    return (0.9, 0.9, 0.9)
