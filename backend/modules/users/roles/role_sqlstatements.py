CREATE_ROLE = """
    INSERT INTO roles (id, role, permissions, is_active, created_at, updated_at,
        created_by, updated_by)
    VALUES(:id, :role, :permissions, :is_active, :created_at, :updated_at,
        :created_by, :updated_by)
    RETURNING id, role, permissions, created_by, updated_by;
"""

GET_ROLE_BY_NAME = """
    SELECT id, role, permissions FROM roles 
    WHERE role = :role; 
"""


def role_list_search():
    return " WHERE LOWER(ro.role) ILIKE :search "


def role_list_sort(order: str | None, direction: str | None) -> str:
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY ro.role ASC;"
    elif order == "role" and direction == "DESC":
        sql_sentence = " ORDER BY ro.role DESC;"
    elif order == "role" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY ro.role ASC;"
    elif order == "estatus" and direction == "DESC":
        sql_sentence = " ORDER BY ro.is_active DESC;"
    elif order == "estatus" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY ro.is_active ASC;"

    return sql_sentence


GET_ROLES_LIST = """
    SELECT ro.id, ro.role, ro.permissions, ro.is_active, 
        ro.created_at, us1.fullname AS created_by,
        ro.updated_at, us2.fullname AS updated_by
    FROM roles AS ro
    LEFT JOIN users AS us1 ON ro.created_by = us1.id
    LEFT JOIN users AS us2 ON ro.updated_by = us2.id
"""

GET_ROLES_LIST_FUNCTIONALITY = """
    SELECT ro.id, ro.role, ro.permissions, ro.is_active, 
        ro.created_at, us1.fullname AS created_by,
        ro.updated_at, us2.fullname AS updated_by
    FROM roles AS ro
    LEFT JOIN users AS us1 ON ro.created_by = us1.id
    LEFT JOIN users AS us2 ON ro.updated_by = us2.id
    WHERE :permit LIKE ANY(ro.permissions)
"""

GET_ROLE_BY_ID = """
    SELECT id, role, permissions, is_active FROM roles 
    WHERE id = :id; 
"""

UPDATE_ROLE_BY_ID = """
    UPDATE roles
    SET role        = :role,
        permissions = :permissions,
        created_at  = :created_at,
        created_by  = :created_by,
        updated_by  = :updated_by,
        updated_at  = :updated_at,
        is_active   = :is_active
    WHERE id = :id
    RETURNING id, role, permissions, is_active, created_by, updated_by;
"""

DELETE_ROLE_BY_ID = """
    DELETE from roles
    WHERE id = :id
    RETURNING id
"""
