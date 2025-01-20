from flask import jsonify, request
from yandex_business_ai_landing.model import LongOperation, Post, UserFile
from yandex_business_ai_landing.extensions import executor, db
from datetime import datetime

def scheduledPost(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    # params : []
    now = datetime.now()

    post = Post.query.filter_by(user_id=user_id_int, status='draft').filter(Post.posting_time < now).first()

    if post is None:
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'id': '',
                'image_url': '',
                'content': '',
            },
            'id': request_id
        })

    image = UserFile.query.get(post.user_file_id)
    absolute_url = f"{image.url.lstrip('/')}"
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': post.id,
            'image_url': absolute_url,
            'content': post.post_content,
        },
        'id': request_id
    })
