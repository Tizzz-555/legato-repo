from legato import create_app

# Run only when executed directly, not as an import
if __name__ == "__main__":
    # Call to create_app from __init__.py
    app = create_app()
    # Start development server in debug mode
    app.run(debug=True)
