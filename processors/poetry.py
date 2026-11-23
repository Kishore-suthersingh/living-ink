"""
Poetry Generator — Creates evocative micro-poems from pattern analysis.

Builds atmospheric, nature-inspired text that describes the "soul"
of the organic patterns found in the uploaded image.
"""

import random


class PoetryGenerator:
    """Generates short poetic descriptions from pattern analysis data."""

    def generate(self, analysis: dict, style: str = "tattoo") -> str:
        """
        Create a poetic description based on the pattern analysis.

        Args:
            analysis: dict from PatternAnalyzer.analyze()
            style: the selected art style key

        Returns:
            A short evocative poem / description string.
        """
        patterns = analysis.get("dominant_patterns", ["organic forms"])
        density = analysis.get("density", "moderate")
        flow = analysis.get("flow_direction", "organic")
        complexity = analysis.get("complexity", 0.5)
        texture = analysis.get("texture_frequency", "medium")
        branching = analysis.get("branching_score", 0.0)

        opening = random.choice(self._openings(patterns))
        middle = random.choice(self._middles(flow, density, branching))
        closing = random.choice(self._closings(complexity, texture, style))

        return f"{opening} {middle} {closing}"

    # ------------------------------------------------------------- templates

    @staticmethod
    def _openings(patterns: list) -> list:
        """Pattern-specific opening lines."""
        lines = []

        pattern_set = set(patterns)

        if "branching structures" in pattern_set:
            lines += [
                "Where roots once whispered to the dark earth,",
                "A thousand tributaries of silence converge —",
                "The tree remembers every path it chose,",
                "Branching outward like a question with no single answer,",
            ]
        if "intricate textures" in pattern_set:
            lines += [
                "Woven by hands older than language,",
                "Every thread of this surface holds a century,",
                "The fabric of the earth, unraveled and resung,",
                "In the weave of stone and time,",
            ]
        if "cellular patterns" in pattern_set:
            lines += [
                "A hidden city mapped in living cells,",
                "Each chamber holds a breath the world forgot,",
                "The geometry of growth, repeated infinitely,",
                "Under the skin of the world, a mosaic breathes,",
            ]
        if "flowing lines" in pattern_set:
            lines += [
                "Water wrote this story on sleeping stone,",
                "The current left its signature in silence,",
                "Flowing like a river that forgot how to stop,",
                "Lines drawn by the patient hand of wind,",
            ]
        if "radial patterns" in pattern_set:
            lines += [
                "From a single point, the universe expanded,",
                "Radiating outward like a slow explosion of becoming,",
                "The center holds everything the edges have forgotten,",
                "Spiraling outward in the language of galaxies,",
            ]
        if "crack patterns" in pattern_set:
            lines += [
                "The earth split open to show its veins,",
                "Fractures that speak of pressure, patience, release,",
                "Each crack a letter in the alphabet of erosion,",
                "Broken open, the surface reveals its inner geography,",
            ]
        if "smooth gradients" in pattern_set:
            lines += [
                "Softness carved by millennia of wind,",
                "The gentlest erosion leaves the deepest marks,",
                "Where nothing seems to happen, everything transforms,",
                "In the quiet gradient between light and shadow,",
            ]
        if "vein networks" in pattern_set:
            lines += [
                "A map of rivers too small for any atlas,",
                "Life chose these paths long before memory,",
                "The veins of a leaf mirror the rivers of a continent,",
                "Connected, always connected — that is the law of living things,",
            ]

        if not lines:
            lines = [
                "Nature carved this in a language we almost remember,",
                "The organic world speaks in patterns we feel but cannot name,",
                "Something ancient moves through these forms,",
                "The earth wrote this with no audience in mind,",
            ]

        return lines

    @staticmethod
    def _middles(flow: str, density: str, branching: float) -> list:
        """Flow and density-specific middle phrases."""
        lines = []

        # Flow-based
        flow_lines = {
            "horizontal": [
                "stretching across the horizon like a held breath,",
                "layered in the calm geometry of still water,",
                "each line a horizon, each horizon a promise,",
            ],
            "vertical": [
                "rising like smoke from the memory of fire,",
                "drawn upward by some invisible devotion,",
                "ascending in the quiet grammar of growth,",
            ],
            "diagonal": [
                "leaning into the wind that shaped it,",
                "angled like a conversation between earth and sky,",
                "tilted by forces that move in centuries,",
            ],
            "radial": [
                "spreading outward from a secret center,",
                "echoing the first ripple in the first pond,",
                "each ring a year, a breath, a turning,",
            ],
            "organic": [
                "wandering like thought through an open field,",
                "following no ruler but the logic of living,",
                "curving in the way only nature can decide,",
            ],
        }
        lines += flow_lines.get(flow, flow_lines["organic"])

        # Density-based additions
        if density == "dense":
            lines += [
                "dense as a forest floor in deep autumn,",
                "layered with the urgency of a world that never stops growing,",
            ]
        elif density == "sparse":
            lines += [
                "spare and essential as a desert psalm,",
                "stripped to the bone of beauty,",
            ]

        # Branching-based additions
        if branching > 0.6:
            lines.append(
                "every fork a decision the organism made and kept,"
            )

        return lines

    @staticmethod
    def _closings(complexity: float, texture: str, style: str) -> list:
        """Complexity and style-specific closing lines."""
        lines = []

        # Style-specific closings
        style_closings = {
            "tattoo": [
                "now translated into permanent ink — a covenant with form.",
                "ready to live on skin, as close to the body as a second pulse.",
                "the kind of mark that means something you can't quite say.",
                "etched in ink, it becomes a promise worn on the body.",
            ],
            "abstract": [
                "dissolved into pure emotion and color.",
                "abstracted until only the feeling remains.",
                "the essence, distilled — no longer a thing, but a sensation.",
                "freed from form, it becomes something you feel rather than see.",
            ],
            "sacred_geometry": [
                "revealed as the mathematics the universe dreams in.",
                "aligned with the sacred proportions hidden in all living things.",
                "the proof that nature and geometry share the same mother tongue.",
                "where the organic meets the eternal, in golden silence.",
            ],
            "minimalist": [
                "reduced to a single breath of line.",
                "simplified until only truth remains.",
                "the quietest version of itself — and therefore the loudest.",
                "distilled to the point where less becomes everything.",
            ],
            "dark_botanical": [
                "blooming in darkness, where all real growth begins.",
                "rendered in shadow, where beauty takes its most honest form.",
                "dark and intricate as a midnight garden.",
                "where the occult and the organic share a single stem.",
            ],
            "living_sketch": [
                "still wet, still breathing, still becoming.",
                "drawn in ink that refuses to dry — always in motion.",
                "a sketch that lives, trembles, and breathes on the page.",
                "captured mid-flow, as if the ink itself were alive.",
            ],
        }
        lines += style_closings.get(style, style_closings["tattoo"])

        # Complexity additions
        if complexity > 0.7:
            lines += [
                "complex as a conversation between centuries.",
                "intricate enough to get lost in — and want to stay.",
            ]
        elif complexity < 0.3:
            lines += [
                "simple as a stone at the bottom of a clear river.",
                "quiet as the space between heartbeats.",
            ]

        return lines
