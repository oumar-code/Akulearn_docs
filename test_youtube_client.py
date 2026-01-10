from youtube_mcp_client import YouTubeMCPClient

client = YouTubeMCPClient()
mode = "stub" if client.use_stub else "API"
print(f"YouTube client mode: {mode}")

results = client.search_videos("Biology photosynthesis SS1", limit=2)
print(f"\nFound {len(results)} videos:")
for v in results:
    print(f"  - {v['title'][:60]}")
    print(f"    Channel: {v['channel']}, Duration: {v['duration']}")
