import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    
    print("🚀 Starting AI Career Connect Flask Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
