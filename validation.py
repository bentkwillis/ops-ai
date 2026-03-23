def validate_response(data):
    if not isinstance(data, dict):
        return False
    
    required_fields = ["analysis", "plan", "next_command", "reason", "confidence"]

    for field in required_fields:
        if field not in data:
            return False
        
    if not isinstance(data["analysis"], str):
        return False
    
    if not isinstance(data["plan"], list):
        return False
    
    if len(data["plan"]) !=3:
        return False
    
    if not all(isinstance(step, str) for step in data["plan"]):
        return False
    
    if not isinstance(data["next_command"], str):
        return False
    
    if not isinstance(data["reason"], str):
        return False
    
    if not isinstance(data["confidence"], (int, float)):
        return False
    
    if "done" not in data:
        return False
    
    if not isinstance(data["done"], bool):
        return False
    
    return True