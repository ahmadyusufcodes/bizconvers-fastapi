from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from app.schema.schemas import superuser_serializer, staff_serializer, login_serializer
from app.models.company import SuperUser, Staff

# POST /register/superuser: Register a new superuser.
# POST /register/user: Register a new user (staff member).
# POST /login: User login and authentication.
# GET /users/: Get a list of all users.
# GET /users/{user_id}: Get user details by ID.
# PUT /users/{user_id}: Update user details.
# DELETE /users/{user_id}: Delete a user.

router = APIRouter({
    "prefix": "/user",
    "tags": ["User"]
})

superuser = db["superuser"] # collection
staff = db["staff"] # collection

@router.post("/register/superuser", response_description="Add new superuser", response_model=SuperUser)
async def create_superuser(superuser: SuperUser = Depends(superuser_serializer)):
    try:
        superuser_id = await db["superuser"].insert_one(superuser.dict())
        new_superuser = await db["superuser"].find_one({"_id": superuser_id.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_superuser)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/register/user", response_description="Add new user", response_model=Staff)
async def create_staff(staff: Staff = Depends(staff_serializer)):
    try:
        staff_id = await db["staff"].insert_one(staff.dict())
        new_staff = await db["staff"].find_one({"_id": staff_id.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_staff)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/login", response_description="Login and authentication", response_model=Staff)
async def login_staff(staff: Staff = Depends(login_serializer)):
    try:
        staff = await db["staff"].find_one({"email": staff.email, "password": staff.password})
        if staff:
            return staff
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_description="Get all users")
async def read_users(request: Request):
    try:
        total = await db["staff"].count_documents({})
        staff = await db["staff"].find({}).skip((request.query_params["page"] - 1) * 10).limit(10).to_list(length=100)
        return {"total": total, "staff": staff, "next": request.query_params["page"] + 1}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{user_id}", response_description="Get a single user")
async def read_user(user_id: str):
    try:
        user = await db["staff"].find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}", response_description="Update a user")
async def update_user(user_id: str, user: Staff = Depends(staff_serializer)):
    try:
        user = await db["staff"].find_one({"_id": ObjectId(user_id)})
        if user:
            updated_user = await db["staff"].update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
            if updated_user:
                return await db["staff"].find_one({"_id": ObjectId(user_id)})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str):
    try:
        user = await db["staff"].find_one({"_id": ObjectId(user_id)})
        if user:
            await db["staff"].delete_one({"_id": ObjectId(user_id)})
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))