# Test task for Trood

[![](https://travis-ci.org/osminogin/trood_test_task.svg?branch=master)](https://travis-ci.org/osminogin/trood_test_task)

## Features

* Python 3.7 and 3.6 Support.
* Uses asynchronous workers for non-blocking IO.
* Automatically generated OpenAPI specs and documentation.
* Full test coverage.
* Load tests with Locust.
* Continuous Integration with Travis CI.
* With internationalization in mind.

## How to check

```bash
make run    # Start gunicorn or django dev server
make locust # Open http://localhost:8089 and start Locust
make check  # Returns current active uploads from API
```

## Author

Vladimir Osintsev <oc@co.ru>
