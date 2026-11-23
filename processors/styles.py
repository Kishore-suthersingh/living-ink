"""
Style Transformer — Converts nature photos into artistic ink illustrations.

Six distinct transformation pipelines:
  1. Tattoo Design      – Bold blackwork / fine-line, stippled shading
  2. Abstract            – Painterly color-quantized illustration
  3. Sacred Geometry     – Organic edges fused with golden-ratio geometry
  4. Minimalist Ink      – Extreme simplification, essential contours only
  5. Dark Botanical      – White-on-black, cross-hatched, moody
  6. Living Sketch       – Wet-ink pencil sketch with wash & splatter
"""

import math
import os

import cv2
import numpy as np


class StyleTransformer:
    """Applies artistic style transformations to nature photographs."""

    STYLES = {
        "tattoo": "Tattoo Design",
        "abstract": "Abstract Illustration",
        "sacred_geometry": "Sacred Geometry Hybrid",
        "minimalist": "Minimalist Ink",
        "dark_botanical": "Dark Botanical",
        "living_sketch": "Living Sketch",
    }

    def transform(self, image_path: str, style: str, analysis: dict) -> str:
        """
        Transform an image with the chosen style.

        Args:
            image_path: path to the uploaded image
            style: one of the STYLES keys
            analysis: pattern analysis dict

        Returns:
            Path to the saved output image.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")

        # Resize to reasonable working size (max 2048 on longest side)
        h, w = img.shape[:2]
        max_dim = 2048
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(
                img,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA,
            )

        dispatch = {
            "tattoo": self._tattoo,
            "abstract": self._abstract,
            "sacred_geometry": self._sacred_geometry,
            "minimalist": self._minimalist,
            "dark_botanical": self._dark_botanical,
            "living_sketch": self._living_sketch,
        }

        method = dispatch.get(style, self._tattoo)
        result = method(img, analysis)

        # Build output path
        base = os.path.basename(image_path)
        name, ext = os.path.splitext(base)
        # image_path is .../static/uploads/file.jpg → go up to .../static/, then into outputs/
        out_dir = os.path.join(
            os.path.dirname(os.path.dirname(image_path)), "outputs"
        )
        os.makedirs(out_dir, exist_ok=True)
        out_name = f"{name}_{style}.png"
        out_path = os.path.join(out_dir, out_name)
        cv2.imwrite(out_path, result, [cv2.IMWRITE_PNG_COMPRESSION, 3])
        return out_path

    # ================================================================ STYLES

    def _tattoo(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """Bold blackwork with stippled mid-tone shading."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Multi-scale Canny
        b1 = cv2.GaussianBlur(gray, (3, 3), 0)
        b2 = cv2.GaussianBlur(gray, (7, 7), 0)
        e1 = cv2.Canny(b1, 30, 100)
        e2 = cv2.Canny(b2, 50, 150)
        edges = cv2.bitwise_or(e1, e2)

        # Bold lines
        kernel = np.ones((2, 2), np.uint8)
        bold = cv2.dilate(edges, kernel, iterations=1)

        # Stippled shading in mid-tones
        _, dark_mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
        _, light_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        mid = cv2.bitwise_and(dark_mask, cv2.bitwise_not(light_mask))

        rng = np.random.RandomState(42)
        noise = rng.random(gray.shape)
        stipple = np.zeros_like(gray)
        # Density varies with darkness
        dark_norm = 1.0 - gray.astype(np.float32) / 255.0
        threshold_map = 0.92 - dark_norm * 0.12
        stipple_mask = (noise < threshold_map) & (mid > 0)
        stipple[~stipple_mask & (mid > 0)] = 255
        stipple = cv2.dilate(stipple, np.ones((2, 2), np.uint8), iterations=1)

        combined = cv2.bitwise_or(bold, stipple)

        # Black on white
        result = cv2.bitwise_not(combined)
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    def _abstract(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """Painterly bilateral filter + color quantization."""
        # Painterly smoothing
        filtered = img.copy()
        for _ in range(7):
            filtered = cv2.bilateralFilter(filtered, 9, 75, 75)

        # Structural edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
        )
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        result = cv2.bitwise_and(filtered, edges_bgr)

        # Color quantization (k-means)
        data = result.reshape((-1, 3)).astype(np.float32)
        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            20,
            1.0,
        )
        _, labels, centers = cv2.kmeans(
            data, 10, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        centers = np.uint8(centers)
        result = centers[labels.flatten()].reshape(result.shape)

        # Boost saturation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255)
        result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        return result

    def _sacred_geometry(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """Organic edges fused with golden-ratio geometric overlay."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Organic edges
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 40, 120)

        # --- Geometric overlay ---
        geo = np.zeros((h, w), dtype=np.uint8)
        cx, cy = w // 2, h // 2
        max_r = int(min(h, w) * 0.45)
        phi = 1.618033988749895

        # Golden-ratio concentric circles
        r = max_r
        for _ in range(9):
            ri = int(r)
            if ri > 3:
                cv2.circle(geo, (cx, cy), ri, 200, 1, cv2.LINE_AA)
            r /= phi

        # Fibonacci spiral
        angle = 0.0
        sr = 5.0
        px, py = cx, cy
        for _ in range(300):
            angle += 0.12
            sr += 0.45
            nx = int(cx + sr * math.cos(angle))
            ny = int(cy + sr * math.sin(angle))
            if 0 <= nx < w and 0 <= ny < h:
                cv2.line(geo, (px, py), (nx, ny), 180, 1, cv2.LINE_AA)
            px, py = nx, ny

        # Dual triangles (Star of David / merkaba)
        for offset_deg in (0, 180):
            pts = []
            for k in range(3):
                theta = math.radians(offset_deg + k * 120 - 90)
                pts.append(
                    [
                        int(cx + max_r * 0.72 * math.cos(theta)),
                        int(cy + max_r * 0.72 * math.sin(theta)),
                    ]
                )
            cv2.polylines(
                geo, [np.array(pts, np.int32)], True, 220, 1, cv2.LINE_AA
            )

        # Hexagonal lattice
        hex_r = max_r // 7
        sqrt3 = math.sqrt(3)
        for gy in range(-4, 5):
            for gx in range(-4, 5):
                hx = int(cx + gx * hex_r * 1.5)
                hy = int(cy + gy * hex_r * sqrt3 + (gx % 2) * hex_r * sqrt3 / 2)
                pts = []
                for a in range(6):
                    theta = math.radians(60 * a + 30)
                    pts.append(
                        [
                            int(hx + hex_r * 0.42 * math.cos(theta)),
                            int(hy + hex_r * 0.42 * math.sin(theta)),
                        ]
                    )
                cv2.polylines(
                    geo, [np.array(pts, np.int32)], True, 100, 1, cv2.LINE_AA
                )

        # Blend organic edges (bright) + geometry
        blended = cv2.addWeighted(edges, 0.8, geo, 0.5, 0)
        _, clean = cv2.threshold(blended, 25, 255, cv2.THRESH_BINARY)

        # White background, dark lines
        result = cv2.bitwise_not(clean)
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    def _minimalist(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """Extreme simplification — only the essential contours."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Heavy blur to erase detail
        blur = cv2.GaussianBlur(gray, (25, 25), 0)

        # Adaptive threshold with large block size
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 5
        )

        # Morphological open+close to merge small features
        k = np.ones((7, 7), np.uint8)
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, k)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, k)

        # Keep only the N largest contours
        inv = cv2.bitwise_not(closed)
        contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        keep = min(12, len(contours))

        canvas = np.ones_like(gray) * 255
        for c in contours[:keep]:
            eps = 0.012 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, eps, True)
            cv2.drawContours(canvas, [approx], -1, 0, 2, cv2.LINE_AA)

        return cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)

    def _dark_botanical(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """White-on-black with cross-hatching and vignette."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Detail-preserving edges
        e1 = cv2.Canny(gray, 20, 80)
        e2 = cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 40, 130)
        edges = cv2.bitwise_or(e1, e2)

        # Cross-hatching in dark regions
        _, dark = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

        hatch = np.zeros((h, w), dtype=np.uint8)
        for i in range(-max(h, w), max(h, w), 5):
            cv2.line(hatch, (i, 0), (i + h, h), 255, 1)
        for i in range(-max(h, w), max(h, w), 7):
            cv2.line(hatch, (i + h, 0), (i, h), 200, 1)

        hatch_masked = cv2.bitwise_and(hatch, dark)

        combined = cv2.bitwise_or(edges, hatch_masked)

        # Vignette mask
        vig = np.zeros((h, w), dtype=np.float32)
        cv2.circle(vig, (w // 2, h // 2), int(min(h, w) * 0.55), 1.0, -1)
        vig = cv2.GaussianBlur(vig, (0, 0), sigmaX=min(h, w) * 0.18)
        vig = np.clip(vig, 0, 1)

        combined = (combined.astype(np.float32) * vig).astype(np.uint8)

        # Warm tint on dark background
        result = np.full((h, w, 3), [12, 10, 8], dtype=np.uint8)  # near-black BG
        line_color = np.array([185, 200, 220], dtype=np.uint8)  # warm cream
        mask = combined > 20
        for c in range(3):
            ch = result[:, :, c].copy()
            ch[mask] = np.clip(
                combined[mask].astype(np.float32) / 255.0 * line_color[c], 0, 255
            ).astype(np.uint8)
            result[:, :, c] = ch

        return result

    def _living_sketch(self, img: np.ndarray, analysis: dict) -> np.ndarray:
        """Wet-ink pencil sketch with wash & splatter effects."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Pencil-sketch: divide by inverted blur
        inv = cv2.bitwise_not(gray)
        inv_blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, cv2.bitwise_not(inv_blur), scale=256)

        # Ink wash — blurred dark regions
        _, dark = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY_INV)
        wash = cv2.GaussianBlur(dark, (41, 41), 0)
        wash = (wash.astype(np.float32) * 0.35).astype(np.uint8)

        combined = cv2.subtract(sketch, wash)

        # Directional motion blur (wet ink feel)
        ksize = 7
        mk = np.zeros((ksize, ksize), dtype=np.float32)
        mk[ksize // 2, :] = 1.0 / ksize
        angle = float(np.random.default_rng(42).choice([0, 30, 60, 90, 120, 150]))
        rot_mat = cv2.getRotationMatrix2D(
            (ksize / 2, ksize / 2), angle, 1.0
        )
        mk = cv2.warpAffine(mk, rot_mat, (ksize, ksize))
        s = mk.sum()
        if s > 0:
            mk /= s

        edges = cv2.Canny(gray, 50, 150)
        edge_blur = cv2.filter2D(edges, -1, mk)
        combined = cv2.subtract(combined, (edge_blur * 0.12).astype(np.uint8))

        # Ink splatters
        rng = np.random.default_rng(42)
        for _ in range(rng.integers(8, 25)):
            sx = int(rng.integers(0, w))
            sy = int(rng.integers(0, h))
            sr = int(rng.integers(1, 5))
            sd = int(rng.integers(170, 230))
            cv2.circle(combined, (sx, sy), sr, sd, -1)

        # Warm paper tint
        paper_b, paper_g, paper_r = 218, 228, 238
        f = combined.astype(np.float32) / 255.0
        result = np.zeros((h, w, 3), dtype=np.uint8)
        result[:, :, 0] = (f * paper_b).astype(np.uint8)
        result[:, :, 1] = (f * paper_g).astype(np.uint8)
        result[:, :, 2] = (f * paper_r).astype(np.uint8)

        return result
