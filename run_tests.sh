#!/bin/bash

# Install dependencies (if not already installed)
pip install -r /workspace/yandex_ai_back_end/requirements.txt

# Set up environment variables (if needed)
export FLASK_ENV=testing
export DATABASE_URL=sqlite:///test.db

export PYTHONPATH=/workspace/yandex_ai_back_end

# Generate coverage report (optional)
pytest --cov=yandex_business_ai_landing /workspace/yandex_ai_back_end/tests/

# Clean up (if needed)
rm -f  /workspace/yandex_ai_back_end/instance/test.db
