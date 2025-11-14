"""
PyInstaller runtime hook to fix inspect.getsource issues
This patches various modules that try to call inspect.getsource
which fails when source code is not available (compiled to bytecode)
"""

import sys
import inspect

# CRITICAL: Intercept torch._C import to patch add_docstr
# This fixes "RuntimeError: function 'conv1d' already has a docstring" on macOS ARM64
class TorchCImportHook:
    """Import hook to patch torch._C.add_docstr during module load"""

    def find_module(self, fullname, path=None):
        if fullname == 'torch._C':
            return self
        return None

    def load_module(self, fullname):
        # Check if already loaded
        if fullname in sys.modules:
            return sys.modules[fullname]

        # Import using standard mechanism, but catch docstring errors
        import importlib
        try:
            module = importlib.import_module(fullname)
        except RuntimeError as e:
            if 'already has a docstring' in str(e):
                # Error occurred during import - try to get partially loaded module
                module = sys.modules.get(fullname)
                if module is None:
                    print(f"[Runtime Hook] ✗ torch._C import failed completely: {e}")
                    raise
                print(f"[Runtime Hook] ⚠ torch._C partially loaded despite error: {e}")
            else:
                raise

        # Now patch add_docstr function
        if hasattr(module, 'add_docstr'):
            _original_add_docstr = module.add_docstr

            def _silent_add_docstr(obj, docstr):
                """Wrapper that silently ignores duplicate docstring errors"""
                try:
                    return _original_add_docstr(obj, docstr)
                except RuntimeError as e:
                    if 'already has a docstring' in str(e):
                        # Silently ignore - docstring already exists
                        return None
                    raise

            module.add_docstr = _silent_add_docstr
            print("[Runtime Hook] ✓ Patched torch._C.add_docstr")
        else:
            print("[Runtime Hook] ⚠ torch._C has no add_docstr attribute")

        return module

# Install torch._C import hook FIRST (highest priority)
sys.meta_path.insert(0, TorchCImportHook())
print("[Runtime Hook] ✓ Installed torch._C import hook")

# Monkey-patch inspect.getsource and related functions to handle frozen modules
_original_getsource = inspect.getsource
_original_getsourcelines = inspect.getsourcelines
_original_findsource = inspect.findsource

def patched_getsource(object):
    """Patched getsource that returns empty string for frozen modules"""
    try:
        return _original_getsource(object)
    except (OSError, TypeError):
        # Return empty string for frozen/compiled code
        return ""

def patched_getsourcelines(object):
    """Patched getsourcelines that returns empty list for frozen modules"""
    try:
        return _original_getsourcelines(object)
    except (OSError, TypeError):
        # Return empty list for frozen/compiled code
        return ([], 0)

def patched_findsource(object):
    """Patched findsource that returns empty for frozen modules"""
    try:
        return _original_findsource(object)
    except (OSError, TypeError):
        # Return empty tuple for frozen/compiled code
        return ([], 0)

# Apply global inspect patches
inspect.getsource = patched_getsource
inspect.getsourcelines = patched_getsourcelines
inspect.findsource = patched_findsource

print("[Runtime Hook] Successfully patched inspect.getsource, getsourcelines, findsource")

# Use import hook to patch modules lazily when they're imported
# This avoids triggering torch import in the runtime hook itself
class LazyModulePatcher:
    """Import hook to patch modules after they're loaded"""

    def find_module(self, fullname, path=None):
        # Intercept these specific modules
        if fullname in ('transformers.utils.doc', 'torch.utils._config_module'):
            return self
        return None

    def load_module(self, fullname):
        # Let Python load the module normally first
        if fullname in sys.modules:
            return sys.modules[fullname]

        # Use standard import mechanism
        import importlib
        module = importlib.import_module(fullname)

        # Now patch the loaded module
        try:
            if fullname == 'transformers.utils.doc':
                def patched_get_docstring_indentation_level(func):
                    return 0
                module.get_docstring_indentation_level = patched_get_docstring_indentation_level
                print("[Runtime Hook] ✓ Patched transformers.utils.doc")

            elif fullname == 'torch.utils._config_module':
                def patched_get_assignments_with_compile_ignored_comments(filepath):
                    return {}
                module.get_assignments_with_compile_ignored_comments = patched_get_assignments_with_compile_ignored_comments
                print("[Runtime Hook] ✓ Patched torch.utils._config_module")
        except Exception as e:
            print(f"[Runtime Hook] ✗ Failed to patch {fullname}: {e}")

        return module

# Install the import hook
sys.meta_path.insert(0, LazyModulePatcher())
print("[Runtime Hook] ✓ Installed lazy module patcher")
