from flask import jsonify
from yandex_business_ai_landing.model import LongOperation
from yandex_business_ai_landing.extensions import executor, db
from yandex_business_ai_landing.llm.mistral import MistralRequest
import time
import json

writeTopicSystemPrompt = """
Вы экспертный писатель, создающий профессиональные статьи для укрепления доверия к услугам компании.
На основе предоставленного подробного описания изображения напишите краткую, самодостаточную статью на одну тему на русском языке.

Статья должна:
1. Четко фокусироваться на одной услуге или теме, относящейся к экспертным знаниям компании.
2. Укреплять доверие, демонстрируя профессионализм, опыт и ценность компании для клиентов.
3. Включать практические инсайты, уникальные вызовы или экспертные советы, чтобы показать авторитет компании в своей области.
4. Быть написана в дружелюбном и профессиональном тоне, делая ее доступной и увлекательной для потенциальных клиентов.
5. Избегать прямых ссылок на изображение, обеспечивая полную самодостаточность статьи, а изображение просто дополняет ее.

Используйте название компании и предоставленную дополнительную информацию для повышения релевантности и профессионализма статьи.
Сделайте статью релевантной для отрасли, услуг или экспертных знаний компании, как описано.
Длина текста — до 2000 букв с учетом пробелов.
"""

def generatePostContent(params, request_id, user_id, userPrompt, companyInfo, imageDescription):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    # Convert the params dictionary to a JSON string
    params_json = json.dumps(params, ensure_ascii=False)

    # Create a new long operation
    new_operation = LongOperation(
        user_id=user_id_int,
        status='processing',
        request=params_json,
        response=None,
        error=None
    )
    db.session.add(new_operation)
    db.session.commit()

    # Set the prompt. if userPrompt is not None, use it, otherwise use the systemPrompt
    prompt = (userPrompt if userPrompt else writeTopicSystemPrompt) + companyInfo + imageDescription

    # Start the background task
    executor.submit(process_long_operation, new_operation.id, user_id_int, params, prompt)

    # Return the CreateOperationResponse
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': new_operation.id,
            'status': new_operation.status
        },
        'id': request_id
    })

def process_long_operation(operation_id, user_id, params, prompt):
    try:
        llm_request = MistralRequest()

        # Extract values from the params
        image_url = None
        image_description = None
        for param in params:
            if param.get('name') == 'image_url':
                image_url = param.get('value')
            if param.get('name') == 'image_description':
                image_description = param.get('value')

        try:
            response = llm_request.write_topic(prompt)
            status = 'done'
            error = None
        except Exception as e:
            response = None
            status = 'error'
            error = str(e)
            print(f'Error processing long operation: {e}')

        operation = LongOperation.query.get(operation_id)
        operation.status = status
        operation.response = response
        operation.error = error
        db.session.commit()

    except Exception as e:
        print(f'Error processing long operation: {e}')
        operation = LongOperation.query.get(operation_id)
        operation.status = 'error'
        operation.error = str(e)
        db.session.commit()