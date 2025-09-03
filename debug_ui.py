from urllib.parse import parse_qs
import html

DEFAULT_IMAGE_URL = 'https://metaphysica-parfums.com/wp-content/uploads/2025/08/5d903ab13fd79a8c8e8dee91b05fa507.jpg'

def _render(self, defaultPublicationPrompt: str, defaultImagePrompt: str, env, values=None, outputs=None):
    values = values or {}
    outputs = outputs or {}
    defaults = {
        'orgName': '',
        'assortmentName': '',
        'description': '',
        'imageDescription': '',
        'pub_prompt': defaultPublicationPrompt,
        'pub_char_limit': str(env.get("python.max_chars_for_publication", 2500)),
        'img_prompt': defaultImagePrompt,
        'img_token_limit': str(env.get("python.max_tokens_for_describe_image", 500)),
        'imageUrl': DEFAULT_IMAGE_URL,
    }
    defaults.update({k: v for k, v in values.items() if v is not None})

    def esc(s: str):
        return html.escape(s or '')

    describe_result = outputs.get('describe_result')
    publication_result = outputs.get('publication_result')

    page = f"""
    <html><head><title>Debug UI</title><meta charset='utf-8'></head>
    <body>
    <h1>Это страница для отладки</h1>

    <h2>Генерация описания изображения</h2>
    <form method="post" action="/debug">
      <input type="hidden" name="action" value="describe" />
      <label>Название организации:<br><input type="text" name="orgName" value="{esc(defaults['orgName'])}" style="width:480px"/></label><br><br>
      <label>URL изображения:<br><input type="text" name="imageUrl" value="{esc(defaults['imageUrl'])}" style="width:640px"/></label><br><br>
      <label>Название ассортимента/услуги:<br><input type="text" name="assortmentName" value="{esc(defaults['assortmentName'])}" style="width:480px"/></label><br><br>
      <label>Промпт:<br><textarea name="img_prompt" rows="6" style="width:800px">{esc(defaults['img_prompt'])}</textarea></label><br><br>
      <label>Лимит токенов:<br><input type="number" name="img_token_limit" value="{esc(defaults['img_token_limit'])}"/></label><br><br>
      <button type="submit">Сгенерировать описание</button>
    </form>
    {('<h3>Результат описания изображения:</h3><pre style="white-space:pre-wrap;">' + esc(describe_result) + '</pre>') if describe_result else ''}

    <hr/>

    <h2>Генерация публикации</h2>
    <form method="post" action="/debug">
      <input type="hidden" name="action" value="publication" />
      <label>Название организации:<br><input type="text" name="orgName" value="{esc(defaults['orgName'])}" style="width:480px"/></label><br><br>
      <label>Название ассортимента/услуги:<br><input type="text" name="assortmentName" value="{esc(defaults['assortmentName'])}" style="width:480px"/></label><br><br>
      <label>Описание ассортимента/услуги:<br><textarea name="description" rows="6" style="width:800px">{esc(defaults['description'])}</textarea></label><br><br>
      <label>Описание изображения (опционально):<br><textarea name="imageDescription" rows="4" style="width:800px">{esc(defaults['imageDescription'])}</textarea></label><br><br>
      <label>Промпт:<br><textarea name="pub_prompt" rows="6" style="width:800px">{esc(defaults['pub_prompt'])}</textarea></label><br><br>
      <label>Лимит символов:<br><input type="number" name="pub_char_limit" value="{esc(defaults['pub_char_limit'])}"/></label><br><br>
      <button type="submit">Сгенерировать публикацию</button>
    </form>
    {('<h3>Результат публикации:</h3><pre style="white-space:pre-wrap;">' + esc(publication_result) + '</pre>') if publication_result else ''}

    </body></html>
    """

    self.send_response(200)
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.end_headers()
    self.wfile.write(page.encode('utf-8'))


def handle_debug_get(self, defaultPublicationPrompt: str, defaultImagePrompt: str, env):
    _render(self, defaultPublicationPrompt, defaultImagePrompt, env)


def handle_debug_post(self, defaultPublicationPrompt: str, defaultImagePrompt: str, env,
                      gen_publication_cb, describe_image_cb):
    length = int(self.headers.get('Content-Length', 0))
    body = self.rfile.read(length).decode('utf-8') if length > 0 else ''
    form = parse_qs(body)

    action = (form.get('action') or [''])[0]
    values = {
        'orgName': (form.get('orgName') or [''])[0],
        'assortmentName': (form.get('assortmentName') or [''])[0],
        'description': (form.get('description') or [''])[0],
        'imageDescription': (form.get('imageDescription') or [''])[0],
        'pub_prompt': (form.get('pub_prompt') or [defaultPublicationPrompt])[0],
        'pub_char_limit': (form.get('pub_char_limit') or [str(env.get("python.max_chars_for_publication", 2500))])[0],
        'img_prompt': (form.get('img_prompt') or [defaultImagePrompt])[0],
        'img_token_limit': (form.get('img_token_limit') or [str(env.get("python.max_tokens_for_describe_image", 500))])[0],
        'imageUrl': (form.get('imageUrl') or [''])[0],
    }

    outputs = {}
    try:
        if action == 'describe':
            res = describe_image_cb(values['orgName'], values['imageUrl'], values['assortmentName'],
                                    values['img_prompt'], int(values['img_token_limit']))
            outputs['describe_result'] = res or ''
        elif action == 'publication':
            res = gen_publication_cb(values['orgName'], values['assortmentName'], values['description'],
                                     values['imageDescription'] or None, values['pub_prompt'], int(values['pub_char_limit']))
            outputs['publication_result'] = res or ''
    except Exception as e:
        outputs['publication_result' if action == 'publication' else 'describe_result'] = f"Ошибка: {e}"

    _render(self, defaultPublicationPrompt, defaultImagePrompt, env, values, outputs)
