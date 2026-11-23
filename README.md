# 🖋️ Living Ink

> **Extracting nature's hidden geometry, translated into art.**

Living Ink is a computer vision and generative art application that transforms natural textures and organic forms (tree bark, leaf veins, cracked earth, stone textures, river flows, coral, clouds) into tattoo-ready illustrations and abstract fine art.

---

## ✨ Features

- **Organic Pattern Analysis**: Extracts dominant geometries, flow direction, branching hierarchy, texture frequency (FFT), edge density, and contour complexity using OpenCV.
- **6 Artistic Transformation Styles**:
  1. **Tattoo Design**: Bold blackwork with stippled mid-tone shading.
  2. **Abstract Illustration**: Painterly bilateral filtering with k-means color quantization.
  3. **Sacred Geometry Hybrid**: Organic contours fused with golden ratio spirals and geometric lattices.
  4. **Minimalist Ink**: Simplified essential contours retaining the core natural form.
  5. **Dark Botanical**: Moody, cross-hatched white-on-dark mystical aesthetic with vignette.
  6. **Living Sketch**: Wet-ink wash, pencil line divide, and organic splatter effects.
- **Interactive UI**:
  - Drag-and-drop file upload with real-time preview.
  - Interactive Before & After comparison slider.
  - Pattern metrics dashboard (Complexity, Flow, Density, Branching).
  - Poetic AI-generated micro-descriptions reflecting the soul of the pattern.
  - High-res instant artwork download.

---

## 🛠️ Project Structure

```
living-ink/
├── app.py                      # Flask web server and REST API
├── requirements.txt            # Python dependencies
├── processors/
│   ├── __init__.py
│   ├── analyzer.py             # Computer vision pattern detection
│   ├── styles.py               # 6 artistic transformation pipelines
│   └── poetry.py               # Pattern-aware poetic micro-generation
├── templates/
│   └── index.html              # Frontend template
└── static/
    ├── css/style.css           # Premium warm dark ink aesthetics
    ├── js/app.js               # Reactive client application logic
    ├── uploads/                # User uploaded source images
    └── outputs/                # Processed artwork
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/living-ink.git
cd living-ink
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (cmd):
.\venv\Scripts\activate.bat

# Linux / macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📜 License

MIT License. Feel free to use, modify, and build upon this project.
