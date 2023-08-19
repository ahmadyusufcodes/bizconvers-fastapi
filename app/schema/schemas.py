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
        "username": staff["username"],
        "avartar": staff["avartar"],
        "roles": [role_serial(role) for role in staff["roles"]],
        "branch": [str(branch) for branch in staff["branch"]],
        "company": staff["company"],
    }

def staff_update_serializer(staff):
    return {
        "id": staff["_id"],
        "address": staff["address"],
        "phone": staff["phone"],
        "email": staff["email"],
        "branch": [str(branch) for branch in staff["branch"]],
        "company": staff["company"],
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
        "attributes": branch["attributes"],
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
        "attributes": company["attributes"],
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
        "attributes": branch["attributes"],
        "company": branch["company"],
    }

def product_serializer(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "image": product["image"],
        "unit": product["unit"],
        "category_id": str(product["category_id"]),
        "attributes": product["attributes"],
    }

def product_update_serializer(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "image": [image for image in product["image"]],
        "unit": product["unit"],
        "category_id": str(product["category_id"]),
        "attributes": product["attributes"],
    }

def product_variant_serializer(product_variant):
    return {
        "id": str(product_variant["_id"]),
        "product_id": str(product_variant["product_id"]),
        "name": product_variant["name"],
        "description": product_variant["description"],
        "images": [image for image in product_variant["image"]],
        "unit": product_variant["unit"],
        "attributes": product_variant["attributes"],
    }

def product_variant_update_serializer(product_variant):
    return {
        "id": str(product_variant["_id"]),
        "product_id": str(product_variant["product_id"]),
        "name": product_variant["name"],
        "description": product_variant["description"],
        "images": [image for image in product_variant["image"]],
        "unit": product_variant["unit"],
        "attributes": product_variant["attributes"],
    }

def product_in_branch_serializer(product_in_branch):
    return {
        "id": str(product_in_branch["_id"]),
        "product_id": str(product_in_branch["product_id"]),
        "branch_id": str(product_in_branch["branch_id"]),
        "price": product_in_branch["price"],
        "quantity": product_in_branch["quantity"],
        "attributes": product_in_branch["attributes"],
        "in_stock": product_in_branch["in_stock"],
    }

def product_in_branch_update_serializer(product_in_branch):
    return {
        "id": str(product_in_branch["_id"]),
        "product_id": str(product_in_branch["product_id"]),
        "branch_id": str(product_in_branch["branch_id"]),
        "price": product_in_branch["price"],
        "quantity": product_in_branch["quantity"],
        "attributes": product_in_branch["attributes"],
        "in_stock": product_in_branch["in_stock"],
    }

def product_variant_in_branch_serializer(product_variant_in_branch):
    return {
        "id": str(product_variant_in_branch["_id"]),
        "product_id": str(product_variant_in_branch["product_id"]),
        "variant_id": str(product_variant_in_branch["variant_id"]),
        "branch_id": str(product_variant_in_branch["branch_id"]),
        "price": product_variant_in_branch["price"],
        "quantity": product_variant_in_branch["quantity"],
        "attributes": product_variant_in_branch["attributes"],
        "in_stock": product_variant_in_branch["in_stock"],
    }

def product_variant_in_branch_update_serializer(product_variant_in_branch):
    return {
        "id": str(product_variant_in_branch["_id"]),
        "product_id": str(product_variant_in_branch["product_id"]),
        "variant_id": str(product_variant_in_branch["variant_id"]),
        "branch_id": str(product_variant_in_branch["branch_id"]),
        "price": product_variant_in_branch["price"],
        "quantity": product_variant_in_branch["quantity"],
        "attributes": product_variant_in_branch["attributes"],
        "in_stock": product_variant_in_branch["in_stock"],
    }

def category_serializer(category):
    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category["description"],
        "company_id": str(category["company_id"]),
        "attributes": category["attributes"],
    }

def category_update_serializer(category):
    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category["description"],
        "company_id": str(category["company_id"]),
        "attributes": category["attributes"],
    }

def order_item_serializer(order_item):
    return {
        "id": str(order_item["_id"]),
        "product_id": str(order_item["product_id"]),
        "variant_id": str(order_item["variant_id"]),
        "quantity": order_item["quantity"],
        "attributes": order_item["attributes"],
    }

def order_item_update_serializer(order_item):
    return {
        "id": str(order_item["_id"]),
        "product_id": str(order_item["product_id"]),
        "variant_id": str(order_item["variant_id"]),
        "quantity": order_item["quantity"],
        "attributes": order_item["attributes"],
    }

def order_serializer(order):
    return {
        "id": str(order["_id"]),
        "order_number": order["order_number"],
        "customer_id": str(order["customer_id"]),
        "branch_id": str(order["branch_id"]),
        "items": [order_item_serializer(item) for item in order["items"]],
        "total": order["total"],
        "payment_method": order["payment_method"],
        "payment_status": order["payment_status"],
        "delivery_method": order["delivery_method"],
        "delivery_status": order["delivery_status"],
        "attributes": order["attributes"],
    }

def order_update_serializer(order):
    return {
        "id": str(order["_id"]),
        "order_number": order["order_number"],
        "customer_id": str(order["customer_id"]),
        "branch_id": str(order["branch_id"]),
        "items": [order_item_serializer(item) for item in order["items"]],
        "total": order["total"],
        "payment_method": order["payment_method"],
        "payment_status": order["payment_status"],
        "delivery_method": order["delivery_method"],
        "delivery_status": order["delivery_status"],
        "attributes": order["attributes"],
    }

def order_payment_serializer(order_payment):
    return {
        "id": str(order_payment["_id"]),
        "order_id": str(order_payment["order_id"]),
        "amount": order_payment["amount"],
        "payment_method": order_payment["payment_method"],
        "payment_status": order_payment["payment_status"],
        "attributes": order_payment["attributes"],
    }

def order_payment_update_serializer(order_payment):
    return {
        "id": str(order_payment["_id"]),
        "order_id": str(order_payment["order_id"]),
        "amount": order_payment["amount"],
        "payment_method": order_payment["payment_method"],
        "payment_status": order_payment["payment_status"],
        "attributes": order_payment["attributes"],
    }

def order_delivery_serializer(order_delivery):
    return {
        "id": str(order_delivery["_id"]),
        "order_id": str(order_delivery["order_id"]),
        "amount": order_delivery["amount"],
        "delivery_method": order_delivery["delivery_method"],
        "delivery_status": order_delivery["delivery_status"],
        "attributes": order_delivery["attributes"],
    }

def order_delivery_update_serializer(order_delivery):
    return {
        "id": str(order_delivery["_id"]),
        "order_id": str(order_delivery["order_id"]),
        "amount": order_delivery["amount"],
        "delivery_method": order_delivery["delivery_method"],
        "delivery_status": order_delivery["delivery_status"],
        "attributes": order_delivery["attributes"],
    }

def order_status_update_serializer(order_status_update):
    return {
        "id": str(order_status_update["_id"]),
        "order_id": str(order_status_update["order_id"]),
        "status": order_status_update["status"],
        "attributes": order_status_update["attributes"],
    }

def order_status_update_update_serializer(order_status_update):
    return {
        "id": str(order_status_update["_id"]),
        "order_id": str(order_status_update["order_id"]),
        "status": order_status_update["status"],
        "attributes": order_status_update["attributes"],
    }

