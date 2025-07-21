from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dateapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Gemini API設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# データベースモデル
class DatePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    ai_comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'activity': self.activity,
            'budget': self.budget,
            'duration': self.duration,
            'description': self.description,
            'score': self.score,
            'comment': self.ai_comment,
            'createdAt': self.created_at.isoformat()
        }

# AI分析関数
def analyze_date_plan(data):
    prompt = f"""
    以下のデートプランを分析して、偏差値（50-100）とコメントを日本語で提供してください。
    
    タイトル: {data['title']}
    場所: {data['location']}
    アクティビティ: {data['activity']}
    予算: {data['budget']}円
    時間: {data['duration']}
    詳細: {data['description']}
    
    以下の要素を考慮して偏差値を算出してください：
    - 創造性・オリジナリティ
    - 予算の適切性
    - 場所の選択
    - 時間配分
    - 相手への配慮
    
    回答は以下の形式でお願いします：
    偏差値: [数値]
    コメント: [100文字程度のアドバイス]
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 偏差値とコメントを抽出
        lines = content.strip().split('\n')
        score = 75  # デフォルト値
        comment = "素晴らしいデートプランです！"
        
        for line in lines:
            if '偏差値:' in line or '偏差値：' in line:
                try:
                    score = int(''.join(filter(str.isdigit, line)))
                    if score < 50:
                        score = 50
                    elif score > 100:
                        score = 100
                except:
                    pass
            elif 'コメント:' in line or 'コメント：' in line:
                comment = line.split(':', 1)[-1].split('：', 1)[-1].strip()
        
        return score, comment
    except Exception as e:
        print(f"AI分析エラー: {e}")
        return 75, "分析中にエラーが発生しましたが、良いデートプランだと思います！"

# API エンドポイント
@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        
        # AI分析
        score, ai_comment = analyze_date_plan(data)
        
        # データベースに保存
        new_post = DatePost(
            title=data['title'],
            location=data['location'],
            activity=data['activity'],
            budget=int(data['budget']),
            duration=data['duration'],
            description=data['description'],
            score=score,
            ai_comment=ai_comment
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'score': score,
            'comment': ai_comment,
            'post': new_post.to_dict()
        })
        
    except Exception as e:
        print(f"投稿作成エラー: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        posts = DatePost.query.order_by(DatePost.score.desc()).all()
        return jsonify({
            'success': True,
            'posts': [post.to_dict() for post in posts]
        })
    except Exception as e:
        print(f"投稿取得エラー: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Backend is running'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
