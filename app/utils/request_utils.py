from fastapi.responses import JSONResponse

def response(status_code, message, data=None):
    return JSONResponse(status_code=status_code, content={"message": message, "data": data})