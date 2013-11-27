from webapp import create_app


def main():
    app = create_app('config_production.cfg')

    from webapp.redeem import redeem
    app.register_blueprint(redeem, url_prefix='/redeem')

    app.run(host=app.config.get('SERVER_IP'),
            port=app.config.get('SERVER_PORT'),
            debug=app.config.get('DEBUG'))

if __name__ == '__main__':
    main()
