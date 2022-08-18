npm --prefix ../../templates/default run build
source .venv/bin/activate
pip install --upgrade --force-reinstall --no-cache-dir ../../
python qa.py
