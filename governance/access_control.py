def require_role(user_role: str, allowed_roles: list):
    if user_role not in allowed_roles:
        raise PermissionError("Access denied for this action")
