from flask_jwt_extended import get_jwt_identity, jwt_required
from Stackoverflowlite import models
MY_USER = models.Users()


@jwt_required
def get_logged_in_user():
    return MY_USER.get_user_by_field(key='username', value=get_jwt_identity())
