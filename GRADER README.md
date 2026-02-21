# Student notes to grader

- Running on port 8000 due to conflict on dev laptop
- Notice that I have included integration tests: /tests/test_integration.py. They are used to test the integration between the order tracker and the in memory storage. Not that in memory storage would be sufficient for production environment; rather, I want to test the interface between the two and have a solid contract, before I would choose a proper solution. This way, tests are less of a rewrite and more of a safety net.
- You are going to see some duplicated code in my tests. I generally prefer to have more of the setup in each test than less. This reduces the scrolling burden as well as the debug burden months from now when I have to return to test.