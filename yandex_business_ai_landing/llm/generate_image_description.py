import time
from flask import jsonify
from yandex_business_ai_landing.model import UserFile, LongOperation
from yandex_business_ai_landing.extensions import executor, db
from yandex_business_ai_landing.llm.mistral import MistralRequest
import json

generateImageDescriptionSystemPrompt = """
Вы эксперт по созданию контента для компании, описанной ниже.

Ваша задача - проанализировать изображение и создать подробное описание,
которое соответствует экспертным знаниям и ценностям компании,
обеспечивая возможность использовать его для написания экспертной статьи.

Включите следующее:
1. Ключевые элементы, видимые на изображении (например, объекты, инструменты, техники или конкретные модели, относящиеся к услугам компании).
2. Услуги, которые изображение может иллюстрировать, непосредственно связанные с областью деятельности компании.
3. Контекстные детали, которые могут вдохновить статью, связывая изображение с отраслью, экспертными знаниями или уникальными ценностями компании (например, решение проблем клиентов, использование инновационных методов и т.д.).
4. Убедитесь, что описание отражает идентичность компании и избегает неуместных или вводящих в заблуждение ассоциаций.

Используйте название компании и предоставленную дополнительную информацию для повышения релевантности и профессионализма описания. Используйте около 4000 токенов для описания.
"""

def generateImageDescription(params, request_id, user_id, userPrompt, companyInfo):
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
    prompt = (userPrompt if userPrompt else generateImageDescriptionSystemPrompt) + companyInfo

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
        for param in params:
            if param.get('name') == 'image_url':
                image_url = param.get('value')

        try:
            response = llm_request.describe_image(prompt, image_url)
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