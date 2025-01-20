from flask import jsonify
from yandex_business_ai_landing.model import LongOperation, Post
from yandex_business_ai_landing.extensions import executor, db

def markPostAsPublished(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    # Extract the post_id from the params list
    post_id = None
    for param in params:
        if param.get('name') == 'post_id':
            post_id = param.get('value')
            break
    post_id_int = int(post_id)

    post = Post.query.filter_by(user_id=user_id_int, id=post_id_int).first()
    if post is None:
        return jsonify({
            'jsonrpc': '2.0',
            'error': 'Invalid post ID',
            'id': request_id
        })

    post.status = 'published'
    db.session.commit()

    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': post.id,
        },
        'id': request_id
    })