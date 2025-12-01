import ollama
import re

def convene_council(func_name: str, signature: str, docstring: str) -> str:
    """
    Convenes the Council (LLM) to generate the implementation for the given function.
    """
    
    # Construct the prompt for the Council
    prompt = f"""
    You are an expert Python Code Generator.
    Your task is to write the implementation for the following Python function.
    
    Function Name: {func_name}
    Signature: {signature}
    Docstring: {docstring}
    
    CRITICAL INSTRUCTIONS:
    1. Return ONLY the valid Python code for the function.
    2. The code MUST include the function definition (`def {func_name}(...):`).
    3. Do NOT wrap the code in markdown blocks (like ```python ... ```).
    4. Do NOT include any explanations, comments, or text outside the code.
    5. The implementation must match the signature and docstring exactly.
    """

    try:
        # We use a model that is good at coding. 
        # Ideally this is configurable, but for now we default to a capable local model.
        # Users should have 'qwen2.5-coder' or similar pulled in Ollama.
        # Fallback order could be implemented here.
        model = "qwen2.5-coder" 
        
        response = ollama.chat(model=model, messages=[
            {
                'role': 'system',
                'content': 'You are a Python code generator. Output ONLY valid Python code. No markdown.'
            },
            {
                'role': 'user',
                'content': prompt
            },
        ])
        
        content = response['message']['content']
        
        # Post-processing to clean up common LLM artifacts
        # 1. Remove markdown code blocks if present
        content = re.sub(r'^```python\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'```$', '', content, flags=re.MULTILINE)
        
        return content.strip()

    except Exception as e:
        # In a real app, we might want to fallback or error out gracefully
        print(f"❌ The Council failed to reach a consensus: {e}")
        raise e

