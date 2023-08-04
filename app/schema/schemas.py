def permission_serial(permission):
    return {
        "id": permission["_id"],
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

def staff_serializer(staff):
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

def staff_update_serializer(staff):
    return {
        "id": staff["_id"],
        "address": staff["address"],
        "phone": staff["phone"],
        "email": staff["email"],
        "branch": staff["branch"],
        "username": staff["username"],
        "avartar": staff["avartar"],
        "roles": [role_serial(role) for role in staff["roles"]],
    }

def branch_serializer(branch):
    return {
        "id": str(branch["_id"]),
        "name": branch["name"],
        "address": branch["address"],
        "phone": branch["phone"],
        "email": branch["email"],
        "website": branch["website"],
        "logo": branch["logo"],
        "gstin": branch["gstin"],
        "cin": branch["cin"],
        "pan": branch["pan"],
        "tan": branch["tan"],
        "company": str(branch["company"]),
    }

def company_serializer(company):
    return {
        "id": str(company["_id"]),
        "name": company["name"],
        "address": company["address"],
        "phone": company["phone"],
        "email": company["email"],
        "branches": company["branches"],
        "superusers": company["superusers"],
        "website": company["website"],
        "logo": company["logo"],
        "gstin": company["gstin"],
        "cin": company["cin"],
        "pan": company["pan"],
        "tan": company["tan"],
    }

def branch_update_serializer(branch):
    return {
        "id": str(branch["_id"]),
        "name": branch["name"],
        "address": branch["address"],
        "phone": branch["phone"],
        "email": branch["email"],
        "website": branch["website"],
        "logo": branch["logo"],
        "gstin": branch["gstin"],
        "cin": branch["cin"],
        "pan": branch["pan"],
        "tan": branch["tan"],
        "company": branch["company"],
    }