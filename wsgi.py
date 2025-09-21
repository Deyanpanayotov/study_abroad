from study_abroad.app import app

# Gunicorn looks for 'app' in this file
if __name__ == "__main__":
    app.run()
