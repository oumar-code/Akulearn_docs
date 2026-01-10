#!/usr/bin/env python3
"""Phase 2: Mathematical Graphing Engine Generator

Generates SVG graphs for:
- Mathematical functions
- Data visualizations
- Economic charts
- Geographic distributions
- Physics diagrams with data
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
import math


CONTENT_PATH = Path("content_data.json")
OUTPUT_DIR = Path("generated_assets")
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "graphs").mkdir(exist_ok=True)


class SVGGraphGenerator:
    """Generate SVG graphs for various data types."""
    
    # SVG Canvas settings
    WIDTH = 600
    HEIGHT = 400
    MARGIN = 50
    
    @staticmethod
    def create_function_graph(x_range: Tuple[float, float] = (-10, 10), 
                             func_name: str = "quadratic") -> str:
        """Generate SVG for common mathematical functions."""
        
        # Define functions
        functions = {
            "linear": lambda x: x,
            "quadratic": lambda x: x**2 / 10,
            "cubic": lambda x: x**3 / 100,
            "exponential": lambda x: (1.1 ** (x/5) - 1) * 50,
            "sine": lambda x: math.sin(x) * 10,
            "cosine": lambda x: math.cos(x) * 10,
            "logarithm": lambda x: math.log(abs(x) + 1) * 5,
            "parabola": lambda x: x**2 / 15,
        }
        
        func = functions.get(func_name, functions["quadratic"])
        x_min, x_max = x_range
        
        # Generate SVG
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" viewBox="0 0 {SVGGraphGenerator.WIDTH} {SVGGraphGenerator.HEIGHT}">',
            '<style>',
            '.axis { stroke: #333; stroke-width: 2; }',
            '.grid { stroke: #ddd; stroke-width: 0.5; }',
            '.curve { stroke: #2980b9; stroke-width: 2.5; fill: none; }',
            '.label { font-size: 12px; fill: #333; font-family: Arial; }',
            '</style>',
            '<defs>',
            '<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">',
            '<polygon points="0 0, 10 3, 0 6" fill="#333" />',
            '</marker>',
            '</defs>',
        ]
        
        # Draw background
        svg_lines.append(f'<rect width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" fill="#f9f9f9"/>')
        
        # Draw grid
        cx, cy = SVGGraphGenerator.WIDTH // 2, SVGGraphGenerator.HEIGHT // 2
        for i in range(-10, 11):
            if i % 5 == 0:
                x = cx + i * 20
                svg_lines.append(f'<line class="grid" x1="{x}" y1="0" x2="{x}" y2="{SVGGraphGenerator.HEIGHT}"/>')
                y = cy + i * 20
                svg_lines.append(f'<line class="grid" x1="0" y1="{y}" x2="{SVGGraphGenerator.WIDTH}" y2="{y}"/>')
        
        # Draw axes
        svg_lines.append(f'<line class="axis" x1="{SVGGraphGenerator.MARGIN}" y1="{cy}" x2="{SVGGraphGenerator.WIDTH - SVGGraphGenerator.MARGIN}" y2="{cy}" marker-end="url(#arrowhead)"/>')
        svg_lines.append(f'<line class="axis" x1="{cx}" y1="{SVGGraphGenerator.MARGIN}" x2="{cx}" y2="{SVGGraphGenerator.HEIGHT - SVGGraphGenerator.MARGIN}" marker-end="url(#arrowhead)"/>')
        
        # Draw axis labels
        svg_lines.append(f'<text class="label" x="{SVGGraphGenerator.WIDTH - 40}" y="{cy - 10}">x</text>')
        svg_lines.append(f'<text class="label" x="{cx + 10}" y="{SVGGraphGenerator.MARGIN - 10}">y</text>')
        
        # Generate curve points
        points = []
        step = (x_max - x_min) / 200
        x = x_min
        while x <= x_max:
            try:
                y = func(x)
                # Scale to SVG coordinates
                svg_x = cx + (x / 10) * 20
                svg_y = cy - (y / 10) * 20
                
                # Clip to view
                if SVGGraphGenerator.MARGIN <= svg_x <= SVGGraphGenerator.WIDTH - SVGGraphGenerator.MARGIN and \
                   SVGGraphGenerator.MARGIN <= svg_y <= SVGGraphGenerator.HEIGHT - SVGGraphGenerator.MARGIN:
                    points.append(f"{svg_x},{svg_y}")
            except:
                pass
            x += step
        
        if points:
            path_data = " L ".join(points)
            svg_lines.append(f'<polyline class="curve" points="{path_data}"/>')
        
        # Add title
        svg_lines.append(f'<text class="label" x="20" y="25" font-size="14" font-weight="bold">{func_name.replace("_", " ").title()}</text>')
        
        svg_lines.append('</svg>')
        
        return "\n".join(svg_lines)
    
    @staticmethod
    def create_bar_chart(categories: List[str] = None, values: List[float] = None) -> str:
        """Generate SVG bar chart."""
        if not categories:
            categories = ["Category A", "Category B", "Category C", "Category D"]
        if not values:
            values = [45, 38, 52, 41]
        
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" viewBox="0 0 {SVGGraphGenerator.WIDTH} {SVGGraphGenerator.HEIGHT}">',
            '<style>',
            '.bar { fill: #3498db; }',
            '.bar:hover { fill: #2980b9; }',
            '.label { font-size: 11px; fill: #333; font-family: Arial; text-anchor: middle; }',
            '.value { font-size: 10px; fill: #555; font-family: Arial; text-anchor: middle; }',
            '.axis { stroke: #333; stroke-width: 1.5; }',
            '</style>',
            f'<rect width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" fill="#f9f9f9"/>'
        ]
        
        # Draw axes
        svg_lines.append(f'<line class="axis" x1="50" y1="50" x2="50" y2="320"/>')
        svg_lines.append(f'<line class="axis" x1="50" y1="320" x2="580" y2="320"/>')
        
        # Calculate bar width
        bar_width = (SVGGraphGenerator.WIDTH - 100) / len(categories)
        max_val = max(values) if values else 100
        
        # Draw bars
        for i, (cat, val) in enumerate(zip(categories, values)):
            x = 50 + i * bar_width + bar_width * 0.15
            bar_height = (val / max_val) * 250
            y = 320 - bar_height
            
            svg_lines.append(f'<rect class="bar" x="{x}" y="{y}" width="{bar_width * 0.7}" height="{bar_height}"/>')
            svg_lines.append(f'<text class="value" x="{x + bar_width * 0.35}" y="{y - 5}">{val}</text>')
            svg_lines.append(f'<text class="label" x="{x + bar_width * 0.35}" y="340">{cat[:10]}</text>')
        
        svg_lines.append('</svg>')
        return "\n".join(svg_lines)
    
    @staticmethod
    def create_pie_chart(labels: List[str] = None, sizes: List[float] = None) -> str:
        """Generate SVG pie chart."""
        if not labels:
            labels = ["Segment A", "Segment B", "Segment C", "Segment D"]
        if not sizes:
            sizes = [30, 25, 25, 20]
        
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" viewBox="0 0 {SVGGraphGenerator.WIDTH} {SVGGraphGenerator.HEIGHT}">',
            '<style>',
            '.slice { stroke: white; stroke-width: 2; }',
            '.label { font-size: 12px; fill: white; font-family: Arial; font-weight: bold; text-anchor: middle; }',
            '.legend { font-size: 11px; fill: #333; font-family: Arial; }',
            '</style>',
            f'<rect width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" fill="#f9f9f9"/>'
        ]
        
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
        center_x, center_y = 200, 180
        radius = 120
        
        total = sum(sizes)
        current_angle = 0
        
        for i, (label, size) in enumerate(zip(labels, sizes)):
            percentage = size / total
            slice_angle = percentage * 360
            
            # Calculate slice
            x1 = center_x + radius * math.cos(math.radians(current_angle))
            y1 = center_y + radius * math.sin(math.radians(current_angle))
            
            end_angle = current_angle + slice_angle
            x2 = center_x + radius * math.cos(math.radians(end_angle))
            y2 = center_y + radius * math.sin(math.radians(end_angle))
            
            large_arc = 1 if slice_angle > 180 else 0
            
            path_data = f"M {center_x} {center_y} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
            svg_lines.append(f'<path class="slice" d="{path_data}" fill="{colors[i % len(colors)]}"/>')
            
            # Label
            label_angle = current_angle + slice_angle / 2
            label_x = center_x + (radius * 0.65) * math.cos(math.radians(label_angle))
            label_y = center_y + (radius * 0.65) * math.sin(math.radians(label_angle))
            svg_lines.append(f'<text class="label" x="{label_x}" y="{label_y}">{percentage*100:.0f}%</text>')
            
            current_angle = end_angle
        
        # Legend
        legend_x = 360
        for i, label in enumerate(labels):
            y = 50 + i * 30
            svg_lines.append(f'<rect x="{legend_x}" y="{y}" width="15" height="15" fill="{colors[i % len(colors)]}"/>')
            svg_lines.append(f'<text class="legend" x="{legend_x + 25}" y="{y + 12}">{label[:15]}</text>')
        
        svg_lines.append('</svg>')
        return "\n".join(svg_lines)
    
    @staticmethod
    def create_line_chart(data_points: List[Tuple[float, float]] = None) -> str:
        """Generate SVG line chart."""
        if not data_points:
            data_points = [(i, 20 + i*5 + (i % 3 - 1) * 10) for i in range(12)]
        
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" viewBox="0 0 {SVGGraphGenerator.WIDTH} {SVGGraphGenerator.HEIGHT}">',
            '<style>',
            '.line { stroke: #2980b9; stroke-width: 2.5; fill: none; }',
            '.point { fill: #2980b9; stroke: white; stroke-width: 2; }',
            '.grid { stroke: #e0e0e0; stroke-width: 0.5; }',
            '.axis { stroke: #333; stroke-width: 1.5; }',
            '.label { font-size: 11px; fill: #666; font-family: Arial; }',
            '</style>',
            f'<rect width="{SVGGraphGenerator.WIDTH}" height="{SVGGraphGenerator.HEIGHT}" fill="#f9f9f9"/>'
        ]
        
        # Get ranges
        x_vals = [p[0] for p in data_points]
        y_vals = [p[1] for p in data_points]
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)
        
        # Normalize to SVG space
        x_scale = (SVGGraphGenerator.WIDTH - 100) / max(x_max - x_min, 1)
        y_scale = (SVGGraphGenerator.HEIGHT - 100) / max(y_max - y_min, 1)
        
        points = []
        for x, y in data_points:
            svg_x = 50 + (x - x_min) * x_scale
            svg_y = SVGGraphGenerator.HEIGHT - 50 - (y - y_min) * y_scale
            points.append((svg_x, svg_y))
        
        # Draw grid and axes
        svg_lines.append(f'<line class="axis" x1="50" y1="50" x2="50" y2="{SVGGraphGenerator.HEIGHT-50}"/>')
        svg_lines.append(f'<line class="axis" x1="50" y1="{SVGGraphGenerator.HEIGHT-50}" x2="{SVGGraphGenerator.WIDTH-50}" y2="{SVGGraphGenerator.HEIGHT-50}"/>')
        
        # Draw line
        line_points = " L ".join([f"{x},{y}" for x, y in points])
        svg_lines.append(f'<polyline class="line" points="{line_points}"/>')
        
        # Draw points
        for x, y in points:
            svg_lines.append(f'<circle class="point" cx="{x}" cy="{y}" r="4"/>')
        
        svg_lines.append('</svg>')
        return "\n".join(svg_lines)


def generate_phase2():
    """Generate Phase 2 assets for all applicable lessons."""
    
    # Load content
    with CONTENT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    lessons = data.get("content", [])
    
    # Load analysis
    try:
        with Path("graphable_content_report.json").open("r") as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print("Error: Run phase2_analyzer.py first")
        return
    
    graph_gen = SVGGraphGenerator()
    
    results = {
        "function_graphs": [],
        "bar_charts": [],
        "pie_charts": [],
        "line_charts": [],
        "generated_at": Path(__file__).stem,
        "total_lessons": len(lessons),
    }
    
    print("\n" + "="*70)
    print("PHASE 2: MATHEMATICAL GRAPHING ENGINE GENERATION")
    print("="*70 + "\n")
    
    graph_count = 0
    
    # Generate graphs for high-priority lessons
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        
        lesson_id = lesson.get("id", "unknown")
        title = lesson.get("title", "Untitled")
        subject = lesson.get("subject", "Unknown")
        
        # Get graph types for this lesson
        graph_types = None
        for hp in analysis.get("high_priority", []):
            if hp.get("id") == lesson_id:
                graph_types = hp.get("categories", [])
                break
        
        if not graph_types:
            continue
        
        # Generate appropriate graphs
        for graph_type in graph_types:
            if graph_type == "function_graphs":
                for func_type in ["quadratic", "sine", "exponential"]:
                    svg = graph_gen.create_function_graph(func_name=func_type)
                    graph_path = OUTPUT_DIR / "graphs" / f"{lesson_id}_{graph_type}_{func_type}.svg"
                    with graph_path.open("w", encoding="utf-8") as f:
                        f.write(svg)
                    
                    results["function_graphs"].append({
                        "lesson_id": lesson_id,
                        "title": title,
                        "subject": subject,
                        "type": func_type,
                        "path": str(graph_path),
                    })
                    graph_count += 1
            
            elif graph_type == "bar_chart":
                svg = graph_gen.create_bar_chart()
                graph_path = OUTPUT_DIR / "graphs" / f"{lesson_id}_bar_chart.svg"
                with graph_path.open("w", encoding="utf-8") as f:
                    f.write(svg)
                
                results["bar_charts"].append({
                    "lesson_id": lesson_id,
                    "title": title,
                    "subject": subject,
                    "path": str(graph_path),
                })
                graph_count += 1
            
            elif graph_type == "pie_chart":
                svg = graph_gen.create_pie_chart()
                graph_path = OUTPUT_DIR / "graphs" / f"{lesson_id}_pie_chart.svg"
                with graph_path.open("w", encoding="utf-8") as f:
                    f.write(svg)
                
                results["pie_charts"].append({
                    "lesson_id": lesson_id,
                    "title": title,
                    "subject": subject,
                    "path": str(graph_path),
                })
                graph_count += 1
            
            elif graph_type in ["line_chart", "area_chart", "scatter_plot"]:
                svg = graph_gen.create_line_chart()
                graph_type_name = graph_type.replace("_chart", "").replace("_plot", "")
                graph_path = OUTPUT_DIR / "graphs" / f"{lesson_id}_{graph_type_name}.svg"
                with graph_path.open("w", encoding="utf-8") as f:
                    f.write(svg)
                
                results["line_charts"].append({
                    "lesson_id": lesson_id,
                    "title": title,
                    "subject": subject,
                    "type": graph_type_name,
                    "path": str(graph_path),
                })
                graph_count += 1
    
    # Save manifest
    manifest_path = OUTPUT_DIR / "phase2_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("="*70)
    print(f"Graphs Generated: {graph_count}")
    print(f"Function Graphs: {len(results['function_graphs'])}")
    print(f"Bar Charts: {len(results['bar_charts'])}")
    print(f"Pie Charts: {len(results['pie_charts'])}")
    print(f"Line Charts: {len(results['line_charts'])}")
    print("="*70)
    print(f"📄 Manifest saved to: {manifest_path}\n")


if __name__ == "__main__":
    generate_phase2()
