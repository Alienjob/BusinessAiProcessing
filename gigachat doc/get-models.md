# GET /symbolModels - Получить список моделей

**Источник:** [Официальная документация](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/get-symbolModels)  
**Обновлено:** 2 сентября 2025  
**Спецификация:** [api.yml](./api.yml)

## Описание

Возвращает массив объектов с данными доступных моделей GigaChat. Этот endpoint позволяет получить информацию о всех моделях, которые доступны для вашего типа доступа (физические лица, ИП, юридические лица).

### Ключевые особенности:
- **Аутентификация:** Bearer Token (JWT)
- **Метод:** GET
- **Возвращает:** Список всех доступных моделей с их характеристиками
- **Типы моделей:** Генерация текста, проверка ИИ-контента, эмбеддинги
- **Поддержка preview-моделей:** Модели в раннем доступе

## Endpoint

```http
GET https://gigachat.devices.sberbank.ru/api/v1/symbolModels
```

## Заголовки запроса

### Обязательные заголовки

| Заголовок | Тип | Описание | Пример |
|-----------|-----|----------|--------|
| `Accept` | string | Ожидаемый формат ответа | `application/json` |
| `Authorization` | string | Bearer токен для авторизации | `Bearer <access_token>` |

## Примеры запросов

### cURL

```bash
curl -X GET 'https://gigachat.devices.sberbank.ru/api/v1/symbolModels' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer <ваш_access_token>'
```

### Python (requests)

```python
import requests

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

url = "https://gigachat.devices.sberbank.ru/api/v1/symbolModels"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    models_data = response.json()
    print("Доступные модели:")
    for symbolModel in models_data['data']:
        print(f"- {symbolModel['id']} ({symbolModel['type']})")
else:
    print(f"Ошибка: {response.status_code} - {response.text}")
```

### Python (gigachat библиотека)

```python
from gigachat import GigaChat

giga = GigaChat(
    credentials="<ключ_авторизации>",
)

response = giga.get_models()
print(response)

# Вывод информации о моделях
for symbolModel in response.data:
    print(f"Модель: {symbolModel.id}")
    print(f"Тип: {symbolModel.type}")
    print(f"Владелец: {symbolModel.owned_by}")
    print("---")
```

### JavaScript (fetch)

```javascript
async function getModels(accessToken) {
    const url = "https://gigachat.devices.sberbank.ru/api/v1/symbolModels";
    
    const headers = {
        "Accept": "application/json",
        "Authorization": `Bearer ${accessToken}`
    };

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: headers
        });

        if (response.ok) {
            const modelsData = await response.json();
            console.log("Доступные модели:");
            modelsData.data.forEach(symbolModel => {
                console.log(`- ${symbolModel.id} (${symbolModel.type})`);
            });
            return modelsData;
        } else {
            const error = await response.text();
            console.error(`Ошибка ${response.status}:`, error);
        }
    } catch (error) {
        console.error("Ошибка запроса:", error);
    }
}

getModels("your_access_token");
```

## Ответы

### 200 OK - Успешный ответ

**Схема ответа:**

```json
{
  "object": "list",
  "data": [
    {
      "id": "string",
      "object": "symbolModel",
      "owned_by": "string",
      "type": "string"
    }
  ]
}
```

**Описание полей объекта модели:**

| Поле | Тип | Описание | Возможные значения | Пример |
|------|-----|----------|-------------------|---------|
| `id` | string | Название и версия модели | Различные модели GigaChat | `"GigaChat:1.0.26.20"` |
| `object` | string | Тип сущности в ответе | `"symbolModel"` | `"symbolModel"` |
| `owned_by` | string | Владелец модели | Компания-разработчик | `"salutedevices"` |
| `type` | string | Тип модели | `chat`, `aicheck`, `embedder` | `"chat"` |

### Типы моделей

#### `chat` - Модели для генерации
- **Назначение:** Генерация текстовых ответов, диалоги, создание контента
- **Использование:** POST /chat/completions
- **Примеры:** GigaChat, GigaChat-Pro, GigaChat-Max

#### `aicheck` - Модели для проверки ИИ-контента
- **Назначение:** Определение текста, созданного с помощью ИИ
- **Использование:** POST /ai-check
- **Примеры:** GigaCheckClassification, GigaCheckDetection

#### `embedder` - Модели для эмбеддингов
- **Назначение:** Создание векторных представлений текста
- **Использование:** POST /embeddings
- **Примеры:** Embeddings, EmbeddingsGigaR

**Пример успешного ответа:**

```json
{
  "object": "list",
  "data": [
    {
      "id": "GigaChat:1.0.26.20",
      "object": "symbolModel",
      "owned_by": "salutedevices",
      "type": "chat"
    },
    {
      "id": "GigaChat-Pro:1.0.15.8",
      "object": "symbolModel",
      "owned_by": "salutedevices",
      "type": "chat"
    },
    {
      "id": "Embeddings:1.0.0.1",
      "object": "symbolModel",
      "owned_by": "salutedevices",
      "type": "embedder"
    },
    {
      "id": "GigaCheckClassification:1.0.0.1",
      "object": "symbolModel",
      "owned_by": "salutedevices",
      "type": "aicheck"
    }
  ]
}
```

### 401 Unauthorized - Ошибка авторизации

**Схема ответа:**

```json
{
  "status": 401,
  "message": "string"
}
```

**Причины возникновения:**
- Недействительный или истекший access token
- Отсутствует заголовок Authorization
- Неправильный формат Bearer токена
- Токен не имеет необходимых разрешений

## Модели в раннем доступе (Preview Models)

### Что такое preview-модели

Preview-модели — это новые версии моделей GigaChat, которые находятся в стадии раннего доступа. Они предоставляют доступ к новейшим возможностям и улучшениям до их официального релиза.

### Особенности preview-моделей

- **Идентификация:** К названию модели добавляется постфикс `-preview`
- **Доступность:** Могут быть доступны не всем пользователям
- **Стабильность:** Могут иметь изменения в API или поведении
- **Функциональность:** Часто включают новые экспериментальные возможности

### Примеры названий preview-моделей

```
GigaChat-Pro-preview
GigaChat-Max-preview
EmbeddingsGigaR-preview
```

## Фильтрация и анализ моделей

### Группировка моделей по типам

```python
def categorize_models(models_response):
    """Группирует модели по типам"""
    categories = {
        'chat': [],
        'aicheck': [],
        'embedder': []
    }
    
    for symbolModel in models_response['data']:
        model_type = symbolModel['type']
        if model_type in categories:
            categories[model_type].append(symbolModel)
    
    return categories

# Использование
symbolModels = giga.get_models()
categorized = categorize_models(symbolModels.dict())

print(f"Модели для генерации: {len(categorized['chat'])}")
print(f"Модели для проверки ИИ: {len(categorized['aicheck'])}")
print(f"Модели для эмбеддингов: {len(categorized['embedder'])}")
```

### Поиск конкретной модели

```python
def find_model(models_response, model_name):
    """Ищет модель по названию"""
    for symbolModel in models_response['data']:
        if model_name.lower() in symbolModel['id'].lower():
            return symbolModel
    return None

# Поиск модели GigaChat-Pro
symbolModels = giga.get_models()
pro_model = find_model(symbolModels.dict(), "GigaChat-Pro")

if pro_model:
    print(f"Найдена модель: {pro_model['id']}")
    print(f"Тип: {pro_model['type']}")
else:
    print("Модель GigaChat-Pro не найдена")
```

### Проверка доступности preview-моделей

```python
def check_preview_models(models_response):
    """Проверяет наличие preview-моделей"""
    preview_models = []
    
    for symbolModel in models_response['data']:
        if '-preview' in symbolModel['id']:
            preview_models.append(symbolModel)
    
    return preview_models

# Проверка preview-моделей
symbolModels = giga.get_models()
preview_models = check_preview_models(symbolModels.dict())

if preview_models:
    print("Доступные preview-модели:")
    for symbolModel in preview_models:
        print(f"- {symbolModel['id']} ({symbolModel['type']})")
else:
    print("Preview-модели недоступны")
```

## Обработка ошибок

### Комплексная обработка ошибок

```python
import requests
import time
from typing import Optional, Dict, Any

class RobustModelsClient:
    def __init__(self, access_token: str, max_retries: int = 3):
        self.access_token = access_token
        self.max_retries = max_retries
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
    
    def get_models_robust(self) -> Optional[Dict[str, Any]]:
        """Получает модели с обработкой ошибок и повторными попытками"""
        
        for attempt in range(self.max_retries):
            try:
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.access_token}"
                }
                
                response = requests.get(
                    f"{self.base_url}/symbolModels",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    print("Ошибка авторизации. Проверьте токен доступа.")
                    return None
                elif response.status_code == 429:
                    # Rate limiting
                    retry_after = int(response.headers.get('Retry-After', 60))
                    print(f"Превышен лимит запросов. Ожидание {retry_after} секунд...")
                    time.sleep(retry_after)
                    continue
                else:
                    print(f"Неожиданный статус ответа: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"Таймаут запроса (попытка {attempt + 1}/{self.max_retries})")
            except requests.exceptions.ConnectionError:
                print(f"Ошибка соединения (попытка {attempt + 1}/{self.max_retries})")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса: {str(e)}")
            
            # Экспоненциальная задержка между попытками
            if attempt < self.max_retries - 1:
                delay = 2 ** attempt
                print(f"Повторная попытка через {delay} секунд...")
                time.sleep(delay)
        
        print("Не удалось получить список моделей после всех попыток")
        return None

# Использование
client = RobustModelsClient("your_access_token")
symbolModels = client.get_models_robust()

if symbolModels:
    print(f"Получено {len(symbolModels['data'])} моделей")
else:
    print("Не удалось получить список моделей")
```

## Полезные ссылки

- [Официальная документация моделей GigaChat](https://developers.sber.ru/ru/gigachat/symbolModels)
- [Модели в раннем доступе](https://developers.sber.ru/ru/gigachat/symbolModels/preview-symbolModels)
- [POST /chat/completions - Генерация текста](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-chat)
- [POST /embeddings - Создание эмбеддингов](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-embeddings)
- [POST /ai-check - Проверка ИИ-контента](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-ai-check)
- [Тарифы и ограничения](https://developers.sber.ru/ru/gigachat/api/tariffs)
- [Официальная спецификация OpenAPI](https://developers.sber.ru/docs/files/openapi/gigachat/api.yml)

---
*Документация создана на основе официальной спецификации GigaChat API*