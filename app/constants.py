from fastapi import HTTPException, status


HTTP_401_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')