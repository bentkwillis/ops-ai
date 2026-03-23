def validate_response(data):
    if not isinstance(data, dict):
        return False
    
    required_fields = ["analysis", "next_command", "reason", "confidence"]

    for field in required_fields:
        if field not in data:
            return False
    
    if not isinstance(data["next_command"], str):
        return False
    
    if not isinstance(data["confidence"], (int, float)):
        return False
    
    return True