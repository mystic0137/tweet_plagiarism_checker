from app import app

if __name__ == "__main__":
    # This block only executes when running the file directly
    # It won't run when imported by a WSGI server
    app.run()
