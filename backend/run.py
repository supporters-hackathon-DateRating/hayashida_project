from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("データベーステーブルを作成しました")
    
    print("サーバーを起動しています...")
    print("URL: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
