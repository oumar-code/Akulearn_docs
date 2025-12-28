#!/usr/bin/env python3
"""
Quick server startup script for Wave 3 Advanced Platform
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("Wave 3 Advanced Platform - Starting Server")
print("=" * 70)

# Import and check features
try:
    from wave3_advanced_platform import (
        app, 
        WEBSOCKET_AVAILABLE, 
        GRAPHQL_AVAILABLE, 
        RECOMMENDATIONS_AVAILABLE, 
        GAMIFICATION_AVAILABLE, 
        ANALYTICS_AVAILABLE
    )
    
    print("\n✓ Successfully imported wave3_advanced_platform")
    print("\nFeature Status:")
    print(f"  {'✓' if WEBSOCKET_AVAILABLE else '✗'} WebSocket Real-Time Updates")
    print(f"  {'✓' if GRAPHQL_AVAILABLE else '✗'} GraphQL API")
    print(f"  {'✓' if RECOMMENDATIONS_AVAILABLE else '✗'} AI Recommendations")
    print(f"  {'✓' if GAMIFICATION_AVAILABLE else '✗'} Gamification System")
    print(f"  {'✓' if ANALYTICS_AVAILABLE else '✗'} Advanced Analytics")
    
    enabled_features = sum([
        WEBSOCKET_AVAILABLE,
        GRAPHQL_AVAILABLE,
        RECOMMENDATIONS_AVAILABLE,
        GAMIFICATION_AVAILABLE,
        ANALYTICS_AVAILABLE
    ])
    
    print(f"\n{enabled_features}/5 features enabled")
    
    if enabled_features == 5:
        print("\n🎉 All features loaded successfully!")
    elif enabled_features > 0:
        print("\n⚠️ Some features are disabled (check dependencies)")
    else:
        print("\n❌ No features loaded (check installation)")
        sys.exit(1)
    
    print("\nServer Endpoints:")
    print("  • Health Check: http://localhost:8000/api/v3/health")
    print("  • API Documentation: http://localhost:8000/docs")
    if GRAPHQL_AVAILABLE:
        print("  • GraphQL Playground: http://localhost:8000/graphql")
    if WEBSOCKET_AVAILABLE:
        print("  • WebSocket: ws://localhost:8000/ws/{student_id}")
    
    print("\nStarting server on http://0.0.0.0:8000...")
    print("=" * 70)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Start server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nMake sure you have installed all dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
