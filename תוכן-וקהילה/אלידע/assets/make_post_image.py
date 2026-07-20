#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחולל תמונה נלווית ממותגת ל-אלידע.
צינור: דמות קבועה (mascot-reference.png) -> סצנת פוסט עקבית ב-Gemini ->
הלבשת כותרת עברית (Rubik) + לוגו (assets/logo.png אם קיים).

שימוש:
  python3 make_post_image.py --headline "כותרת" --sub "תת-כותרת" \
      --scene "תיאור סצנה באנגלית להמחשת הנושא" --out /path/out.png

דרישות: GEMINI_API_KEY ב-env. Pillow + python-bidi (pip install Pillow python-bidi).
"""
import os, sys, json, base64, argparse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MASCOT = os.path.join(HERE, "mascot-reference.png")
LOGO = os.path.join(HERE, "logo.png")          # אופציונלי — לוגו שקוף
FONT = os.path.join(HERE, "Rubik-Regular.ttf")
CACERT = "/root/.ccr/ca-bundle.crt"

# פלטת המותג
NAVY, ROYAL, TEAL, WHITE = "#16255F", "#2C5AE0", "#38A9BC", "#FFFFFF"

def gen_scene(scene_desc, out_path):
    """מייצר סצנת פוסט עם הדמות הקבועה כרפרנס."""
    key = os.environ["GEMINI_API_KEY"]
    ref = base64.b64encode(open(MASCOT, "rb").read()).decode()
    prompt = (
        "Use the EXACT SAME robot mascot character shown in the reference image "
        "(same design, same teal check-mark crest on its head, same colors and proportions) "
        "— keep it perfectly consistent. Place it in a premium 3D marketing scene: "
        f"{scene_desc}. "
        f"Clean gradient background in brand blues (navy {NAVY}, royal blue {ROYAL}) with "
        f"subtle glowing tech-circuit motifs and teal {TEAL} accents. Cinematic soft studio "
        "lighting, glossy clay render, premium advertising quality. Square 1:1. "
        "Leave clean empty space in the UPPER THIRD for a headline. No text, no letters, no words."
    )
    parts = [{"inlineData": {"mimeType": "image/png", "data": ref}}, {"text": prompt}]
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"responseModalities": ["IMAGE"]}}).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key={key}",
        data=body, headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            open(out_path, "wb").write(base64.b64decode(p["inlineData"]["data"]))
            return out_path
    raise RuntimeError("no image returned: " + json.dumps(d)[:300])

def overlay(img_path, headline, sub, out_path):
    """מלביש כותרת עברית + לוגו על הסצנה."""
    from PIL import Image, ImageDraw, ImageFont
    from bidi.algorithm import get_display
    img = Image.open(img_path).convert("RGBA")
    W, H = img.size
    d = ImageDraw.Draw(img)

    def draw_center(text, y, size, fill):
        f = ImageFont.truetype(FONT, size)
        disp = get_display(text)
        tw = d.textlength(disp, font=f)
        x = (W - tw) / 2
        d.text((x + 2, y + 2), disp, font=f, fill=(0, 0, 0, 160))   # צל לקריאוּת
        d.text((x, y), disp, font=f, fill=fill)

    if headline:
        draw_center(headline, int(H * 0.055), int(H * 0.070), (56, 169, 188, 255))  # טורקיז
    if sub:
        draw_center(sub, int(H * 0.150), int(H * 0.050), (255, 255, 255, 255))

    # לוגו בפינה תחתונה (אם קיים)
    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        lw = int(W * 0.24)
        lh = int(lw * logo.height / logo.width)
        logo = logo.resize((lw, lh))
        img.alpha_composite(logo, (int(W * 0.04), int(H - lh - W * 0.04)))

    img.convert("RGB").save(out_path, "PNG")
    return out_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--scene", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tmp = a.out + ".scene.png"
    gen_scene(a.scene, tmp)
    overlay(tmp, a.headline, a.sub, a.out)
    print("saved", a.out)

if __name__ == "__main__":
    main()
