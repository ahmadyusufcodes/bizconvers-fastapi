def permission_serial(permission):
    return {
        "name": permission["name"],
        "read": permission["read"],
        "write": permission["write"],
        "delete": permission["delete"],
        "description": permission["description"]
    }

def role_serial(role):
    return {
        "id": str(role["_id"]),
        "name": role["name"],
        "description": role["description"],
        "slug": role["name"].lower().replace(" ", "_"),
        "permissions": [permission_serial(permission) for permission in role["permissions"]]
    }

def staff_serial(staff):
    return {
        "id": str(staff["_id"]),
        "address": staff["address"],
        "phone": staff["phone"],
        "email": staff["email"],
        "branch": staff["branch"],
        "username": staff["username"],
        "avartar": staff["avartar"],
        "roles": [role_serial(role) for role in staff["roles"]],
    }