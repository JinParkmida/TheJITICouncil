try:
    import ollama
    print("✅ Successfully imported ollama")
    print(f"Ollama version: {ollama.__version__ if hasattr(ollama, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"❌ ImportError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
