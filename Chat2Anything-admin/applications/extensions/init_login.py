from flask_login import LoginManager


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = 'system.passport.login'

    @login_manager.user_loader
    def load_user(user_id):
        from applications.models import User
        user = User.query.get(int(user_id))
        return user
