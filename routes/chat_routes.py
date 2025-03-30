from flask import Blueprint, render_template, request, jsonify
from models.chat_models import insert_post_to_db, query_posts

chat_bp = Blueprint('chat', __name__, template_folder="../views")


@chat_bp.route('/')
@chat_bp.route('/chat/')
def chat_page():
    return render_template('chat.html')


@chat_bp.route('/add-post', methods=['POST']) 
def add_post():
    data = request.json  
    comment_text = data.get('text')

    insert_post_to_db(comment_text)

    return jsonify({'message': 'Post added successfully!'}), 201


@chat_bp.route('/get-posts', methods=['GET'])
def get_posts():
    posts_data = []
    data_from_database = query_posts()


    for line in data_from_database:
        post_id, content, created_at = line
        posts_data.append({'post_id': post_id, 'content': content, 'created_at': created_at})
        
    return jsonify(posts=posts_data), 200

