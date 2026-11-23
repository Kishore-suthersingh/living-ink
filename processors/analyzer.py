"""
Pattern Analyzer — Detects and classifies organic patterns in nature photos.

Extracts: flow direction, branching structures, texture frequency,
edge density, contour complexity, and dominant pattern types.
"""

import cv2
import numpy as np


class PatternAnalyzer:
    """Analyzes natural images to extract organic pattern signatures."""

    def analyze(self, image_path: str) -> dict:
        """
        Run full pattern analysis on an image.

        Returns a dictionary with:
            - dominant_patterns: list of detected pattern type strings
            - complexity: 0.0–1.0 overall complexity score
            - flow_direction: dominant directional flow
            - density: 'sparse' | 'moderate' | 'dense'
            - edge_density: ratio of edge pixels
            - contour_count: total contours found
            - branching_score: 0.0–1.0 hierarchy depth
            - texture_frequency: 'coarse' | 'medium' | 'fine'
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")

        # Resize for consistent analysis (max 1024px on longest side)
        h, w = img.shape[:2]
        max_dim = 1024
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Edge detection ---
        edges = cv2.Canny(gray, 50, 150)
        edge_density = float(np.count_nonzero(edges)) / edges.size

        # --- Contour analysis ---
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        contour_count = len(contours)

        # --- Branching depth ---
        branching_score = self._compute_branching(hierarchy)

        # --- Flow direction ---
        flow_direction = self._detect_flow(edges)

        # --- Texture frequency ---
        texture_frequency = self._analyze_texture(gray)

        # --- Classify dominant patterns ---
        dominant_patterns = self._classify_patterns(
            edge_density, contour_count, branching_score, flow_direction
        )

        # --- Complexity score ---
        complexity = min(
            1.0,
            (edge_density * 5 + min(contour_count / 800, 1.0) + branching_score) / 3,
        )

        # --- Density label ---
        if edge_density > 0.15:
            density = "dense"
        elif edge_density > 0.05:
            density = "moderate"
        else:
            density = "sparse"

        return {
            "dominant_patterns": dominant_patterns,
            "complexity": round(complexity, 2),
            "flow_direction": flow_direction,
            "density": density,
            "edge_density": round(edge_density, 4),
            "contour_count": contour_count,
            "branching_score": round(branching_score, 2),
            "texture_frequency": texture_frequency,
        }

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _compute_branching(hierarchy) -> float:
        """Measure hierarchy depth as a proxy for branching structures."""
        if hierarchy is None:
            return 0.0
        h = hierarchy[0]
        max_depth = 0
        for i in range(len(h)):
            depth = 0
            parent = h[i][3]
            while parent != -1 and depth < 20:
                depth += 1
                parent = h[parent][3]
            max_depth = max(max_depth, depth)
        return min(1.0, max_depth / 6.0)

    @staticmethod
    def _detect_flow(edges) -> str:
        """Detect dominant directional flow using Hough line segments."""
        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10
        )
        if lines is None or len(lines) == 0:
            return "organic"

        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1)) % 180
            angles.append(angle)

        std_angle = float(np.std(angles))
        mean_angle = float(np.mean(angles))

        if std_angle > 50:
            return "radial"
        elif std_angle > 35:
            return "organic"
        elif mean_angle < 30 or mean_angle > 150:
            return "horizontal"
        elif 60 < mean_angle < 120:
            return "vertical"
        else:
            return "diagonal"

    @staticmethod
    def _analyze_texture(gray) -> str:
        """Classify texture frequency using FFT energy distribution."""
        f_transform = np.fft.fft2(gray.astype(np.float32))
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.log(np.abs(f_shift) + 1)

        h, w = magnitude.shape
        ch, cw = h // 2, w // 2
        r = min(h, w) // 8

        low_freq = float(np.mean(magnitude[ch - r : ch + r, cw - r : cw + r]))
        total = float(np.mean(magnitude))
        high_freq = total - low_freq * (4 * r * r) / (h * w)

        ratio = high_freq / (low_freq + 1e-6)

        if ratio > 0.5:
            return "fine"
        elif ratio > 0.2:
            return "medium"
        else:
            return "coarse"

    @staticmethod
    def _classify_patterns(
        edge_density: float,
        contour_count: int,
        branching_score: float,
        flow_direction: str,
    ) -> list:
        """Return up to 4 dominant pattern type labels."""
        patterns = []

        if branching_score > 0.4:
            patterns.append("branching structures")
        if edge_density > 0.12:
            patterns.append("intricate textures")
        if contour_count > 500:
            patterns.append("cellular patterns")
        if flow_direction in ("horizontal", "vertical"):
            patterns.append("flowing lines")
        if flow_direction == "radial":
            patterns.append("radial patterns")
        if edge_density > 0.08 and contour_count > 200:
            patterns.append("crack patterns")
        if edge_density < 0.04:
            patterns.append("smooth gradients")
        if branching_score > 0.2 and contour_count > 300:
            patterns.append("vein networks")

        if not patterns:
            patterns.append("organic forms")

        return patterns[:4]
