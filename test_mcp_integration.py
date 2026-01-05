#!/usr/bin/env python3
"""
Test Brave Search API Integration
Verifies MCP Brave Search connectivity and functionality
"""

import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_brave_search_api():
    """Test Brave Search API connection"""
    
    logger.info("\n" + "="*60)
    logger.info("🔍 BRAVE SEARCH API TEST")
    logger.info("="*60 + "\n")
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key exists
    api_key = os.getenv('BRAVE_SEARCH_API_KEY')
    
    if not api_key:
        logger.error("❌ BRAVE_SEARCH_API_KEY not found in .env file")
        logger.info("\n📝 To fix:")
        logger.info("   1. Open .env file")
        logger.info("   2. Add: BRAVE_SEARCH_API_KEY=your_actual_key_here")
        logger.info("   3. Save and run this test again\n")
        return False
    
    if api_key == "YOUR_API_KEY_HERE":
        logger.error("❌ Please replace YOUR_API_KEY_HERE with your actual API key")
        logger.info("\n📝 To fix:")
        logger.info("   1. Open .env file")
        logger.info("   2. Replace YOUR_API_KEY_HERE with your actual Brave Search API key")
        logger.info("   3. Save and run this test again\n")
        return False
    
    logger.info(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test API call
    try:
        import requests
        
        logger.info("\n🔄 Testing API connection...")
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key
        }
        
        # Test search query
        test_query = "WAEC Mathematics syllabus Nigeria"
        params = {
            "q": test_query,
            "count": 3
        }
        
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            logger.info(f"✅ API connection successful!")
            logger.info(f"\n📊 Test Query: '{test_query}'")
            
            if 'web' in results and 'results' in results['web']:
                logger.info(f"   Found {len(results['web']['results'])} results:")
                for i, result in enumerate(results['web']['results'][:3], 1):
                    logger.info(f"\n   {i}. {result.get('title', 'N/A')}")
                    logger.info(f"      URL: {result.get('url', 'N/A')}")
                    logger.info(f"      Description: {result.get('description', 'N/A')[:100]}...")
            
            logger.info("\n✅ Brave Search API is working correctly!")
            logger.info("   You can now use MCP-enhanced content generation")
            return True
        
        else:
            logger.error(f"❌ API error: Status {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
    
    except ImportError:
        logger.error("❌ 'requests' library not installed")
        logger.info("\n📝 To fix:")
        logger.info("   pip install requests")
        return False
    
    except Exception as e:
        logger.error(f"❌ Error testing API: {e}")
        return False


def test_mcp_content_generation():
    """Test MCP-enhanced content generation"""
    
    logger.info("\n" + "="*60)
    logger.info("🎓 MCP CONTENT GENERATION TEST")
    logger.info("="*60 + "\n")
    
    try:
        from enhanced_content_generator import EnhancedContentGenerator
        
        # Create generator with MCP enabled
        logger.info("🔄 Initializing MCP-enabled content generator...")
        generator = EnhancedContentGenerator(use_mcp=True)
        
        logger.info("✅ Generator initialized with MCP support")
        logger.info("\n📊 WAEC Topics Available:")
        for subject, topics in generator.WAEC_TOPICS.items():
            logger.info(f"   • {subject}: {len(topics)} topics")
        
        logger.info("\n✅ MCP content generation is ready!")
        logger.info("   Run: python curriculum_expander.py")
        logger.info("   Or: python run_batch4_generation.py")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Error initializing generator: {e}")
        return False


def main():
    """Run all tests"""
    
    logger.info("\n🚀 STARTING MCP INTEGRATION TESTS\n")
    
    # Test 1: API Key
    api_test = test_brave_search_api()
    
    if not api_test:
        logger.info("\n⚠️  Fix API key issues before proceeding\n")
        return
    
    # Test 2: Content Generation
    content_test = test_mcp_content_generation()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"   Brave Search API: {'✅ PASS' if api_test else '❌ FAIL'}")
    logger.info(f"   MCP Generation:   {'✅ PASS' if content_test else '❌ FAIL'}")
    
    if api_test and content_test:
        logger.info("\n🎉 ALL TESTS PASSED!")
        logger.info("\n🚀 Next Steps:")
        logger.info("   1. Generate research-backed content:")
        logger.info("      python curriculum_expander.py")
        logger.info("\n   2. Or run complete Batch 4 workflow:")
        logger.info("      python run_batch4_generation.py")
        logger.info("\n   3. Content will include:")
        logger.info("      • Real-time WAEC syllabus research")
        logger.info("      • Nigerian educational context")
        logger.info("      • Current exam patterns and trends")
        logger.info("      • Up-to-date examples and applications\n")
    else:
        logger.info("\n⚠️  Please fix the issues above and run test again\n")


if __name__ == "__main__":
    main()
