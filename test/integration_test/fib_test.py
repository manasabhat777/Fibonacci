import sys
import os

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../src')))

from generate_fib_controller import app
import json

class TestFib():

  def test_valid_fib_generation(self):
    tester = app.test_client(self)
    response = tester.get('/fib/2/5', content_type='application/json')
    assert response.status_code == 201, 'but received %s' \
            % response.status_code
    assert json.loads(response.data) == {"fibonacci_numbers": [2, 3, 5]}, 'but received %s' % json.loads(response.data)

  def test_fib_with_negative(self):
    tester = app.test_client(self)
    response = tester.get('/fib/-2/5', content_type='application/json')
    assert response.status_code == 500, 'but received %s' \
            % response.status_code

  def test_fib_with_equal_values(self):
    tester = app.test_client(self)
    response = tester.get('/fib/2/2', content_type='application/json')
    assert response.status_code == 500, 'but received %s' \
            % response.status_code

  def test_fib_with_start_idx_greater_than_end_idx(self):
    tester = app.test_client(self)
    response = tester.get('/fib/20/2', content_type='application/json')
    assert response.status_code == 500, 'but received %s' \
            % response.status_code
  
