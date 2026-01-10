#!/usr/bin/env python3
"""
Phase 3 Diagram Generator - Specialized Visualizations

Generates SVG diagrams for:
- Venn Diagrams (2-set and 3-set)
- Flowcharts
- Timelines
- Electrical circuits (basic series layout)
- Logic circuits (basic gates)
- Molecular structures (simple radial layout)
- Chemical reactions (reactants → products)

This module provides a `Phase3Generator` with methods to render
each diagram type to SVG, a routing method `generate_from_spec()`,
and a `main()` that loads specs, generates diagrams, and writes a manifest.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
from datetime import datetime
import hashlib
import json
import sys


# ----------------------
# Data Structures
# ----------------------

@dataclass
class DiagramSpec:
    diagram_type: str
    lesson_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    title: str = ""
    subject: str = ""


# ----------------------
# Generator
# ----------------------

class Phase3Generator:
    def __init__(self, output_dir: str | Path = "generated_assets") -> None:
        self.output_dir: Path = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated: List[Dict[str, Any]] = []

    # ----------------------
    # Venn Diagrams (2-set)
    # ----------------------
    def create_venn_diagram_2(
        self,
        set_a_label: str,
        set_b_label: str,
        only_a: Any = "",
        both: Any = "",
        only_b: Any = "",
        title: str = "Two-Set Venn Diagram",
    ) -> str:
        """Return SVG for a simple two-set Venn diagram.

        Parameters represent labels and optional values displayed in regions.
        """
        width, height = 400, 320
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>

  <!-- Circles -->
  <circle cx="150" cy="160" r="90" fill="#3498db" opacity="0.35" stroke="#2980b9" stroke-width="3"/>
  <circle cx="250" cy="160" r="90" fill="#e74c3c" opacity="0.35" stroke="#c0392b" stroke-width="3"/>

  <!-- Labels -->
  <text x="105" y="90" text-anchor="middle" font-size="14" font-weight="bold" fill="#2c3e50">{set_a_label}</text>
  <text x="295" y="90" text-anchor="middle" font-size="14" font-weight="bold" fill="#2c3e50">{set_b_label}</text>

  <!-- Region Values -->
  <text x="105" y="165" text-anchor="middle" font-size="13" fill="#1a1a1a">{only_a}</text>
  <text x="200" y="165" text-anchor="middle" font-size="13" font-weight="bold" fill="#1a1a1a">{both}</text>
  <text x="295" y="165" text-anchor="middle" font-size="13" fill="#1a1a1a">{only_b}</text>

  <text x="{width/2}" y="300" text-anchor="middle" font-size="12" fill="#666">Intersection shown in center</text>
</svg>"""
        return svg

    # ----------------------
    # Venn Diagrams (3-set)
    # ----------------------
    def create_venn_diagram_3(
        self,
        set_a_label: str,
        set_b_label: str,
        set_c_label: str,
        title: str = "Three-Set Venn Diagram",
    ) -> str:
        """Return SVG for a simple three-set Venn diagram."""
        width, height = 460, 360
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>

  <!-- Circles -->
  <circle cx="170" cy="170" r="90" fill="#3498db" opacity="0.35" stroke="#2980b9" stroke-width="3"/>
  <circle cx="290" cy="170" r="90" fill="#e74c3c" opacity="0.35" stroke="#c0392b" stroke-width="3"/>
  <circle cx="230" cy="240" r="90" fill="#2ecc71" opacity="0.35" stroke="#27ae60" stroke-width="3"/>

  <!-- Labels -->
  <text x="120" y="95" text-anchor="middle" font-size="14" font-weight="bold" fill="#2c3e50">{set_a_label}</text>
  <text x="340" y="95" text-anchor="middle" font-size="14" font-weight="bold" fill="#2c3e50">{set_b_label}</text>
  <text x="230" y="330" text-anchor="middle" font-size="14" font-weight="bold" fill="#2c3e50">{set_c_label}</text>

  <!-- Center intersection marker -->
  <text x="230" y="205" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a1a1a">A∩B∩C</text>
</svg>"""
        return svg

    # ----------------------
    # Flowchart
    # ----------------------
    def create_flowchart(
        self,
        steps: List[Dict[str, str]],
        title: str = "Process Flowchart",
    ) -> str:
        """Return SVG for a simple vertical flowchart.

        steps: list of dicts with keys: {type: start|process|decision|end, text: str}
        """
        width = 420
        height = 140 + (len(steps) * 100)
        y0 = 80

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
            '<defs>\n    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto">\n      <polygon points="0 0, 10 3, 0 6" fill="#555"/>\n    </marker>\n  </defs>',
        ]

        for i, step in enumerate(steps):
            stype = step.get("type", "process").lower()
            text = step.get("text", "")
            y = y0 + (i * 100)

            if stype in {"start", "end"}:
                parts.append(f'<rect x="160" y="{y}" width="100" height="40" rx="20" fill="#27ae60" stroke="#1e8449" stroke-width="2"/>')
                parts.append(f'<text x="210" y="{y+25}" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">{text}</text>')
            elif stype == "decision":
                parts.append(f'<polygon points="210,{y} 290,{y+30} 210,{y+60} 130,{y+30}" fill="#f39c12" stroke="#d68910" stroke-width="2"/>')
                parts.append(f'<text x="210" y="{y+35}" text-anchor="middle" font-size="11" font-weight="bold" fill="#fff">{text}</text>')
            else:
                parts.append(f'<rect x="160" y="{y}" width="100" height="40" fill="#3498db" stroke="#2980b9" stroke-width="2"/>')
                parts.append(f'<text x="210" y="{y+25}" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">{text}</text>')

            if i < len(steps) - 1:
                parts.append(f'<line x1="210" y1="{y+40}" x2="210" y2="{y+60}" stroke="#555" stroke-width="2" marker-end="url(#arrowhead)"/>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Timeline
    # ----------------------
    def create_timeline(
        self,
        events: List[Dict[str, str]],
        title: str = "Timeline",
    ) -> str:
        """Return SVG for a simple horizontal timeline.

        events: list of dicts with keys {year: str, event: str}
        """
        width, height = 820, 220
        line_y, margin = 110, 60
        line_w = width - (2 * margin)

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
            f'<line x1="{margin}" y1="{line_y}" x2="{width-margin}" y2="{line_y}" stroke="#34495e" stroke-width="3"/>'
        ]

        if events:
            spacing = line_w / (len(events) - 1) if len(events) > 1 else 0
            for i, ev in enumerate(events):
                x = margin + (i * spacing)
                year = ev.get("year", "")
                text = ev.get("event", ev.get("label", ""))

                parts.append(f'<circle cx="{x}" cy="{line_y}" r="8" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>')
                parts.append(f'<text x="{x}" y="{line_y-20}" text-anchor="middle" font-size="12" font-weight="bold" fill="#2c3e50">{year}</text>')

                words = text.split()
                if len(words) <= 4:
                    parts.append(f'<text x="{x}" y="{line_y+26}" text-anchor="middle" font-size="10" fill="#555">{text}</text>')
                else:
                    mid = len(words) // 2
                    line1 = " ".join(words[:mid])
                    line2 = " ".join(words[mid:])
                    parts.append(f'<text x="{x}" y="{line_y+26}" text-anchor="middle" font-size="10" fill="#555">{line1}</text>')
                    parts.append(f'<text x="{x}" y="{line_y+42}" text-anchor="middle" font-size="10" fill="#555">{line2}</text>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Electrical Circuit
    # ----------------------
    def create_electrical_circuit(
        self,
        components: List[Dict[str, str]],
        connections: str = "series",
        title: str = "Electrical Circuit",
    ) -> str:
        """Return SVG for a basic electrical circuit diagram.

        Supports a simple horizontal series path with basic component glyphs.
        components: list of dicts with keys {type: battery|resistor|lamp, label, value}
        """
        width, height = 560, 280
        y = 150
        x0 = 50
        x_spacing = 130

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
            f'<line x1="{x0}" y1="{y}" x2="{x0 + max(1,len(components)) * x_spacing}" y2="{y}" stroke="#333" stroke-width="2"/>'
        ]

        for i, comp in enumerate(components):
            x = x0 + (i * x_spacing)
            ctype = comp.get("type", "resistor").lower()
            label = comp.get("label", ctype.title())
            value = comp.get("value", "")

            if ctype == "battery":
                parts.append(f'<line x1="{x-8}" y1="{y-18}" x2="{x-8}" y2="{y+18}" stroke="#e74c3c" stroke-width="4"/>')
                parts.append(f'<line x1="{x+8}" y1="{y-12}" x2="{x+8}" y2="{y+12}" stroke="#e74c3c" stroke-width="3"/>')
            elif ctype == "lamp":
                parts.append(f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="#f1c40f" stroke-width="3"/>')
                parts.append(f'<line x1="{x-12}" y1="{y-12}" x2="{x+12}" y2="{y+12}" stroke="#f1c40f" stroke-width="2"/>')
                parts.append(f'<line x1="{x-12}" y1="{y+12}" x2="{x+12}" y2="{y-12}" stroke="#f1c40f" stroke-width="2"/>')
            else:  # resistor
                path = f'M{x-22},{y} l10,-10 l10,20 l10,-20 l10,20 l10,-10'
                parts.append(f'<path d="{path}" fill="none" stroke="#2980b9" stroke-width="2"/>')

            parts.append(f'<text x="{x}" y="{y-28}" text-anchor="middle" font-size="11" font-weight="bold" fill="#2c3e50">{label}</text>')
            if value:
                parts.append(f'<text x="{x}" y="{y+32}" text-anchor="middle" font-size="10" fill="#555">{value}</text>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Logic Circuit
    # ----------------------
    def create_logic_circuit(
        self,
        gates: List[Dict[str, Any]],
        title: str = "Logic Circuit",
    ) -> str:
        """Return SVG for a simple logic gate chain with labels."""
        width, height = 520, 300
        y0 = 90

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
        ]

        for i, gate in enumerate(gates):
            gtype = gate.get("type", "AND").upper()
            inputs = gate.get("inputs", ["A", "B"])
            output = gate.get("output", f"Q{i+1}")
            y = y0 + (i * 80)

            # Inputs
            parts.append(f'<text x="40" y="{y+12}" font-size="12" fill="#333">{inputs[0]}</text>')
            parts.append(f'<line x1="60" y1="{y+8}" x2="{100}" y2="{y+8}" stroke="#333" stroke-width="2"/>')
            if len(inputs) > 1:
                parts.append(f'<text x="40" y="{y+32}" font-size="12" fill="#333">{inputs[1]}</text>')
                parts.append(f'<line x1="60" y1="{y+28}" x2="{100}" y2="{y+28}" stroke="#333" stroke-width="2"/>')

            # Gate body (rounded rect with label)
            parts.append(f'<rect x="100" y="{y}" width="80" height="40" rx="8" fill="none" stroke="#2980b9" stroke-width="2"/>')
            parts.append(f'<text x="140" y="{y+24}" text-anchor="middle" font-size="12" font-weight="bold" fill="#2980b9">{gtype}</text>')

            # Output
            parts.append(f'<line x1="{180}" y1="{y+20}" x2="{240}" y2="{y+20}" stroke="#333" stroke-width="2"/>')
            parts.append(f'<text x="{250}" y="{y+25}" font-size="12" font-weight="bold" fill="#333">{output}</text>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Molecular Structure
    # ----------------------
    def create_molecular_structure(
        self,
        formula: str,
        atoms: List[Tuple[str, int]],
        title: str = "Molecular Structure",
    ) -> str:
        """Return SVG for a simple radial molecular diagram.

        atoms: list of (symbol, count) tuples; only symbols used for display.
        """
        width, height = 380, 320
        cx, cy = width / 2, height / 2

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
            f'<text x="{width/2}" y="50" text-anchor="middle" font-size="14" fill="#666">{formula}</text>',
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>',
        ]

        center_symbol = atoms[0][0] if atoms else "C"
        parts.append(f'<text x="{cx}" y="{cy+8}" text-anchor="middle" font-size="16" font-weight="bold" fill="#fff">{center_symbol}</text>')

        # Place up to 6 peripheral atoms around
        radius = 80
        peripheral = atoms[1:7]
        for i, (sym, _count) in enumerate(peripheral):
            angle = (i / max(1, len(peripheral))) * 2 * 3.14159
            px = cx + radius * 0.85 * float(__import__('math').cos(angle))
            py = cy + radius * 0.85 * float(__import__('math').sin(angle))
            parts.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#7f8c8d" stroke-width="2"/>')
            parts.append(f'<circle cx="{px}" cy="{py}" r="20" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>')
            parts.append(f'<text x="{px}" y="{py+6}" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">{sym}</text>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Chemical Reaction
    # ----------------------
    def create_chemical_reaction(
        self,
        reactants: List[str],
        products: List[str],
        reaction_type: str = "synthesis",
        title: str = "Chemical Reaction",
    ) -> str:
        """Return SVG for a simple reaction arrow with labels."""
        width, height = 560, 220
        cy = height / 2

        parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>',
            '<defs><marker id="arrow-reaction" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">\n              <polygon points="0 0, 10 3, 0 6" fill="#e74c3c"/>\n            </marker></defs>'
        ]

        left = ", ".join(reactants) if reactants else "Reactants"
        right = ", ".join(products) if products else "Products"

        parts.append(f'<rect x="40" y="{cy-18}" width="150" height="36" rx="6" fill="#3498db" stroke="#2980b9" stroke-width="2"/>')
        parts.append(f'<text x="115" y="{cy+6}" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">{left}</text>')

        parts.append(f'<line x1="210" y1="{cy}" x2="360" y2="{cy}" stroke="#e74c3c" stroke-width="3" marker-end="url(#arrow-reaction)"/>')
        parts.append(f'<text x="285" y="{cy-12}" text-anchor="middle" font-size="11" fill="#e74c3c">{reaction_type}</text>')

        parts.append(f'<rect x="380" y="{cy-18}" width="150" height="36" rx="6" fill="#27ae60" stroke="#229954" stroke-width="2"/>')
        parts.append(f'<text x="455" y="{cy+6}" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">{right}</text>')

        parts.append("</svg>")
        return "\n".join(parts)

    # ----------------------
    # Routing & I/O
    # ----------------------
    def generate_from_spec(self, spec: DiagramSpec) -> str:
        """Route a `DiagramSpec` to the appropriate generator method."""
        dtype = spec.diagram_type
        data = spec.data or {}

        if dtype == "venn_2":
            return self.create_venn_diagram_2(**data)
        if dtype == "venn_3":
            return self.create_venn_diagram_3(**data)
        if dtype == "flowchart":
            return self.create_flowchart(**data)
        if dtype == "timeline":
            return self.create_timeline(**data)
        if dtype == "circuit_electrical":
            return self.create_electrical_circuit(**data)
        if dtype == "circuit_logic":
            return self.create_logic_circuit(**data)
        if dtype == "chemistry_molecular":
            return self.create_molecular_structure(**data)
        if dtype == "chemistry_reaction":
            return self.create_chemical_reaction(**data)

        raise ValueError(f"Unknown diagram type: {dtype}")

    def save_diagram(self, spec: DiagramSpec, svg_content: str) -> Dict[str, Any]:
        """Save SVG diagram and return metadata record."""
        digest = hashlib.md5(
            f"{spec.lesson_id}_{spec.diagram_type}_{spec.title}".encode("utf-8")
        ).hexdigest()[:8]
        filename = f"{spec.diagram_type}_{spec.lesson_id}_{digest}.svg".replace(" ", "_")
        filepath = self.output_dir / filename

        with filepath.open("w", encoding="utf-8") as f:
            f.write(svg_content)

        meta = {
            "id": f"{spec.diagram_type}_{digest}",
            "lesson_id": spec.lesson_id,
            "type": spec.diagram_type,
            "title": spec.title,
            "subject": spec.subject,
            "path": str(filepath),
            "generated_at": datetime.now().isoformat(),
        }
        self.generated.append(meta)
        return meta

    def generate_all_diagrams(self, specs: List[DiagramSpec]) -> List[Dict[str, Any]]:
        """Generate all diagrams from a list of specs."""
        print(f"Generating {len(specs)} diagrams...")
        for i, spec in enumerate(specs, 1):
            try:
                svg = self.generate_from_spec(spec)
                self.save_diagram(spec, svg)
                print(f"  [{i}/{len(specs)}] Generated: {spec.diagram_type} for {spec.lesson_id}")
            except Exception as exc:
                print(f"  [{i}/{len(specs)}] Error generating {spec.diagram_type}: {exc}")
        print(f"\n✓ Generated {len(self.generated)} diagrams")
        return self.generated

    def create_manifest(self, output_file: str = "generated_assets/phase3_manifest.json") -> None:
        """Write a manifest JSON summarizing generated diagrams."""
        manifest = {
            "venn_diagrams": [],
            "flowcharts": [],
            "timelines": [],
            "electrical_circuits": [],
            "logic_circuits": [],
            "molecular_structures": [],
            "chemical_reactions": [],
        }

        for item in self.generated:
            dtype = item.get("type", "")
            if dtype.startswith("venn"):
                manifest["venn_diagrams"].append(item)
            elif dtype == "flowchart":
                manifest["flowcharts"].append(item)
            elif dtype == "timeline":
                manifest["timelines"].append(item)
            elif dtype == "circuit_electrical":
                manifest["electrical_circuits"].append(item)
            elif dtype == "circuit_logic":
                manifest["logic_circuits"].append(item)
            elif dtype == "chemistry_molecular":
                manifest["molecular_structures"].append(item)
            elif dtype == "chemistry_reaction":
                manifest["chemical_reactions"].append(item)

        manifest["metadata"] = {
            "phase": 3,
            "generated_at": datetime.now().isoformat(),
            "total_diagrams": len(self.generated),
            "venn_diagrams_count": len(manifest["venn_diagrams"]),
            "flowcharts_count": len(manifest["flowcharts"]),
            "timelines_count": len(manifest["timelines"]),
            "electrical_circuits_count": len(manifest["electrical_circuits"]),
            "logic_circuits_count": len(manifest["logic_circuits"]),
            "molecular_structures_count": len(manifest["molecular_structures"]),
            "chemical_reactions_count": len(manifest["chemical_reactions"]),
        }

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Manifest saved to: {output_file}")


# ----------------------
# Samples & CLI
# ----------------------

def create_sample_diagrams() -> List[DiagramSpec]:
    """Create sample diagram specifications for testing all 8 types."""
    specs: List[DiagramSpec] = []

    # Venn 2
    specs.append(
        DiagramSpec(
            lesson_id="math_sets_sample_001",
            diagram_type="venn_2",
            title="Union of Sets A and B",
            subject="Further Mathematics",
            data={
                "set_a_label": "Set A",
                "set_b_label": "Set B",
                "only_a": 5,
                "both": 3,
                "only_b": 4,
                "title": "Union of Sets A and B",
            },
        )
    )

    # Venn 3
    specs.append(
        DiagramSpec(
            lesson_id="math_sets_sample_002",
            diagram_type="venn_3",
            title="Three-Set Intersection",
            subject="Further Mathematics",
            data={
                "set_a_label": "A",
                "set_b_label": "B",
                "set_c_label": "C",
                "title": "Venn Diagram: A, B, C",
            },
        )
    )

    # Flowchart
    specs.append(
        DiagramSpec(
            lesson_id="cs_flow_sample_001",
            diagram_type="flowchart",
            title="Algorithm Flowchart",
            subject="Computer Science",
            data={
                "steps": [
                    {"type": "start", "text": "Start"},
                    {"type": "process", "text": "Input Data"},
                    {"type": "decision", "text": "Valid?"},
                    {"type": "process", "text": "Process"},
                    {"type": "end", "text": "End"},
                ],
                "title": "Data Processing Algorithm",
            },
        )
    )

    # Timeline
    specs.append(
        DiagramSpec(
            lesson_id="history_timeline_sample_001",
            diagram_type="timeline",
            title="Historical Timeline",
            subject="History",
            data={
                "events": [
                    {"year": "1960", "event": "Nigerian Independence"},
                    {"year": "1970", "event": "End of Civil War"},
                    {"year": "1999", "event": "Return to Democracy"},
                    {"year": "2015", "event": "Democratic Transition"},
                ],
                "title": "Key Events in Nigerian History",
            },
        )
    )

    # Electrical Circuit
    specs.append(
        DiagramSpec(
            lesson_id="physics_circuit_sample_001",
            diagram_type="circuit_electrical",
            title="Series Circuit",
            subject="Physics",
            data={
                "components": [
                    {"type": "battery", "label": "+/−"},
                    {"type": "resistor", "label": "R1", "value": "10Ω"},
                    {"type": "lamp", "label": "Lamp"},
                    {"type": "resistor", "label": "R2", "value": "5Ω"},
                ],
                "connections": "series",
                "title": "Basic Series Circuit",
            },
        )
    )

    # Logic Circuit
    specs.append(
        DiagramSpec(
            lesson_id="digital_logic_sample_001",
            diagram_type="circuit_logic",
            title="Logic Chain",
            subject="Computer Science",
            data={
                "gates": [
                    {"type": "AND", "inputs": ["A", "B"], "output": "X"},
                    {"type": "OR", "inputs": ["X", "C"], "output": "Y"},
                ],
                "title": "AND then OR",
            },
        )
    )

    # Molecular Structure
    specs.append(
        DiagramSpec(
            lesson_id="chem_molecule_sample_001",
            diagram_type="chemistry_molecular",
            title="Water Molecule",
            subject="Chemistry",
            data={
                "formula": "H₂O",
                "atoms": [("O", 1), ("H", 1), ("H", 1)],
                "title": "Molecule: H2O",
            },
        )
    )

    # Chemical Reaction
    specs.append(
        DiagramSpec(
            lesson_id="chem_reaction_sample_001",
            diagram_type="chemistry_reaction",
            title="Combustion Reaction",
            subject="Chemistry",
            data={
                "reactants": ["CH₄", "2O₂"],
                "products": ["CO₂", "2H₂O"],
                "reaction_type": "combustion",
                "title": "CH4 + 2O2 → CO2 + 2H2O",
            },
        )
    )

    return specs


def main() -> int:
    """CLI entrypoint: load specs, generate diagrams, write manifest."""
    spec_file = sys.argv[1] if len(sys.argv) > 1 else None

    print("=" * 70)
    print("PHASE 3 DIAGRAM GENERATOR - SPECIALIZED VISUALIZATIONS")
    print("=" * 70)

    generator = Phase3Generator()

    if spec_file:
        try:
            with open(spec_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
            specs: List[DiagramSpec] = []
            for item in raw:
                specs.append(
                    DiagramSpec(
                        diagram_type=item.get("type") or item.get("diagram_type", ""),
                        lesson_id=item["lesson_id"],
                        data=item.get("data", {}),
                        title=item.get("title", ""),
                        subject=item.get("subject", ""),
                    )
                )
            print(f"✓ Loaded {len(specs)} specs from {spec_file}\n")
        except Exception as e:
            print(f"✗ Error loading specs: {e}")
            print("Using sample specs instead...\n")
            specs = create_sample_diagrams()
    else:
        print("No spec file provided, using sample specs...\n")
        specs = create_sample_diagrams()

    generator.generate_all_diagrams(specs)
    generator.create_manifest()

    print("\n" + "=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)
    print(f"Total diagrams generated: {len(generator.generated)}")
    print(f"Output directory: {generator.output_dir}")
    print("Manifest: generated_assets/phase3_manifest.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())

