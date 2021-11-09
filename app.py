from app import create_app

site_app = create_app()
site_app.run(host='127.0.0.1', port=3000)
