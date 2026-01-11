"""
Mathematics Diagrams Generator
Generates mathematical diagrams for educational lessons
- Trigonometric functions
- Quadratic equations
- Circle theorems
- Statistical plots
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MathDiagramGenerator:
    """Generate mathematical diagrams for lessons"""
    
    def __init__(self, output_dir="generated_assets/math_diagrams"):
        """
        Initialize math diagram generator
        
        Args:
            output_dir: Directory to save generated diagrams
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"MathDiagramGenerator initialized: {self.output_dir}")
    
    def generate_trigonometric_functions(self) -> str:
        """Generate sine, cosine, tangent graphs"""
        try:
            fig, axes = plt.subplots(3, 1, figsize=(12, 10))
            x = np.linspace(-2*np.pi, 2*np.pi, 1000)
            
            # Sine wave
            axes[0].plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
            axes[0].grid(True, alpha=0.3)
            axes[0].axhline(y=0, color='k', linewidth=0.5)
            axes[0].axvline(x=0, color='k', linewidth=0.5)
            axes[0].set_ylabel('y', fontsize=12)
            axes[0].set_title('Sine Function: y = sin(x)', fontsize=14, fontweight='bold')
            axes[0].legend(fontsize=10)
            axes[0].set_ylim(-1.5, 1.5)
            
            # Cosine wave
            axes[1].plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
            axes[1].grid(True, alpha=0.3)
            axes[1].axhline(y=0, color='k', linewidth=0.5)
            axes[1].axvline(x=0, color='k', linewidth=0.5)
            axes[1].set_ylabel('y', fontsize=12)
            axes[1].set_title('Cosine Function: y = cos(x)', fontsize=14, fontweight='bold')
            axes[1].legend(fontsize=10)
            axes[1].set_ylim(-1.5, 1.5)
            
            # Tangent wave
            axes[2].plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
            axes[2].set_ylim(-5, 5)
            axes[2].grid(True, alpha=0.3)
            axes[2].axhline(y=0, color='k', linewidth=0.5)
            axes[2].axvline(x=0, color='k', linewidth=0.5)
            axes[2].set_xlabel('x (radians)', fontsize=12)
            axes[2].set_ylabel('y', fontsize=12)
            axes[2].set_title('Tangent Function: y = tan(x)', fontsize=14, fontweight='bold')
            axes[2].legend(fontsize=10)
            
            plt.tight_layout()
            output_path = self.output_dir / "trigonometric_functions.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated trigonometric functions: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating trigonometric functions: {e}")
            raise
    
    def generate_quadratic_function(self, a: float = 1, b: float = 0, c: float = 0) -> str:
        """
        Generate parabola for quadratic equations
        
        Args:
            a: Coefficient of x²
            b: Coefficient of x
            c: Constant term
            
        Returns:
            Path to generated image
        """
        try:
            x = np.linspace(-10, 10, 500)
            y = a * x**2 + b * x + c
            
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.plot(x, y, 'b-', linewidth=2.5, label=f'y = {a}x² + {b}x + {c}')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            # Mark vertex
            vertex_x = -b / (2*a) if a != 0 else 0
            vertex_y = a * vertex_x**2 + b * vertex_x + c
            ax.plot(vertex_x, vertex_y, 'ro', markersize=10, label=f'Vertex ({vertex_x:.2f}, {vertex_y:.2f})')
            
            # Mark x-intercepts if they exist
            discriminant = b**2 - 4*a*c
            if discriminant >= 0 and a != 0:
                x1 = (-b + np.sqrt(discriminant)) / (2*a)
                x2 = (-b - np.sqrt(discriminant)) / (2*a)
                ax.plot([x1, x2], [0, 0], 'go', markersize=8, label=f'x-intercepts')
            
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.set_title('Quadratic Function: y = ax² + bx + c', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            
            output_path = self.output_dir / f"quadratic_a{a}_b{b}_c{c}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated quadratic function: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating quadratic function: {e}")
            raise
    
    def generate_circle_theorem(self) -> str:
        """Generate circle with inscribed angle theorem"""
        try:
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Draw circle
            circle = plt.Circle((0, 0), 5, fill=False, color='blue', linewidth=2.5)
            ax.add_patch(circle)
            
            # Draw inscribed angle - angle at circumference
            angles = [0, 60, 180]  # degrees
            points = [(5*np.cos(np.radians(a)), 5*np.sin(np.radians(a))) for a in angles]
            
            # Draw triangle (inscribed angle)
            triangle = plt.Polygon(points, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(triangle)
            
            # Mark points on circumference
            for i, point in enumerate(points):
                ax.plot(point[0], point[1], 'ro', markersize=10)
                offset = 0.3
                ax.text(point[0]*(1.15), point[1]*(1.15), f'P{i+1}', fontsize=14, 
                       ha='center', va='center', fontweight='bold')
            
            # Mark center
            ax.plot(0, 0, 'ko', markersize=8)
            ax.text(0.4, -0.4, 'O', fontsize=14, fontweight='bold')
            
            # Draw central angle (light)
            ax.plot([0, points[0][0]], [0, points[0][1]], 'k--', alpha=0.3, linewidth=1)
            ax.plot([0, points[2][0]], [0, points[2][1]], 'k--', alpha=0.3, linewidth=1)
            
            # Add angle arc for inscribed angle
            arc_angle = np.linspace(0, np.radians(60), 20)
            arc_r = 1.5
            ax.plot([1.5*np.cos(np.radians(180-a)) for a in np.linspace(0, 60, 20)],
                   [1.5*np.sin(np.radians(180-a)) for a in np.linspace(0, 60, 20)],
                   'r-', alpha=0.5, linewidth=1)
            
            ax.set_xlim(-7, 7)
            ax.set_ylim(-7, 7)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.2)
            ax.set_title('Circle Theorem: Inscribed Angle', fontsize=14, fontweight='bold')
            
            output_path = self.output_dir / "circle_theorem_inscribed_angle.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated circle theorem: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating circle theorem: {e}")
            raise
    
    def generate_histogram(self, data: List[float] = None, bins: int = 10, 
                          title: str = "Frequency Distribution") -> str:
        """
        Generate histogram for statistics lessons
        
        Args:
            data: Data to plot (generates random if None)
            bins: Number of bins
            title: Title of the histogram
            
        Returns:
            Path to generated image
        """
        try:
            if data is None:
                data = np.random.normal(100, 15, 1000)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            n, bins_edges, patches = ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='skyblue')
            
            # Color gradient
            cm = plt.cm.RdYlGn
            bin_centers = 0.5 * (bins_edges[:-1] + bins_edges[1:])
            col = bin_centers - min(bin_centers)
            col /= max(col)
            for c, p in zip(col, patches):
                plt.setp(p, 'facecolor', cm(c))
            
            ax.set_xlabel('Value', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add mean and median lines
            mean_val = np.mean(data)
            median_val = np.median(data)
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.1f}')
            ax.legend(fontsize=10)
            
            output_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated histogram: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating histogram: {e}")
            raise
    
    def generate_box_plot(self, datasets: List[List[float]] = None, 
                         labels: List[str] = None, title: str = "Box Plot Comparison") -> str:
        """
        Generate box plot for data analysis
        
        Args:
            datasets: List of datasets (generates random if None)
            labels: Labels for each dataset
            title: Title of the plot
            
        Returns:
            Path to generated image
        """
        try:
            if datasets is None:
                datasets = [
                    np.random.normal(100, 15, 100),
                    np.random.normal(110, 20, 100),
                    np.random.normal(95, 10, 100)
                ]
            
            if labels is None:
                labels = [f'Dataset {i+1}' for i in range(len(datasets))]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bp = ax.boxplot(datasets, labels=labels, patch_artist=True)
            
            # Color boxes
            colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
            
            ax.set_ylabel('Values', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            output_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated box plot: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating box plot: {e}")
            raise
    
    def generate_scatter_plot(self, x_data: List[float] = None, y_data: List[float] = None,
                             title: str = "Scatter Plot") -> str:
        """Generate scatter plot for correlation analysis"""
        try:
            if x_data is None or y_data is None:
                x_data = np.random.normal(100, 15, 100)
                y_data = x_data + np.random.normal(0, 10, 100)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.scatter(x_data, y_data, alpha=0.6, s=50, color='blue', edgecolors='black')
            
            # Add trend line
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            ax.plot(x_data, p(x_data), "r--", alpha=0.8, linewidth=2, label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
            
            ax.set_xlabel('X', fontsize=12)
            ax.set_ylabel('Y', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            output_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✅ Generated scatter plot: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating scatter plot: {e}")
            raise
    
    def generate_all_basic_diagrams(self) -> Dict[str, str]:
        """Generate all basic mathematical diagrams"""
        diagrams = {}
        
        logger.info("🎨 Generating mathematical diagrams...")
        
        try:
            diagrams['trigonometric'] = self.generate_trigonometric_functions()
        except Exception as e:
            logger.warning(f"⚠️ Trigonometric generation failed: {e}")
        
        try:
            diagrams['quadratic'] = self.generate_quadratic_function(1, 0, 0)
        except Exception as e:
            logger.warning(f"⚠️ Quadratic generation failed: {e}")
        
        try:
            diagrams['circle_theorem'] = self.generate_circle_theorem()
        except Exception as e:
            logger.warning(f"⚠️ Circle theorem generation failed: {e}")
        
        try:
            diagrams['histogram'] = self.generate_histogram()
        except Exception as e:
            logger.warning(f"⚠️ Histogram generation failed: {e}")
        
        try:
            diagrams['box_plot'] = self.generate_box_plot()
        except Exception as e:
            logger.warning(f"⚠️ Box plot generation failed: {e}")
        
        try:
            diagrams['scatter_plot'] = self.generate_scatter_plot()
        except Exception as e:
            logger.warning(f"⚠️ Scatter plot generation failed: {e}")
        
        logger.info(f"✅ Generated {len(diagrams)} mathematical diagrams")
        return diagrams


if __name__ == "__main__":
    # Test basic generation
    logging.basicConfig(level=logging.INFO)
    generator = MathDiagramGenerator()
    diagrams = generator.generate_all_basic_diagrams()
    
    print("\n" + "="*50)
    print("📊 Math Diagrams Generated:")
    print("="*50)
    for name, path in diagrams.items():
        print(f"✅ {name}: {path}")
