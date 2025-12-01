# src/jiti/core.py
import functools
import inspect
from .holocron import Holocron
from .council import convene_council

def jiti_implementation(func):
    """
    The JITI Council Decorator.
    Intercepts the call, checks the Holocron (cache),
    or convenes the Council (LLM) to generate the code.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Identify the function
        sig = inspect.signature(func)
        docstring = inspect.getdoc(func)
        func_name = func.__name__
        sig_str = str(sig)
        
        # 2. Check the Holocron (Cache)
        cached_code = Holocron.retrieve(func_name, sig_str)
        
        func_impl = None
        
        if cached_code:
            # print(f"📜 Retrieved {func_name} from the Holocron.")
            pass
        else:
            # 3. Convene the Council (If not cached)
            print(f"⚡ The Council is deliberating on: {func_name}...")
            try:
                cached_code = convene_council(func_name, sig_str, docstring)
                # 4. Archive the decision
                Holocron.archive(func_name, sig_str, cached_code)
            except Exception as e:
                print(f"❌ The Council could not decide: {e}")
                return None

        # 5. Execute the implementation
        # We execute the code in a local scope to retrieve the function object
        if cached_code:
            local_scope = {}
            # We need to ensure the code is safe-ish. 
            # exec() is dangerous, but that's the point of this project.
            try:
                exec(cached_code, globals(), local_scope)
                func_impl = local_scope.get(func_name)
            except Exception as e:
                print(f"❌ Failed to execute Council's decree: {e}")
                # If execution fails, maybe invalidate cache?
                return None
        
        if func_impl:
            return func_impl(*args, **kwargs)
        else:
            print(f"❌ Could not find function {func_name} in generated code.")
            return None

    return wrapper
