#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחולל תמונה נלווית ממותגת ל-אלידע.
צינור: דמות קבועה (mascot-reference.png) -> סצנת פוסט עקבית ב-Gemini ->
הדבקת לוגו (assets/logo.png אם קיים). ללא כותרת טקסט על התמונה.

שימוש:
  python3 make_post_image.py --scene "תיאור סצנה באנגלית להמחשת הנושא" --out /path/out.png
  (--headline / --sub מתקבלים לתאימות לאחור אך אינם מצוירים על התמונה)

דרישות: GEMINI_API_KEY ב-env. Pillow (pip install Pillow).
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
        "Well-balanced composition filling the frame. No text, no letters, no words."
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

def overlay(img_path, out_path):
    """מדביק את הלוגו על הסצנה (ללא טקסט/כותרת)."""
    from PIL import Image
    img = Image.open(img_path).convert("RGBA")
    W, H = img.size

    # לוגו בפינה שמאלית-תחתונה (אם קיים)
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
    ap.add_argument("--headline", default="")   # מתקבל לתאימות לאחור; לא מצויר
    ap.add_argument("--sub", default="")         # מתקבל לתאימות לאחור; לא מצויר
    ap.add_argument("--scene", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tmp = a.out + ".scene.png"
    gen_scene(a.scene, tmp)
    overlay(tmp, a.out)
    print("saved", a.out)

if __name__ == "__main__":
    main()
