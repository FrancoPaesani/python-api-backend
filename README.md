## Oncology Registry Backend

This backend belongs to a patient registry system for the oncology infirmary service. 

The principal responsability of this API is to register the vital signs of the patient in order to analyze them and inform if some value is out of range. This is achieved in order to make give special care and atention to the patient with a minimum response time. 

## Technologies
- Alembic.
- Faker.
- FastAPI.
- Pydantic.
- Pytest
- SQLAlchemy.
- Uvicorn.

## Architecture
This API is developed under a 4 layer architecture:
- Route: The presentation layer.
- Service: The application layer. 
- Domain: Here is defined the bussiness validations.
- Persistence: Wich has the models with the tables definition and repositories that query the DB.

## ER Diagram
![Entity Relationship Diagram](er.png)

## Integrations
![Metrics Integration](metrics_integration.png)

![Logs Integration](logs_integration.png)

## Technical Features: 
1. Lock the application dependencies (e.g., pipenv, poetry, pdm). ✅
2. Add testing with Pytest: ✅
    - a. Add unit tests, leveraging fixtures, mocks, and patches
    - b. Add integration tests by using a TestClient
    - c. Add tests with the database by leveraging Fakes
3. Use dependency injection to deal with external systems like the DB. ✅
4. Use the repository pattern with Generics to manage queries to the database. ✅
5. Separate Database entities from Domain entities by leveraging Domain Driven Design. ✅
6. Add quality gates using pre-commits to the codebase: 
    - a. Formatting and Linting with Ruff ✅
    - b. Linting with Pylint 
    - c. Type checking with Mypy ✅
7. Make a docker container to easily deploy the application ✅
8. Protect the service by using Authentication and Authorization ✅
9. Make the HTTP API RESTFUL following Richardson levels: ✅
    - a. Use HTTP Resources 
    - b. Use HTTP Verbs 
    - c. Implement HATEOAS
10. Use a database migration tool (e.g Alembic) ✅
11. Enhance the retrieve endpoints by adding the possibility to filter records by attributes. ✅