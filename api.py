from flask import Blueprint, request, jsonify
from models import db, Role, User
import json

api = Blueprint("api", __name__)



@api.route("/api/roles", methods=["GET"])
def get_roles():
    roles = Role.query.order_by(Role.id).all()
    return jsonify([r.to_summary() for r in roles])


#get role

@api.route("/api/roles/<int:role_id>", methods=["GET"])
def get_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "not found"}), 404
    return jsonify(role.to_dict())

#post role 

@api.route("/api/roles", methods=["POST"])
def create_role():
    data = request.json or {}

    name = (data.get("name") or "").strip()
    privileges = data.get("privileges") or {}
    assigned_users = data.get("assigned_users") or []

    if not name:
        return jsonify({"error": "missing name"}), 400

    if Role.query.filter_by(name=name).first():
        return jsonify({"error": "role exists"}), 400

    role = Role(
        name=name,
        privileges=json.dumps(privileges),
        assigned_users=json.dumps(assigned_users)
    )

    db.session.add(role)
    db.session.commit()

    return jsonify({
        "message": "role created",
        "role": role.to_dict()
    })




#put roles added
@api.route("/api/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "not found"}), 404

    data = request.json or {}

    name = data.get("name")
    privileges = data.get("privileges")
    assigned_users = data.get("assigned_users")

    if name:
        name = name.strip()
        if Role.query.filter(Role.name == name, Role.id != role_id).first():
            return jsonify({"error": "role name conflict"}), 400
        role.name = name

    if privileges is not None:
        role.privileges = json.dumps(privileges)

    if assigned_users is not None:
        role.assigned_users = json.dumps(assigned_users)

    db.session.commit()

    return jsonify({
        "message": "updated",
        "role": role.to_dict()
    })


#delete api

@api.route("/api/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"error": "not found"}), 404

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "deleted"})



#duplicate role

@api.route("/api/roles/<int:role_id>/duplicate", methods=["POST"])
def duplicate_role(role_id):
    original = Role.query.get(role_id)
    if not original:
        return jsonify({"error": "not found"}), 404

    new_role = Role(
        name=f"{original.name} Copy",
        privileges=original.privileges,
        assigned_users=original.assigned_users
    )

    db.session.add(new_role)
    db.session.commit()

    return jsonify({
        "message": "duplicated",
        "role": new_role.to_dict()
    })

#user api

@api.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([u.to_dict() for u in users])


#get user api

@api.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify(user.to_dict())

#post user api

@api.route("/api/users", methods=["POST"])
def create_user():
    data = request.json or {}

    name = (data.get("name") or "").strip()
    role = data.get("role")
    email = (data.get("email") or "").strip() or None
    phone = (data.get("phone") or "").strip() or None
    branch = (data.get("branch") or "").strip() or None

    if not name:
        return jsonify({"error": "missing name"}), 400

    if User.query.filter_by(name=name).first():
        return jsonify({"error": "user exists"}), 400

    user = User(
        name=name,
        role=role,
        email=email,
        phone=phone,
        branch=branch
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "user added",
        "user": user.to_dict()
    })

#put user api

@api.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404

    data = request.json or {}

    if "name" in data:
        new_name = (data.get("name") or "").strip()
        if new_name and User.query.filter(User.name == new_name, User.id != user_id).first():
            return jsonify({"error": "name already exists"}), 400
        if new_name:
            user.name = new_name

    if "role" in data:
        user.role = data.get("role")

    if "email" in data:
        user.email = data.get("email")

    if "phone" in data:
        user.phone = data.get("phone")

    if "branch" in data:
        user.branch = data.get("branch")

    db.session.commit()

    return jsonify({
        "message": "updated",
        "user": user.to_dict()
    })

#delete user api

@api.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "deleted"})
