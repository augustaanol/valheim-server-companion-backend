# valheim-server-companion-backend

source venv/bin/activate # Linux / Mac
lub
venv\Scripts\activate

uvicorn app.main:app --reload

alembic revision --autogenerate -m "add players table"
alembic upgrade head
