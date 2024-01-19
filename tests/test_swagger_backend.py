#
# not yet implemented do not use
#
import pytest
import yaml

from tools.swagger_backend import SwaggerAPI

test_swagger_yaml = '''   
openapi: 3.0.0
info:
  title: MoC API
  version: 1.0.0

paths:
  /user:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                email:
                  type: string
      responses:
        '200':
          description: User created successfully

  /project/{id}:
    get:
      summary: Get project details
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Project details retrieved successfully

  /projects:
    get:
      summary: Get a list of projects
      responses:
        '200':
          description: List of projects retrieved successfully  
'''



@pytest.fixture
def swagger_object():
    return SwaggerAPI(swagger_yaml=yaml.safe_load(test_swagger_yaml))
class TestSwaggerAPI:
    def test_all_endpoints(self, swagger_object):
        actual_result = swagger_object.all_endpoints()
        expected_result = ["/user", "/projects", "/project/{id}"]
        assert len(actual_result) == len(expected_result), f'Expected result is {expected_result}, but got {actual_result}'
        assert set(actual_result).issubset(expected_result), f'Expected result is {expected_result}, but got {actual_result}'

    def test_endpoint_search(self, swagger_object):
        test_query = '/project'
        actual_result = swagger_object.endpoint_search(test_query)
        expected_result = [ '/project/{id}', '/projects',]
        assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'

    def test_endpoint_search_unspecific(self, swagger_object):
        test_query = 'user'
        actual_result = swagger_object.endpoint_search(test_query)
        expected_result = ['/user']
        assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'

    def test_get_endpoint(self,swagger_object):
        test_endpoint = '/projects'
        actual_result = swagger_object.get_endpoint(test_endpoint)
        expected_result = \
            { "/projects":
                {"get":
                    {"summary": "Get a list of projects",
                        "responses":
                            {"200":
                                { "description": "List of projects retrieved successfully"}}}}}
        assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'