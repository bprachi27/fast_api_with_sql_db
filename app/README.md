

## Uvicorn Server

To start uviorn server:
 - uvicorn main:app --reload


## Alembic as Migration tool

To add empty migration:
 - alembic revision -m "migration message"

To add auto-generate migration:
 - alembic revision --autogenerate -m "migration message"

To downgrade migration:
 - alembic downgrade head -1(number of migration you want to go back)
 - alembic downgrade 8ac14e223d1e(identifier of migration you want to go back)

To commit/upgrade migratin( this command will make changes in database):
 - alembic upgrade head
 
## note
always check migration file before migrating it.


