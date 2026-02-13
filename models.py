from flask_sqlalchemy import SQLAlchemy
import datetime, json

db = SQLAlchemy()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    privileges = db.Column(db.Text, nullable=False, default='{}')
    assigned_users = db.Column(db.Text, nullable=False, default='[]')
    created_at = db.Column(
        db.String(64),
        nullable=False,
        default=lambda: datetime.datetime.utcnow().isoformat()
    )

    def to_summary(self):
        privs = json.loads(self.privileges or "{}")
        priv_count = sum(len(set(v)) for v in privs.values())
        return {
            "id": self.id,
            "name": self.name,
            "privileges_count": priv_count,
            "modules_count": len(privs),
            "assigned_users": json.loads(self.assigned_users or "[]")

        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "privileges": json.loads(self.privileges or "{}"),
            "assigned_users": json.loads(self.assigned_users or "[]"),
            "created_at": self.created_at
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True, nullable=False)
    role = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(220), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    branch = db.Column(db.String(120), nullable=True)
    created_at = db.Column(
        db.String(64),
        nullable=False,
        default=lambda: datetime.datetime.utcnow().isoformat()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "phone": self.phone,
            "branch": self.branch,
            "created_at": self.created_at
        }
