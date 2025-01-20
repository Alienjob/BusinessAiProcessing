function generateDescription(fileId, postId) {
    const btn = document.getElementById(`generateDescBtn_${postId}`);
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generating...';
    }

    fetch(`/generate_description/${fileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: Date.now() })
    }).then(response => response.json())
        .then(data => {
            const operationId = data.id;
            pollOperationStatus(operationId, `photo_description_${postId}`, () => {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = 'Сгенерировать<br>описание';
                }
                autosize.update(document.getElementById(`photo_description_${postId}`));
            });
        })
        .catch(error => {
            console.error('Error:', error);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Сгенерировать<br>описание';
            }
        });
}

function generatePostContent(fileId, postId) {
    const btn = document.getElementById(`generatePostBtn_${postId}`);
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generating...';
    }

    fetch(`/generate_post_content/${fileId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: Date.now(),
            image_description: document.getElementById(`photo_description_${postId}`).value
        })
    })
        .then(response => response.json())
        .then(data => {
            const operationId = data.id;
            pollOperationStatus(operationId, `post_content_${postId}`, () => {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = 'Сгенерировать<br>содержание поста';
                }
                autosize.update(document.getElementById(`post_content_${postId}`));
            });
        })
        .catch(error => {
            console.error('Error:', error);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Сгенерировать<br>содержание поста';
            }
        });
}

function generateIssueResponse(issueId) {
    const btn = document.getElementById(`generateResponseBtn_${issueId}`);
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generating...';
    }

    const reviewText = document.getElementById(`review_text_${issueId}`).value;
    const companyStory = document.getElementById(`company_story_${issueId}`).value;

    fetch(`/generate_issue_response/${issueId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: Date.now(),
            review_text: reviewText,
            company_story: companyStory
        })
    }).then(response => response.json())
        .then(data => {
            const operationId = data.id;
            pollOperationStatus(operationId, `company_response_${issueId}`, () => {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = 'Сгенерировать ответ';
                }
                autosize.update(document.getElementById(`company_response_${issueId}`));
            });
        })
        .catch(error => {
            console.error('Error:', error);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Сгенерировать ответ';
            }
        });
}

async function pollOperationStatus(operationId, elementId, onFinished) {
    const pollInterval = 3000;
    const timeout = 120000;
    const startTime = Date.now();

    try {
        while (Date.now() - startTime < timeout) {
            const response = await fetch(`/operation_result/${operationId}`);
            const data = await response.json();

            if (data.status === 'done' || data.status === 'error') {
                document.getElementById(elementId).value = data.response || data.error;
                if (onFinished) onFinished();
                return;
            }
            await new Promise(resolve => setTimeout(resolve, pollInterval));
        }
        console.error('Polling timed out');
        if (onFinished) onFinished();
    } catch (error) {
        console.error('Error:', error);
        if (onFinished) onFinished();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    autosize(document.querySelectorAll('textarea'));
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', () => autosize.update(textarea));
    });
});