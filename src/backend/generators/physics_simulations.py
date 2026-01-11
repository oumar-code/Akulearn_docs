"""
Physics Simulations Generator
Generates physics simulations and interactive visualizations
- Simple harmonic motion (pendulum, spring)
- Projectile motion
- Circular motion
- Wave propagation
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)


class PhysicsSimulationGenerator:
    """Generate physics simulations and animations"""
    
    def __init__(self, output_dir="generated_assets/simulations"):
        """
        Initialize physics simulation generator
        
        Args:
            output_dir: Directory to save generated simulations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"PhysicsSimulationGenerator initialized: {self.output_dir}")
    
    def generate_pendulum_simulation(self, name: str = "simple_pendulum") -> str:
        """
        Generate interactive simple pendulum simulation
        
        Args:
            name: Name for the simulation
            
        Returns:
            Path to generated HTML file
        """
        try:
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Simple Pendulum - Simple Harmonic Motion</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        #canvas-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .controls {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        label {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        input[type="range"] {
            width: 150px;
        }
        button {
            padding: 8px 16px;
            margin: 0 5px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #0056b3;
        }
        h2 {
            color: #333;
            margin-top: 0;
        }
        .data {
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h2>Simple Pendulum - Simple Harmonic Motion</h2>
    <div id="canvas-container"></div>
    
    <div class="controls">
        <div>
            <label>Length (px): <input type="range" id="length" min="100" max="300" value="200" /></label>
            <span id="lengthValue">200</span>
        </div>
        <div>
            <label>Initial Angle (°): <input type="range" id="angle" min="10" max="90" value="45" /></label>
            <span id="angleValue">45</span>
        </div>
        <div>
            <label>Damping: <input type="range" id="damping" min="0.99" max="1.0" step="0.001" value="0.995" /></label>
            <span id="dampingValue">0.995</span>
        </div>
        <div>
            <button onclick="reset()">Reset</button>
            <button onclick="togglePause()">Pause/Resume</button>
        </div>
    </div>
    
    <div class="info">
        <div class="data">Angle: <span id="currentAngle">0.0</span>°</div>
        <div class="data">Period: <span id="period">0.0</span> cycles</div>
        <div class="data">Energy: <span id="energy">0.0</span> (normalized)</div>
    </div>
    
    <script>
        let angle = PI / 4;
        let angleV = 0;
        let angleA = 0;
        let length = 200;
        const gravity = 0.5;
        let damping = 0.995;
        let paused = false;
        let cycleCount = 0;
        let lastAngle = PI / 4;
        
        function setup() {
            createCanvas(800, 600).parent('canvas-container');
        }
        
        function draw() {
            background(240);
            
            // Update parameters from sliders
            length = parseInt(document.getElementById('length').value);
            damping = parseFloat(document.getElementById('damping').value);
            
            translate(width / 2, 50);
            
            if (!paused) {
                // Physics
                angleA = (-gravity / length) * sin(angle);
                angleV += angleA;
                angleV *= damping;
                angle += angleV;
                
                // Count cycles
                if (lastAngle > 0 && angle <= 0) {
                    cycleCount += 0.5;
                } else if (lastAngle < 0 && angle >= 0) {
                    cycleCount += 0.5;
                }
                lastAngle = angle;
            }
            
            // Draw rod
            let bobX = length * sin(angle);
            let bobY = length * cos(angle);
            stroke(0);
            strokeWeight(2);
            line(0, 0, bobX, bobY);
            
            // Draw bob
            fill(200, 50, 50);
            ellipse(bobX, bobY, 40, 40);
            
            // Draw pivot
            fill(100);
            ellipse(0, 0, 10, 10);
            
            // Draw path arc
            strokeWeight(0.5);
            stroke(150, 150, 200, 100);
            arc(0, 0, 2*length, 2*length, -PI/4, PI/4, OPEN);
            
            // Calculate energy
            let pe = length * (1 - cos(angle));
            let ke = 0.5 * angleV * angleV;
            let energy = (ke + pe) / (length * 2); // normalize
            
            // Display info
            fill(0);
            noStroke();
            textSize(12);
            textAlign(LEFT);
            document.getElementById('currentAngle').textContent = (angle * 180 / PI).toFixed(1);
            document.getElementById('period').textContent = cycleCount.toFixed(1);
            document.getElementById('energy').textContent = energy.toFixed(3);
            document.getElementById('lengthValue').textContent = length;
            document.getElementById('angleValue').textContent = 
                parseInt(document.getElementById('angle').value);
            document.getElementById('dampingValue').textContent = damping.toFixed(3);
        }
        
        function reset() {
            angle = radians(parseInt(document.getElementById('angle').value));
            angleV = 0;
            cycleCount = 0;
            lastAngle = angle;
        }
        
        function togglePause() {
            paused = !paused;
        }
    </script>
</body>
</html>
            '''
            
            output_path = self.output_dir / f"{name}.html"
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            logger.info(f"✅ Generated pendulum simulation: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating pendulum simulation: {e}")
            raise
    
    def generate_projectile_motion_simulation(self, name: str = "projectile_motion") -> str:
        """Generate interactive projectile motion simulation"""
        try:
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Projectile Motion Simulator</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        #canvas-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
        .controls {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        label {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        input[type="range"] {
            width: 150px;
        }
        button {
            padding: 8px 16px;
            margin: 0 5px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #0056b3;
        }
        h2 {
            color: #333;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h2>Projectile Motion Simulator</h2>
    <div id="canvas-container"></div>
    
    <div class="controls">
        <div>
            <label>Initial Velocity: <input type="range" id="velocity" min="10" max="50" value="30" /></label>
            <span id="velocityValue">30</span> m/s
        </div>
        <div>
            <label>Launch Angle: <input type="range" id="launchAngle" min="0" max="90" value="45" /></label>
            <span id="angleValue">45</span>°
        </div>
        <div>
            <button onclick="launchProjectile()">Launch</button>
            <button onclick="clearTrajectory()">Clear</button>
        </div>
    </div>
    
    <script>
        let projectiles = [];
        let gravity = 0.2;
        let scale = 5; // pixels per meter
        
        class Projectile {
            constructor(v, angle) {
                this.x = 50;
                this.y = height - 50;
                this.vx = (v * cos(radians(angle))) / scale;
                this.vy = -(v * sin(radians(angle))) / scale;
                this.trail = [];
            }
            
            update() {
                this.vy += gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.trail.push({x: this.x, y: this.y});
            }
            
            display() {
                // Draw trail
                stroke(150, 150, 200, 100);
                strokeWeight(1);
                noFill();
                beginShape();
                for (let point of this.trail) {
                    vertex(point.x, point.y);
                }
                endShape();
                
                // Draw projectile
                fill(255, 100, 100);
                stroke(200, 0, 0);
                circle(this.x, this.y, 8);
            }
            
            isAlive() {
                return this.y < height - 50;
            }
        }
        
        function setup() {
            createCanvas(800, 500).parent('canvas-container');
        }
        
        function draw() {
            background(135, 206, 235); // Sky blue
            
            // Draw ground
            fill(34, 139, 34);
            rect(0, height - 50, width, 50);
            
            // Draw grid
            stroke(200);
            strokeWeight(0.5);
            for (let i = 0; i < width; i += 50) {
                line(i, height - 50 - 200, i, height - 50);
            }
            
            // Update and display projectiles
            for (let i = projectiles.length - 1; i >= 0; i--) {
                projectiles[i].update();
                projectiles[i].display();
                if (!projectiles[i].isAlive()) {
                    projectiles.splice(i, 1);
                }
            }
            
            // Display info
            fill(0);
            textSize(12);
            textAlign(LEFT);
            text(`Active Projectiles: ${projectiles.length}`, 10, 20);
        }
        
        function launchProjectile() {
            let v = parseInt(document.getElementById('velocity').value);
            let angle = parseInt(document.getElementById('launchAngle').value);
            projectiles.push(new Projectile(v, angle));
        }
        
        function clearTrajectory() {
            projectiles = [];
        }
        
        // Update display values
        document.getElementById('velocity').addEventListener('input', function(e) {
            document.getElementById('velocityValue').textContent = e.target.value;
        });
        
        document.getElementById('launchAngle').addEventListener('input', function(e) {
            document.getElementById('angleValue').textContent = e.target.value;
        });
    </script>
</body>
</html>
            '''
            
            output_path = self.output_dir / f"{name}.html"
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            logger.info(f"✅ Generated projectile motion simulation: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating projectile motion simulation: {e}")
            raise
    
    def generate_wave_simulation(self, name: str = "wave_propagation") -> str:
        """Generate wave propagation simulation"""
        try:
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Wave Propagation Simulator</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        #canvas-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
        .controls {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        label {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        input[type="range"] {
            width: 150px;
        }
        h2 {
            color: #333;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h2>Wave Propagation Simulator</h2>
    <div id="canvas-container"></div>
    
    <div class="controls">
        <div>
            <label>Amplitude: <input type="range" id="amplitude" min="5" max="40" value="20" /></label>
            <span id="ampValue">20</span>
        </div>
        <div>
            <label>Frequency: <input type="range" id="frequency" min="0.02" max="0.1" step="0.01" value="0.05" /></label>
            <span id="freqValue">0.05</span>
        </div>
        <div>
            <label>Speed: <input type="range" id="speed" min="0.5" max="3" step="0.5" value="1.5" /></label>
            <span id="speedValue">1.5</span>
        </div>
    </div>
    
    <script>
        let time = 0;
        
        function setup() {
            createCanvas(800, 400).parent('canvas-container');
        }
        
        function draw() {
            background(240);
            
            let amplitude = parseInt(document.getElementById('amplitude').value);
            let frequency = parseFloat(document.getElementById('frequency').value);
            let speed = parseFloat(document.getElementById('speed').value);
            
            time += speed * frequency;
            
            stroke(0, 100, 200);
            strokeWeight(3);
            noFill();
            
            beginShape();
            for (let x = 0; x < width; x += 5) {
                let y = height / 2 + amplitude * sin(frequency * x * 0.02 - time);
                vertex(x, y);
            }
            endShape();
            
            // Draw axis
            stroke(150);
            strokeWeight(1);
            line(0, height/2, width, height/2);
            
            // Display info
            fill(0);
            textSize(12);
            document.getElementById('ampValue').textContent = amplitude;
            document.getElementById('freqValue').textContent = frequency.toFixed(2);
            document.getElementById('speedValue').textContent = speed.toFixed(1);
        }
    </script>
</body>
</html>
            '''
            
            output_path = self.output_dir / f"{name}.html"
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            logger.info(f"✅ Generated wave simulation: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Error generating wave simulation: {e}")
            raise
    
    def generate_all_simulations(self) -> Dict[str, str]:
        """Generate all physics simulations"""
        simulations = {}
        
        logger.info("🔬 Generating physics simulations...")
        
        try:
            simulations['pendulum'] = self.generate_pendulum_simulation()
        except Exception as e:
            logger.warning(f"⚠️ Pendulum simulation failed: {e}")
        
        try:
            simulations['projectile_motion'] = self.generate_projectile_motion_simulation()
        except Exception as e:
            logger.warning(f"⚠️ Projectile motion simulation failed: {e}")
        
        try:
            simulations['wave_propagation'] = self.generate_wave_simulation()
        except Exception as e:
            logger.warning(f"⚠️ Wave simulation failed: {e}")
        
        logger.info(f"✅ Generated {len(simulations)} physics simulations")
        return simulations


if __name__ == "__main__":
    # Test basic generation
    logging.basicConfig(level=logging.INFO)
    generator = PhysicsSimulationGenerator()
    simulations = generator.generate_all_simulations()
    
    print("\n" + "="*50)
    print("🔬 Physics Simulations Generated:")
    print("="*50)
    for name, path in simulations.items():
        print(f"✅ {name}: {path}")
