3. init_db.sh script from qs_prod (Rust QuickStart)
    - Adapt init_db.sh to Python/Alembic
    - How do we create the DB Schema programmatically with Alembic?
    - Fix FK Constraints on the alembic revision
    - Add indices and confirm unique constraints in the alembic revision 
    - Create models/schemas --> scrap schemas for mapping functions
    - Read: https://docs.sqlalchemy.org/en/20/core/metadata.html#accessing-tables-and-columns
    - Transitions TextNote Table, Model, Alembic code to Event table
    - Transition EventKind PK to not be AUTO INCREMENT

    - Read about SQLAlchemy ORM: https://docs.sqlalchemy.org/en/20/orm/
    - Read about SQLAlchemy Integration with dataclasses: https://docs.sqlalchemy.org/en/20/orm/dataclasses.html
    - Read about Tornado and explore Async options
    - Read: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    - Determine what type to use for `content` on the Event table

    - Pre-populate some data (within pipeline)
    - Test downgrade
    - Establish DB Connection code for the application itself (https://testdriven.io/blog/fastapi-sqlmodel/)
    - Upgrade SQLModel and Alebmic to use async code (https://alembic.sqlalchemy.org/en/latest/cookbook.html)

4. Write the daily and onboard processes for the scheduler
5. Fix tests
6. Write Relays, Relay Configs, Job Config, Filter Config, Subscription Record Database
7. Logging system