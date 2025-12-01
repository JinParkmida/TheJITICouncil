import sys
import os

# Add src to pythonpath so we can import jiti without installing it yet
sys.path.insert(0, os.path.abspath("src"))

try:
    from jiti import jiti_implementation
    print("✅ Successfully imported jiti_implementation")
    
    @jiti_implementation
    def test_func():
        """Test function"""
        pass
        
    print("✅ Successfully applied decorator")
    
except ImportError as e:
    print(f"❌ ImportError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
