from app import create_app, db

# db.create_all(app=create_app())
app = create_app()
app.run(host='127.0.0.1', port=3000)