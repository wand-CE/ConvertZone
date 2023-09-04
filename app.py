from website import create_app, create_tables

app = create_app()

if __name__ == '__main__':
    create_tables(app)
    app.run(debug=True, host='0.0.0.0')
