import sys

def main():
    try:
        import google.generativeai as gen
        ver = getattr(gen, "__version__", "unknown")
        print(f"google-generativeai import: OK | version={ver}")
        sys.exit(0)
    except Exception as e:
        print(f"google-generativeai import: FAIL | {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
