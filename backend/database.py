import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """データベースを作成する"""
    try:
        # PostgreSQLに接続
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password"  # 実際のパスワードに変更してください
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # データベースが存在するかチェック
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'dateapp'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE dateapp')
            print("データベース 'dateapp' を作成しました")
        else:
            print("データベース 'dateapp' は既に存在します")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"データベース作成エラー: {e}")

if __name__ == "__main__":
    create_database()
