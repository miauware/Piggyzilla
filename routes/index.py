from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    Response,
    current_app,
    session,
    send_from_directory,
)
from flask_babel import _
from flask_login import current_user
from main import csrf

bp = Blueprint("index", __name__)


@csrf.exempt
@bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("index.html")


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        "static/icon", "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@bp.route("/set_language/<language>", methods=["POST"])
def set_language(language):
    session["lang"] = language
    next_page = request.referrer or url_for("index.home")
    return redirect(next_page)


@bp.route("/static/css/custom-colors.css")
def customcss():
    from PIL import Image
    import colorsys

    def is_near_gray(r, g, b, threshold=15):
        # INFO: detect gray-like colors
        return (
            abs(r - g) < threshold and abs(r - b) < threshold and abs(g - b) < threshold
        )

    def is_near_black_or_white(r, g, b):
        # INFO: filter colors too close to black or white
        if r < 30 and g < 30 and b < 30:
            return True
        if r > 225 and g > 225 and b > 225:
            return True
        return False

    def is_too_close(c1, c2, threshold=35):
        # INFO: avoid very similar colors
        return sum(abs(a - b) for a, b in zip(c1, c2)) < threshold

    def rgb_to_hex(color):
        return "#{:02x}{:02x}{:02x}".format(*color)

    def clamp(x, lo, hi):
        # INFO: clamp helper
        return max(lo, min(hi, x))

    def to_ui_scale(color, steps=7):
        r, g, b = [x / 255 for x in color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        palette = []

        for i in range(steps):
            t = i / (steps - 1)  # 0 → 1

            # INFO: UI-like curve (lighter top, darker bottom)
            new_v = clamp(0.92 - t * 0.5, 0.45, 0.92)
            new_s = clamp(0.25 + t * 0.35, 0.25, 0.65)

            rr, gg, bb = colorsys.hsv_to_rgb(h, new_s, new_v)
            palette.append((int(rr * 255), int(gg * 255), int(bb * 255)))

        return palette

    def main_colors_hex(path, n=7):
        img = Image.open(path).convert("RGB")

        quant = img.quantize(colors=16)
        palette = quant.getpalette()
        color_counts = sorted(quant.getcolors(), reverse=True)

        base_colors = []

        # INFO: extract base colors
        for count, idx in color_counts:
            r, g, b = palette[idx * 3 : idx * 3 + 3]

            if is_near_gray(r, g, b) or is_near_black_or_white(r, g, b):
                continue

            candidate = (r, g, b)

            if any(is_too_close(candidate, c) for c in base_colors):
                continue

            base_colors.append(candidate)

            if len(base_colors) >= 3:
                break

        # FIXME: fallback if no valid base colors
        if not base_colors:
            base_colors = [(120, 120, 120)]

        final_colors = []
        attempts = 0
        max_attempts = 50  # INFO: prevents infinite loop

        # INFO: build palette from base colors
        for base in base_colors:
            scale = to_ui_scale(base, steps=n)

            for c in scale:
                if not any(is_too_close(c, existing) for existing in final_colors):
                    final_colors.append(c)

                if len(final_colors) >= n:
                    break

            if len(final_colors) >= n:
                break

        # INFO: deterministic fallback completion
        i = 1
        while len(final_colors) < n and attempts < max_attempts:
            base = base_colors[i % len(base_colors)]
            scale = to_ui_scale(base, steps=n)

            c = scale[i % len(scale)]

            if not any(is_too_close(c, existing) for existing in final_colors):
                final_colors.append(c)

            i += 1
            attempts += 1

        # INFO: final safety fallback
        while len(final_colors) < n:
            c = (
                100 + len(final_colors) * 10,
                80 + len(final_colors) * 7,
                90 + len(final_colors) * 5,
            )

            final_colors.append(tuple(map(lambda x: clamp(x, 60, 200), c)))

        return [rgb_to_hex(c) for c in final_colors[:n]]

    colors_mode = current_app.config.get("COLORS_MODE")

    if colors_mode == "default":
        # INFO: default palette
        customcolor1 = "#1f2936"
        customcolor2 = "#5e00d1"
        customcolor3 = "radial-gradient(circle, #8b3cff, #4f26e5)"
        customcolor4 = "#334155"
        textcolor = "#ffffff"
    else:
        colors = main_colors_hex("static/icon/favicon.ico", 7)

        customcolor1 = colors[0]
        customcolor2 = colors[1]
        customcolor3 = colors[2]
        customcolor4 = colors[3]
        customcolor5 = colors[4]
        customcolor6 = colors[5]
        customcolor7 = colors[6]
        textcolor = colors[4]

    customfont = "Brush Script MT,cursive"

    css = f"""
    :root {{
        --customcolor1: {customcolor1};
        --customcolor2: {customcolor2};
        --customcolor3: {customcolor3};
        --customcolor4: {customcolor4};
        --customcolor5: {customcolor5};
        --customcolor6: {customcolor6};
        --customcolor7: {customcolor7};
        --textcolor: {textcolor};
        --customfont: {customfont};
    }}
    .customcolor1 {{
        background-color: var(--customcolor1);
    }}
    .customcolor2 {{
        background-color: var(--customcolor2);
    }}
    .customcolor3 {{
        background-color: var(--customcolor3);
    }}
    .customcolor4 {{
        background-color: var(--customcolor4);
    }}
     .customcolor5 {{
        background-color: var(--customcolor5);
    }}
    .customcolor6 {{
        background-color: var(--customcolor6);
    }}
    .customcolor7 {{
        background-color: var(--customcolor7);
    }}   
    .customtext {{
        color: var(--textcolor);
        font-family: var(--customfont);
    }}
    """
    response = Response(css, mimetype="text/css")

    return response
