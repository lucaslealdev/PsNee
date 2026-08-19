import os

# Generates docs/{index,devices/*,boards/*}.html from the data below. Run
# from anywhere with `python3 docs/tools/gen_site.py` — paths are resolved
# relative to this script's own location, not the current directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))

# Pixel dimensions of the optimized images, keyed by filename — required by
# PhotoSwipe (data-pswp-width/height) for correct zoom-in animation sizing.
IMG_DIMS = {
    "pu-7.jpg": (1247, 1074),
    "pu-8-late.jpg": (1400, 1221),
    "pu-8-early.jpg": (1400, 1181),
    "pu-16.jpg": (1400, 924),
    "pu-18.jpg": (1400, 1065),
    "pu-20.jpg": (1400, 1082),
    "pu-22.jpg": (1400, 911),
    "pu-23.jpg": (1400, 756),
    "pm-41.jpg": (1400, 1133),
    "pm-41-2.jpg": (1400, 1241),
    "nano.jpg": (900, 1200),
    "psnee-v9-pinout.png": (670, 471),
    "led-pin.png": (778, 376),
    "patch-switch.png": (642, 331),
    "40p-scph-1000-3000.jpg": (848, 662),
    "32p-scph-3500-5500.jpg": (1200, 1015),
    "32p-scph-7000-100.jpg": (1200, 1015),
    "40p-scph-3500-5000.jpg": (924, 675),
    "32p-pinout.png": (637, 727),
    "40p-pinout.png": (800, 752),
}


# Images that have a real, meaningfully-smaller "-thumb" sibling generated
# by gen_thumbs.py — used for the inline <img>, while the link/lightbox
# target (and "open in new tab") keep pointing at the full-resolution file.
# The small line-art diagrams (pinout/LED/switch wiring) are already tiny at
# full size, so a resized copy of those wouldn't be meaningfully smaller —
# they're intentionally left out and just use the full image inline too.
HAS_THUMB = {
    "pu-7.jpg", "pu-8-early.jpg", "pu-8-late.jpg", "pu-16.jpg", "pu-18.jpg",
    "pu-20.jpg", "pu-22.jpg", "pu-23.jpg", "pm-41.jpg", "pm-41-2.jpg",
    "nano.jpg", "40p-scph-1000-3000.jpg", "32p-scph-3500-5500.jpg",
    "32p-scph-7000-100.jpg",
}


def thumb_src(src):
    basename = src.rsplit("/", 1)[-1]
    if basename not in HAS_THUMB:
        return src
    root, ext = basename.rsplit(".", 1)
    return src[: -len(basename)] + f"{root}-thumb.{ext}"


def fig(src, alt, caption=None, indent="    ", style=None):
    """A <figure> whose image opens in a PhotoSwipe zoom lightbox, with a
    plain 'open in new tab' link as a no-JS fallback / explicit affordance.
    The inline preview loads a small thumbnail; only the lightbox / "open in
    new tab" pull the full-resolution original, so a page never downloads a
    1400px photo just to show it as a 300px preview."""
    basename = src.rsplit("/", 1)[-1]
    w, h = IMG_DIMS[basename]
    cap = caption if caption is not None else alt
    style_attr = f' style="{style}"' if style else ""
    preview = thumb_src(src)
    return (
        f'{indent}<figure{style_attr}>\n'
        f'{indent}  <a class="zoom-link" href="{src}" target="_blank" rel="noreferrer" '
        f'data-pswp-width="{w}" data-pswp-height="{h}" data-i18n-attr="title:common.zoomHint">\n'
        f'{indent}    <img src="{preview}" alt="{alt}" loading="lazy">\n'
        f'{indent}  </a>\n'
        f'{indent}  <figcaption>{cap}</figcaption>\n'
        f'{indent}  <div class="figure-links"><a href="{src}" target="_blank" rel="noreferrer" '
        f'data-i18n="common.openInNewTab">Open image in new tab &#8599;</a></div>\n'
        f'{indent}</figure>'
    )

BOARD_ORDER = ["pu7", "pu8", "pu16", "pu18", "pu20", "pu22", "pu23", "pm41", "pm412"]

BOARDS = {
    "pu7": {
        "name": "PU-7",
        "images": [("../assets/images/boards/pu-7.jpg", "PU-7")],
        "models": [("qAll", "SCPH-1000"), ("qSomeEarly", "SCPH-1001"), ("qSomeEarly", "SCPH-1002"),
                   ("qSomeEarly", "SCPH-3000"), ("qSomeEarly", "SCPH-3500")],
        "revisions": ["1-655-322-11", "1-655-322-12B", "1-655-322-13", "1-655-322-13A", "1-655-322-13B",
                      "1-655-322-14", "1-655-322-14A", "1-655-322-15", "1-655-322-16"],
        "bios_images": [("../assets/images/bios/40p-scph-1000-3000.jpg", "40-pin BIOS · SCPH-1000 / SCPH-3000")],
        "bios_patch": True,
    },
    "pu8": {
        "name": "PU-8",
        "images": [("../assets/images/boards/pu-8-early.jpg", "PU-8 (early revision)"),
                    ("../assets/images/boards/pu-8-late.jpg", "PU-8 (late revision)")],
        "models": [("qMost", "SCPH-1001"), ("qMost", "SCPH-1002"), ("qMost", "SCPH-3000"),
                   ("qMost", "SCPH-3500"), ("qAll", "SCPH-5000")],
        "revisions": ["1-658-467-11", "1-658-467-12", "1-658-467-13",
                      "1-658-467-21", "1-658-467-22", "1-658-467-23", "1-658-467-41", "1-658-467-42"],
        "bios_images": [("../assets/images/bios/40p-scph-1000-3000.jpg", "40-pin BIOS · SCPH-1000 / SCPH-3000")],
        "bios_patch": True,
    },
    "pu16": {
        "name": "PU-16",
        "images": [("../assets/images/boards/pu-16.jpg", "PU-16")],
        "models": [("qAll", "SCPH-5903")],
        "revisions": ["1-665-191-11"],
        "bios_images": [],
        "bios_patch": False,
    },
    "pu18": {
        "name": "PU-18",
        "images": [("../assets/images/boards/pu-18.jpg", "PU-18")],
        "models": [("qAll", "SCPH-5001"), ("qAll", "SCPH-5500"), ("qAll", "SCPH-5501"), ("qAll", "SCPH-5502"),
                   ("qAll", "SCPH-5503"), ("qAll", "SCPH-5552"), ("qSomeEarly", "SCPH-7000"),
                   ("qSomeEarly", "SCPH-7001"), ("qSomeEarly", "SCPH-7002"), ("qSomeEarly", "SCPH-7003"),
                   ("qSomeEarly", "SCPH-7501")],
        "revisions": ["1-664-537-11", "1-664-537-21", "1-664-537-31", "1-664-537-41",
                      "1-664-537-52", "1-664-537-62", "1-664-537-72", "1-664-537-82"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family"),
                         ("../assets/images/bios/32p-scph-3500-5500.jpg", "32-pin BIOS · SCPH-3500 / SCPH-5500")],
        "bios_patch": True,
    },
    "pu20": {
        "name": "PU-20",
        "images": [("../assets/images/boards/pu-20.jpg", "PU-20")],
        "models": [("qMost", "SCPH-7000"), ("qMost", "SCPH-7001"), ("qMost", "SCPH-7002"), ("qMost", "SCPH-7003")],
        "revisions": ["1-668-413-12", "1-668-413-22", "1-668-413-32", "1-668-413-42", "1-668-413-52"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family")],
        "bios_patch": True,
    },
    "pu22": {
        "name": "PU-22",
        "images": [("../assets/images/boards/pu-22.jpg", "PU-22")],
        "models": [("qAll", "SCPH-7500"), ("qMost", "SCPH-7501"), ("qAll", "SCPH-7502"), ("qAll", "SCPH-7503"),
                   ("qSomeEarly", "SCPH-9000"), ("qSomeEarly", "SCPH-9001"), ("qSomeEarly", "SCPH-9002"),
                   ("qSomeEarly", "SCPH-9003")],
        "revisions": ["1-674-858-11", "1-674-858-21", "1-674-858-31", "1-674-858-41", "1-674-858-51"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family")],
        "bios_patch": True,
    },
    "pu23": {
        "name": "PU-23",
        "images": [("../assets/images/boards/pu-23.jpg", "PU-23")],
        "models": [("qMost", "SCPH-9000"), ("qMost", "SCPH-9001"), ("qMost", "SCPH-9002"), ("qMost", "SCPH-9003")],
        "revisions": ["1-674-987-11", "1-674-987-21", "1-674-987-31", "1-674-987-41", "1-674-987-51"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family")],
        "bios_patch": True,
    },
    "pm41": {
        "name": "PM-41",
        "images": [("../assets/images/boards/pm-41.jpg", "PM-41")],
        "models": [("qEarlier", "SCPH-100"), ("qEarlier", "SCPH-101"), ("qEarlier", "SCPH-102"), ("qEarlier", "SCPH-103")],
        "revisions": ["1-679-335-11", "1-679-335-21", "1-679-335-31", "1-679-335-41", "1-679-335-51",
                      "1-679-335-61", "6P-172143S11-B3"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family")],
        "bios_patch": True,
    },
    "pm412": {
        "name": "PM-41 (2)",
        "images": [("../assets/images/boards/pm-41-2.jpg", "PM-41 (2)")],
        "models": [("qLater", "SCPH-100"), ("qLater", "SCPH-101"), ("qLater", "SCPH-102"), ("qLater", "SCPH-103")],
        "revisions": ["1-679-335-71", "1-679-335-82", "P-161125S-41-71", "P-161125S-41-81"],
        "bios_images": [("../assets/images/bios/32p-scph-7000-100.jpg", "32-pin BIOS · SCPH-7000 → SCPH-100 family")],
        "bios_patch": True,
    },
}

FILENAME = {
    "pu7": "pu-7", "pu8": "pu-8", "pu16": "pu-16", "pu18": "pu-18", "pu20": "pu-20",
    "pu22": "pu-22", "pu23": "pu-23", "pm41": "pm-41", "pm412": "pm-41-2",
}


PSWP_VERSION = "5"


def head(rel, title_key, desc, pswp=False):
    pswp_css = (
        f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/photoswipe@{PSWP_VERSION}/dist/photoswipe.css">\n'
        if pswp else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PSNee</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="{rel}assets/images/brand/favicon.png">
<link rel="stylesheet" href="{rel}assets/css/style.css">
{pswp_css}</head>
<body data-i18n-title="{title_key}">
"""


def header(rel, active):
    def cls(name):
        return ' class="current"' if name == active else ""
    return f"""<header class="site-header">
  <div class="nav-row">
    <a class="brand" href="{rel}index.html"><img src="{rel}assets/images/brand/logo-thumb.png" alt="PSNee logo"><span>PSNee</span></a>
    <button class="nav-toggle" aria-label="Toggle menu">&#9776;</button>
    <nav class="nav-links">
      <a href="{rel}index.html" data-i18n="nav.home"{cls('home')}>Home</a>
      <a href="{rel}devices/arduino-nano.html" data-i18n="nav.devices"{cls('devices')}>Devices</a>
      <a href="{rel}index.html#install" data-i18n="nav.install"{cls('install')}>Installation</a>
      <a href="https://github.com/kalymos/PsNee/wiki" data-i18n="nav.wiki" target="_blank" rel="noopener">Full wiki</a>
      <a href="https://github.com/lucaslealdev/PsNee" data-i18n="nav.github" target="_blank" rel="noopener">GitHub</a>
      <div class="lang-switch">
        <button data-lang="en">EN</button>
        <button data-lang="pt">PT</button>
        <button data-lang="es">ES</button>
      </div>
    </nav>
  </div>
</header>
<main>
"""


def footer(rel, pswp=False):
    pswp_script = ""
    if pswp:
        pswp_script = f"""<script type="module">
  import PhotoSwipeLightbox from "https://cdn.jsdelivr.net/npm/photoswipe@{PSWP_VERSION}/dist/photoswipe-lightbox.esm.js";
  var lightbox = new PhotoSwipeLightbox({{
    gallery: "main",
    children: "a.zoom-link",
    initialZoomLevel: "fit",
    secondaryZoomLevel: 2,
    maxZoomLevel: 4,
    pswpModule: () => import("https://cdn.jsdelivr.net/npm/photoswipe@{PSWP_VERSION}/dist/photoswipe.esm.js")
  }});
  lightbox.init();
</script>
"""
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <p class="footer-disclaimer" data-i18n="footer.disclaimer">PSNee is an unofficial, fan-made project.</p>
  </div>
  <div class="container">
    <span>PSNee &middot; <span data-i18n="footer.license">Public domain.</span></span>
    <div class="footer-links">
      <a href="https://github.com/lucaslealdev/PsNee" data-i18n="footer.sourceLink" target="_blank" rel="noopener">Source code</a>
      <a href="https://github.com/kalymos/PsNee/wiki" data-i18n="footer.wikiLink" target="_blank" rel="noopener">Full wiki</a>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/i18n.js"></script>
{pswp_script}</body>
</html>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------

board_cards = []
for bid in BOARD_ORDER:
    b = BOARDS[bid]
    img = thumb_src(b["images"][0][0]).replace("../assets/", "assets/")
    board_cards.append(f"""      <a class="card board-card" href="boards/{FILENAME[bid]}.html">
        <img src="{img}" alt="{b['name']} motherboard" loading="lazy">
        <h3>{b['name']}</h3>
        <span class="card-link" data-i18n="home.install.viewGuide">View installation guide &rarr;</span>
      </a>""")
board_cards_html = "\n".join(board_cards)

index_body = f"""<section class="hero">
  <div class="container">
    <span class="eyebrow" data-i18n="home.hero.eyebrow">Open-source PS1 modchip firmware</span>
    <h1 data-i18n="home.hero.title">PSNee</h1>
    <p class="lead" data-i18n="home.hero.subtitle">Firmware that removes the PS1's disc region lock.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="devices/arduino-nano.html" data-i18n="home.hero.cta1">See supported devices</a>
      <a class="btn btn-secondary" href="#install" data-i18n="home.hero.cta2">Installation guides</a>
    </div>
  </div>
</section>

<section class="container">
  <h2 data-i18n="home.what.title">What PSNee does</h2>
  <div class="two-col">
    <p class="lead" data-i18n="home.what.p1"></p>
    <p data-i18n="home.what.p2"></p>
  </div>
</section>

<section class="container">
  <h2 data-i18n="home.how.title">How it works</h2>
  <div class="card-grid">
    <div class="card">
      <h3 data-i18n="home.how.regionTitle"></h3>
      <p data-i18n="home.how.regionText"></p>
    </div>
    <div class="card">
      <h3 data-i18n="home.how.biosTitle"></h3>
      <p data-i18n="home.how.biosText"></p>
    </div>
  </div>
  <div class="callout callout-warn">
    <span class="callout-title" data-i18n="home.videoNote.title">Video signal note</span>
    <p data-i18n="home.videoNote.text"></p>
  </div>
</section>

<section class="container">
  <h2 data-i18n="home.hardware.title">Supported microcontrollers</h2>
  <p class="section-intro" data-i18n="home.hardware.intro"></p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th data-i18n="home.hardware.colMcu">MCU</th>
          <th data-i18n="home.hardware.colBoards">Boards</th>
          <th data-i18n="home.hardware.colBios">BIOS patch</th>
        </tr>
      </thead>
      <tbody>
        <tr><td data-i18n="home.hardware.atmega328"></td><td data-i18n="home.hardware.atmega328boards"></td><td><span class="badge badge-yes" data-i18n="home.hardware.yes"></span></td></tr>
        <tr><td data-i18n="home.hardware.atmega32u4"></td><td data-i18n="home.hardware.atmega32u4boards"></td><td><span class="badge badge-yes" data-i18n="home.hardware.yes"></span></td></tr>
        <tr><td data-i18n="home.hardware.attiny"></td><td data-i18n="home.hardware.attinyboards"></td><td><span class="badge badge-no" data-i18n="home.hardware.no"></span></td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="container" id="devices">
  <h2 data-i18n="home.devices.title">Devices</h2>
  <p class="section-intro" data-i18n="home.devices.intro"></p>
  <div class="card-grid">
    <div class="card">
      <span class="card-tag">ATmega328</span>
      <h3 data-i18n="home.devices.nanoTitle">Arduino Nano</h3>
      <p data-i18n="home.devices.nanoText"></p>
      <a class="card-link" href="devices/arduino-nano.html" data-i18n="home.devices.nanoCta">Open guide &rarr;</a>
    </div>
  </div>
</section>

<section class="container" id="install">
  <h2 data-i18n="home.install.title">PS1 motherboard installation guides</h2>
  <p class="section-intro" data-i18n="home.install.intro"></p>
  <div class="card-grid">
{board_cards_html}
  </div>
</section>

<section class="container">
  <div class="callout" style="text-align:center">
    <h3 style="margin-top:0" data-i18n="home.footerCta.title"></h3>
    <p data-i18n="home.footerCta.text"></p>
    <a class="btn btn-secondary" href="#install" data-i18n="home.footerCta.cta"></a>
  </div>
</section>
"""

write("index.html", head("", "home.hero.title", "PSNee: open-source firmware that removes the PS1 disc region lock.")
      + header("", "home") + index_body + footer(""))


# ---------------------------------------------------------------------------
# devices/arduino-nano.html
# ---------------------------------------------------------------------------

nano_body = f"""<section class="container">
  <span class="crumb" data-i18n="device.nano.crumb">Devices</span>
  <h1 data-i18n="device.nano.title">Arduino Nano</h1>
  <p class="lead" data-i18n="device.nano.intro"></p>
</section>

<section class="container">
  <div class="two-col">
    <div>
      <h2 data-i18n="device.nano.wiringTitle"></h2>
      <p data-i18n="device.nano.wiringText"></p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th data-i18n="common.signal">Signal</th><th data-i18n="common.nanoPin">Nano pin</th><th data-i18n="common.notes">Notes</th></tr>
          </thead>
          <tbody>
            <tr><td><code>VCC</code></td><td><code>VCC</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>GND</code></td><td><code>GND</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>SQCK</code></td><td><code>D6</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>SUBQ</code></td><td><code>D7</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>DATA</code></td><td><code>D8</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>WFCK</code></td><td><code>D9</code></td><td data-i18n="common.noteAlways"></td></tr>
            <tr><td><code>RESET</code></td><td><code>RST</code></td><td data-i18n="common.noteReset"></td></tr>
            <tr><td><code>BIOS AX</code></td><td><code>D2</code></td><td data-i18n="common.noteBiosAx"></td></tr>
            <tr><td><code>BIOS AY</code></td><td><code>D3</code></td><td data-i18n="common.noteBiosAy"></td></tr>
            <tr><td><code>BIOS DX</code></td><td><code>D4</code></td><td data-i18n="common.noteBiosDx"></td></tr>
            <tr><td><code>SWITCH</code></td><td><code>D5</code></td><td data-i18n="common.noteSwitch"></td></tr>
            <tr><td><code>LED</code></td><td><code>D13</code></td><td data-i18n="common.noteLed"></td></tr>
          </tbody>
        </table>
      </div>
    </div>
{fig("../assets/images/arduino/nano.jpg", "Arduino Nano board", "Arduino Nano")}
  </div>
</section>

<section class="container">
{fig("../assets/images/arduino/psnee-v9-pinout.png", "PSNee V9 pinout diagram", "PSNee V9 pinout reference", style="max-width:420px;margin-left:auto;margin-right:auto;")}
</section>

<section class="container">
  <h2 data-i18n="device.nano.usbTitle"></h2>
  <p data-i18n="device.nano.usbIntro"></p>
  <ol class="steps" data-i18n="device.nano.usbSteps"></ol>
</section>

<section class="container">
  <h2 data-i18n="device.nano.ispTitle"></h2>
  <div class="callout callout-danger">
    <span class="callout-title" data-i18n="common.important">Important</span>
    <p data-i18n="device.nano.ispIntro"></p>
  </div>
  <ol class="steps" data-i18n="device.nano.ispSteps"></ol>
</section>

<section class="container">
  <h2 data-i18n="device.nano.fusesTitle"></h2>
  <p data-i18n="device.nano.fusesText"></p>
</section>

<section class="container">
  <h2 data-i18n="device.nano.extrasTitle"></h2>
  <div class="two-col">
    <div>
      <h3 data-i18n="device.nano.ledTitle"></h3>
      <p data-i18n-html="device.nano.ledText"></p>
{fig("../assets/images/wiring/led-pin.png", "LED wiring diagram")}
    </div>
    <div>
      <h3 data-i18n="device.nano.switchTitle"></h3>
      <p data-i18n-html="device.nano.switchText"></p>
{fig("../assets/images/wiring/patch-switch.png", "BIOS patch switch wiring diagram")}
    </div>
  </div>
</section>

<section class="container">
  <div class="callout callout-danger">
    <span class="callout-title" data-i18n="device.nano.cautionTitle"></span>
    <p data-i18n="device.nano.cautionText"></p>
  </div>
</section>
"""

write("devices/arduino-nano.html",
      head("../", "device.nano.title", "How to flash PSNee firmware onto an Arduino Nano, with or without the BIOS patch.", pswp=True)
      + header("../", "devices") + nano_body + footer("../", pswp=True))


# ---------------------------------------------------------------------------
# boards/*.html
# ---------------------------------------------------------------------------

for bid in BOARD_ORDER:
    b = BOARDS[bid]

    figures = "\n".join(fig(src, alt) for src, alt in b["images"])
    figures += "\n" + fig("../assets/images/arduino/nano.jpg", "Arduino Nano board", "Arduino Nano")

    grid_class = "two-col" if len(b["images"]) == 1 else "card-grid"

    models_li = "\n".join(
        f'        <li><span data-i18n="common.{qkey}"></span> {code}</li>'
        for qkey, code in b["models"]
    )

    revisions_li = "\n".join(f"        <li>{r}</li>" for r in b["revisions"])

    bios_section = ""
    if b["bios_images"]:
        bios_figs = "\n".join(fig(src, alt, indent="      ") for src, alt in b["bios_images"])
        bios_section = f"""<section class="container">
  <h2 data-i18n="common.biosPinout"></h2>
  <div class="card-grid">
{bios_figs}
  </div>
</section>

"""

    special_note_html = ""
    if bid == "pu16":
        special_note_html = f"""  <div class="callout callout-warn">
    <span class="callout-title" data-i18n="common.warning">Warning</span>
    <p data-i18n="board.{bid}.specialNote"></p>
  </div>
"""

    bios_badge = 'badge-yes" data-i18n="common.biosRelevantYes' if b["bios_patch"] else 'badge-no" data-i18n="common.biosRelevantNo'

    body = f"""<section class="container">
  <span class="crumb"><a href="../index.html#install" data-i18n="common.backToInstall">&larr; Back to installation guides</a></span>
  <h1>{b['name']}</h1>
  <p class="lead" data-i18n="board.{bid}.intro"></p>
  <span class="badge {bios_badge}"></span>
</section>

<section class="container">
  <div class="{grid_class}">
{figures}
  </div>
</section>

<section class="container">
  <h2 data-i18n="common.modelsCovered"></h2>
  <ul class="model-list">
{models_li}
  </ul>
</section>

<section class="container">
  <h2 data-i18n="common.aboutPoints"></h2>
  <p data-i18n="board.{bid}.aboutPoints"></p>
{special_note_html}</section>

<section class="container">
  <h2 data-i18n="common.installTips"></h2>
  <ol class="steps" data-i18n="board.{bid}.tips"></ol>
</section>

{bios_section}<section class="container">
  <h2 data-i18n="common.revisions"></h2>
  <ul class="revision-list">
{revisions_li}
  </ul>
</section>

<section class="container">
  <div class="callout">
    <p><a href="../devices/arduino-nano.html" data-i18n="common.seeNanoGuide"></a></p>
  </div>
</section>
"""

    write(f"boards/{FILENAME[bid]}.html",
          head("../", f"board.{bid}.name", f"PsNee modchip installation guide for the PS1 {b['name']} motherboard.", pswp=True)
          + header("../", "install") + body + footer("../", pswp=True))

print("done")
