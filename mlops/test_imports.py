import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except Exception as e:
    print(f"✗ pandas import failed: {e}")

try:
    import plotly.express as px
    print("✓ plotly imported successfully")
except Exception as e:
    print(f"✗ plotly import failed: {e}")

print("\nTest complete.")
