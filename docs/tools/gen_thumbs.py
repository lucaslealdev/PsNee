from PIL import Image
import os

# Generates the "-thumb" preview images used inline on the site (the
# lightbox/"open in new tab" still point at the full-resolution original).
# Run with `python3 docs/tools/gen_thumbs.py` — resolved relative to this
# script's own location, not the current directory. Requires Pillow.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets", "images"))

# Deliberately excludes the small line-art diagrams (PSNee pinout, LED/switch
# wiring) — they're already tiny at full size (a few hundred pixels, under
# ~15KB), so resizing them further doesn't help and can even grow the file
# (resampling blurs sharp text/line edges, which compresses worse as PNG).
# Keep this list in sync with HAS_THUMB in gen_site.py.
CONTENT_IMAGES = [
    "arduino/nano.jpg",
    "bios/32p-scph-3500-5500.jpg",
    "bios/32p-scph-7000-100.jpg",
    "bios/40p-scph-1000-3000.jpg",
    "boards/pm-41-2.jpg",
    "boards/pm-41.jpg",
    "boards/pu-16.jpg",
    "boards/pu-18.jpg",
    "boards/pu-20.jpg",
    "boards/pu-22.jpg",
    "boards/pu-23.jpg",
    "boards/pu-7.jpg",
    "boards/pu-8-early.jpg",
    "boards/pu-8-late.jpg",
]

CONTENT_MAX_DIM = 640
LOGO_MAX_DIM = 200


def thumb_path(rel_path):
    root, ext = os.path.splitext(rel_path)
    return f"{root}-thumb{ext}"


def make_thumb(rel_path, max_dim):
    src_path = os.path.join(BASE, rel_path)
    dest_path = os.path.join(BASE, thumb_path(rel_path))
    im = Image.open(src_path)
    w, h = im.size
    scale = max_dim / max(w, h)
    if scale < 1:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    fmt = "JPEG" if src_path.lower().endswith((".jpg", ".jpeg")) else "PNG"
    if fmt == "JPEG":
        im = im.convert("RGB")
        im.save(dest_path, "JPEG", quality=78, optimize=True)
    else:
        im.save(dest_path, "PNG", optimize=True)
    print(os.path.relpath(dest_path, BASE), im.size,
          os.path.getsize(dest_path) // 1024, "KB  (full:",
          os.path.getsize(src_path) // 1024, "KB)")


for rel in CONTENT_IMAGES:
    make_thumb(rel, CONTENT_MAX_DIM)

make_thumb("brand/logo.png", LOGO_MAX_DIM)
