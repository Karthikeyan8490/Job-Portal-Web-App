"""Job Portal - Application Entry Point"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 40)
    print("  Job Portal Web App")
    print("  Visit: http://localhost:5000")
    print("=" * 40)
    app.run(debug=True, host='0.0.0.0', port=5000)
