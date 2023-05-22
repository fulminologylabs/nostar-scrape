3. init_db.sh script from qs_prod (Rust QuickStart)
    - Adapt init_db.sh to Python/Alembic
    - How do we create the DB Schema programmatically with Alembic?

    - Fix FK Constraints on the alembic revision
    - Confirm connection to Postgres and that the relationships appear to be set properly
    - Create the models and schema in Pydantic

4. Write the daily and onboard processes for the scheduler
5. Add additional tests
6. Write Relays, Relay Configs, Job Config, Filter Config, Subscription Record Database
    - Populate the DB with some data