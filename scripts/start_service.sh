#alembic upgrade head &&
#python back/cli.py create-user --name admin --email admin@mail.ru --password admin &&
uvicorn back.main:app --host 0.0.0.0 --port 8000 --reload