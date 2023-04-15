from flask import Flask
from decouple import config


def app_factory() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    from bp.account_bp import account
    app.register_blueprint(account)

    from bp.app_bp import app
    app.register_blueprint(app)

    from bp.plan_bp import plan
    app.register_blueprint(app)

    from bp.recs_bp import rec
    app.register_blueprint(rec)

    from bp.social_bp import main
    app.register_blueprint(main)

    # Patch Tekore

    return app


if __name__ == '__main__':
    application = app_factory()
    application.run('0.0.0.0', 5000, threaded=True)
