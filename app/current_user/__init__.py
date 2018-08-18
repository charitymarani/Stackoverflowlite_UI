from flask_jwt_extended import get_jwt_identity, jwt_required
from challenge2.app.api.v1.auth import auth_model
MY_USER = auth_model.Users()


@jwt_required
def get_logged_in_user():
    return MY_USER.get_user_by_field(key='username', value=get_jwt_identity())
