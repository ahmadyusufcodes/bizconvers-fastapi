def success_response(data, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def error_response(message="Error", status_code=400):
    return {
        "status": "error",
        "message": message
    }, status_code
