# src/models/__init__.py
# Safe imports that handle missing dependencies

try:
    from .api_client import ModelClient
    print("✓ ModelClient available")
except Exception as e:
    print(f"⚠ ModelClient not available: {e}")
    ModelClient = None

try:
    from .hf_loader import HFModelLoader
    print("✓ HFModelLoader available")
except Exception as e:
    print(f"⚠ HFModelLoader not available: {e}")
    HFModelLoader = None

__all__ = ['ModelClient', 'HFModelLoader']