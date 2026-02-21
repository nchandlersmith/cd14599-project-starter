# Notes to grader

- Running on port 8000 due to conflict on dev laptop
- Added unit tests /tests/test_integration.py. I needed confidence in that integration.
- Added sad path tests in the api to cover the error handling
- Not returning a 404 unless it blocked an action, i.e. update order
- Next steps
  - Persistent storage -- productionize early
  - Refactor the validations in the order tacker. By creating a validator class that output a ValidatedOrder. This would:
    - Centralize the field validation logic
    - DRY it out
    - Slim down the service logic
  - Then do delete, given the pattern has emerged and I want to test that hyp0thesis on the design.

# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```
