import sys
from pathlib import Path

assignment4 = Path(__file__).parent.parent.absolute()

# Ensure assignment4 dir is on sys.path
sys.path.insert(0, str(assignment4))


# Add custom markers, such that they appear in pytest --markers
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "task11: mark test to run only tests for task 1.1"
    )
    config.addinivalue_line(
        "markers", "task12: mark test to run only tests for task 1.2"
    )
    config.addinivalue_line(
        "markers", "task13: mark test to run only tests for task 1.3"
    )
    config.addinivalue_line("markers", "task2: mark test to run only tests for task 2")
    config.addinivalue_line(
        "markers", "task31: mark test to run only tests for task 3.1"
    )
    config.addinivalue_line(
        "markers", "task32: mark test to run only tests for task 3.2"
    )
    config.addinivalue_line(
        "markers", "task33: mark test to run only tests for task 3.3"
    )
    config.addinivalue_line("markers", "task41: mark test to run only tests for task 8")
    config.addinivalue_line("markers", "task42: mark test to run only tests for task 9")
    config.addinivalue_line(
        "markers", "task43: mark test to run only tests for task 10"
    )
    config.addinivalue_line(
        "markers", "task44: mark test to run only tests for task 4.4"
    )
