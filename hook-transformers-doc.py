"""
PyInstaller runtime hook to fix inspect.getsource issues
This patches various modules that try to call inspect.getsource
which fails when source code is not available (compiled to bytecode)
"""

import sys
import inspect

# Patch PyTorch's docstring mechanism for macOS ARM64 compatibility
# This works around "RuntimeError: function already has a docstring" errors
def patch_torch_docstrings():
    """
    Monkey-patch torch._C to suppress docstring errors.
    This must be done before torch is imported.
    """
    import sys

    # Store the original __import__
    _original_import = builtins.__import__

    def patched_import(name, *args, **kwargs):
        """Intercept torch._C import and patch it"""
        module = _original_import(name, *args, **kwargs)

        # If we're importing torch._C, patch its add_docstr function
        if name == 'torch._C' or (name == 'torch' and hasattr(module, '_C')):
            try:
                torch_c = module._C if hasattr(module, '_C') else module

                # Patch add_docstr to silently ignore docstring conflicts
                if hasattr(torch_c, 'add_docstr'):
                    original_add_docstr = torch_c.add_docstr

                    def silent_add_docstr(obj, docstr):
                        """Wrapper that catches docstring conflicts"""
                        try:
                            return original_add_docstr(obj, docstr)
                        except RuntimeError as e:
                            if 'already has a docstring' in str(e):
                                # Silently ignore - docstring is already set
                                print(f"[Runtime Hook] Suppressed duplicate docstring for {obj}")
                                return
                            raise

                    torch_c.add_docstr = silent_add_docstr
                    print("[Runtime Hook] Successfully patched torch._C.add_docstr")
            except Exception as e:
                print(f"[Runtime Hook] Warning: Could not patch torch._C: {e}")

        return module

    # Replace the built-in import
    builtins.__import__ = patched_import

import builtins
patch_torch_docstrings()

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

# Patch transformers specific issues
def patch_transformers_doc():
    try:
        import transformers.utils.doc as doc_module

        def patched_get_docstring_indentation_level(func):
            """Return default indentation without inspecting source"""
            return 0

        doc_module.get_docstring_indentation_level = patched_get_docstring_indentation_level
        print("[Runtime Hook] Successfully patched transformers.utils.doc")
    except Exception as e:
        print(f"[Runtime Hook] Warning: Could not patch transformers.utils.doc: {e}")

# Patch torch.utils._config_module to not use inspect
def patch_torch_config():
    try:
        import torch.utils._config_module as config_module

        def patched_get_assignments_with_compile_ignored_comments(filepath):
            """Return empty dict for frozen code"""
            return {}

        config_module.get_assignments_with_compile_ignored_comments = patched_get_assignments_with_compile_ignored_comments
        print("[Runtime Hook] Successfully patched torch.utils._config_module")
    except Exception as e:
        print(f"[Runtime Hook] Warning: Could not patch torch.utils._config_module: {e}")

# Apply patches
patch_transformers_doc()
patch_torch_config()
