from datetime import datetime

def format_datetime(dt_str):
    """Format datetime string to a more readable format"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return dt_str

def format_response(response):
    """Format the response for better readability"""
    if isinstance(response, dict):
        formatted = []
        for key, value in response.items():
            if isinstance(value, (list, dict)):
                formatted.append(f"{key}:\n{format_response(value)}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    elif isinstance(response, list):
        return "\n".join([f"- {item}" for item in response])
    else:
        return str(response) 