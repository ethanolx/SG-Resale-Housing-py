from app import create_app

if __name__ == '__main__':
    dev_app = create_app()
    dev_app.run(host='127.0.0.1', port=3000)