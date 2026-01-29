# import os
# from app import create_app

# print("Current working directory:", os.getcwd())  # Print current working directory

# # Create an instance of the Flask application
# app = create_app()

# if __name__ == '__main__':
#     # Run the Flask application on all available IPs and specify the port
#     print("Flask app is running on http://127.0.0.1:5000/")
#     app.run(host='127.0.0.1', port=5000, debug=True)  # Use 127.0.0.1 for local access
import os
from app import create_app

# Create Flask app
app = create_app()

print("✅ Flask app loaded successfully")
print("📂 Current working directory:", os.getcwd())

if __name__ == "__main__":
    print("🚀 Flask app is running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

# import os
# from app import create_app

# # Create Flask application
# app = create_app()

# # Optional: helpful log for debugging
# print("✅ Flask app loaded successfully")
# print("📁 Current working directory:", os.getcwd())
