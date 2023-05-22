3. init_db.sh script from qs_prod (Rust QuickStart)
    - Adapt init_db.sh to Python/Alembic
    - How do we create the DB Schema programmatically with Alembic?
    - Fix FK Constraints on the alembic revision
    - Add indices and confirm unique constraints in the alembic revision
    
    - Create models/schemas
    - Pre-populate some data
    - Test downgrade
    - Establish DB Connection code for the application itself (https://testdriven.io/blog/fastapi-sqlmodel/)

4. Write the daily and onboard processes for the scheduler
5. Fix tests
6. Write Relays, Relay Configs, Job Config, Filter Config, Subscription Record Database
