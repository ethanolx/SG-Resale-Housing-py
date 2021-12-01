from app import create_app

if __name__ == '__main__':
    dev_app = create_app(env='development')
    dev_app.run()
