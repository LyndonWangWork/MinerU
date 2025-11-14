"""
PyInstaller runtime hook to fix transformers inspect.getsource issue
This patches the transformers.utils.doc module to avoid calling inspect.getsource
which fails when source code is not available (compiled to bytecode)
"""

import sys

# Patch before transformers is imported
def patch_transformers_doc():
    try:
        # Patch get_docstring_indentation_level to not use inspect.getsource
        import transformers.utils.doc as doc_module

        def patched_get_docstring_indentation_level(func):
            """Return default indentation without inspecting source"""
            return 0

        # Replace the problematic function
        doc_module.get_docstring_indentation_level = patched_get_docstring_indentation_level

        print("[Runtime Hook] Successfully patched transformers.utils.doc")
    except Exception as e:
        print(f"[Runtime Hook] Warning: Could not patch transformers.utils.doc: {e}")

# Apply patch
patch_transformers_doc()
