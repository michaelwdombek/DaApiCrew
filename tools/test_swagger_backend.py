#
# not yet implemented do not use
#

from swagger_backend import SwaggerAPI

test_swagger_yaml = '''   
swagger: '2.0'            
info:                     
  title: Mock API         
  version: '1.0'          
schemes:                  
  - http
paths:                    
  /users:      
    get: "MOCK"       
  /projects:     
    get: "MOCK"       
  /project/{project_id}:                
    get: "MOCK"                  
'''

class TestSwaggerAPI:
  #@pytest.fixture
  def instance(self):
    return SwaggerAPI(api_path="./api.yaml")

  def test_all_endpoints(self):                                                                                
      actual_result = self.instance().all_endpoints()
      expected_result = ["/users", "/projects", "/project/{project_id}"]
      assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'

  def test_endpoint_search(self):                                                                              
      test_query = '/project'
      actual_result = self.instance.endpoint_search(test_query)                                                
      expected_result = ['/projects','/project/{project_id}']
      assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'

  def test_endpoint_search_unspecific(self):      
      test_query = 'user'
      actual_result = self.instance().endpoint_search(test_query)                                                
      expected_result = ['/users']
      assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'

  def test_get_endpoint(self):                                                                                 
      test_endpoint = '/users'
      actual_result = self.instance().get_endpoint(test_endpoint)                                                
      expected_result = {'/user': {'get': 'MOCK'}}
      assert actual_result == expected_result, f'Expected result is {expected_result}, but got {actual_result}'
