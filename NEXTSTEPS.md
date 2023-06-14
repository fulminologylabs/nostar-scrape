3. init_db.sh script from qs_prod (Rust QuickStart)
    - Adapt init_db.sh to Python/Alembic
    - How do we create the DB Schema programmatically with Alembic?
    - Fix FK Constraints on the alembic revision
    - Add indices and confirm unique constraints in the alembic revision 
    - Create models/schemas --> scrap schemas for mapping functions
    - Read: https://docs.sqlalchemy.org/en/20/core/metadata.html#accessing-tables-and-columns
    - Read: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#basic-relationship-patterns
    - Transitions TextNote Table, Model, Alembic code to Event table
    - Transition EventKind PK to not be AUTO INCREMENT
    - Read about SQLAlchemy ORM: https://docs.sqlalchemy.org/en/20/orm/
    - Read about SQLAlchemy Integration with dataclasses: https://docs.sqlalchemy.org/en/20/orm/dataclasses.html
    - For Models and Alembic - Determine whether to use server_default or default
    *** BOOKMARK ***
    - Read: https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
    - Examine relationships between job, batch, filter, subscription, and relay
    - Pre-populate some data (within pipeline) based on filter_handler and job_manager
    - Fill out and create tests for filter_handler and job_manager
    - Read enough information from DB to setup examples/historical v0.1 process
    - Explore Status ideas for batches / jobs
    - Test downgrade
    - Establish DB Connection code for the application itself (https://testdriven.io/blog/fastapi-sqlmodel/)
    - Read about Tornado and explore Async options
    - Read: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    - Determine what type to use for `content` on the Event table
    - Upgrade SQLModel and Alebmic to use async code (https://alembic.sqlalchemy.org/en/latest/cookbook.html)

4. Write the daily and onboard processes for the scheduler
5. Fix tests
6. Write Relays, Relay Configs, Job Config, Filter Config, Subscription Record Database
7. Logging system
8. Setup equivalent to the Rust CI/CD Pipeline
    - Is there a way to include DB migrations in CI/CD?