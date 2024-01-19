from prance import ResolvingParser
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class SwaggerAPI:
    api_path: str = ""
    swagger_yaml: str = ""
    spec: ResolvingParser = field(default_factory=dict, init=False)
    endpoints: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        if self.swagger_yaml != "":
            self.spec = ResolvingParser(spec_string=self.swagger_yaml, strict=False)

        elif self.api_path != "":
            self.spec = ResolvingParser(url=self.api_path, strict=False)
        else:
            raise ValueError("Either swagger_yaml or api_path must be provided")
        self.endpoints = self.spec.specification["paths"]

    def get_endpoint(self, path) -> Dict[str, Dict[any, any]]:
        """
        Get a specific endpoint from the swagger api
            will return the endpoint:
                /projects/{project_id}: {'get' ...}, {'post' ...}

        Args:
            path (str): Path to endpoint ie: '/projects/{project_id}'

        Returns:
            dict: Endpoint as dict
        """
        return {path: self.endpoints.get(path)}

        #return {self.endpoints[path].keys()
                #: self.endpoints[path]}#: self.endpoints[path].values()}

    def endpoint_search(self, query) -> List[str]:
        """
        Search for endpoints by path
            will return all endpoints that start with the query for example:
                project will return the endpoints:
                    /projects, 
                    /project/{project_id} , 
                    /project/{project_id}/users 
                    ...
        Args:
            query (str): Search query 
        Returns:
            list: List of endpoints as dicts
        """
        if not query.startswith("/"):
            query = "/" + query
        return [endpoint for endpoint in self.endpoints.keys() if endpoint.startswith(query)]

    def all_endpoints(self) -> List[str]:
        """
        Get a list all endpoints from the swagger api
            will return all endpoints:
                /aaaa
                /bbbb
                ...
                /zzzz

        Returns:
            list: List of endpoints as strings
        """
        return [endpoint for endpoint in self.endpoints]