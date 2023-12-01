import ast
from typing import Any, ClassVar, Optional
from fastapi import HTTPException

from langflow.utils import validate
from langflow.interface.custom.code_parser import CodeParser


class ComponentCodeNullError(HTTPException):
    pass


class ComponentFunctionEntrypointNameNullError(HTTPException):
    pass


class Component:
    ERROR_CODE_NULL: ClassVar[str] = "Python code must be provided."
    ERROR_FUNCTION_ENTRYPOINT_NAME_NULL: ClassVar[
        str
    ] = "The name of the entrypoint function must be provided."

    code: Optional[str] = None
    _function_entrypoint_name: str = "build"
    field_config: dict = {}

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

    def get_code_tree(self, code: str):
        parser = CodeParser(code)
        return parser.parse_code()

    def get_function(self):
        if not self.code:
            raise ComponentCodeNullError(
                status_code=400,
                detail={"error": self.ERROR_CODE_NULL, "traceback": ""},
            )

        if not self._function_entrypoint_name:
            raise ComponentFunctionEntrypointNameNullError(
                status_code=400,
                detail={
                    "error": self.ERROR_FUNCTION_ENTRYPOINT_NAME_NULL,
                    "traceback": "",
                },
            )

        return validate.create_function(self.code, self._function_entrypoint_name)

    def build_template_config(self, attributes) -> dict:
        template_config = {}

        for item in attributes:
            item_name = item.get("name")

            if item_value := item.get("value"):
                if "display_name" in item_name:
                    template_config["display_name"] = ast.literal_eval(item_value)

                elif "description" in item_name:
                    template_config["description"] = ast.literal_eval(item_value)

                elif "beta" in item_name:
                    template_config["beta"] = ast.literal_eval(item_value)

                elif "documentation" in item_name:
                    template_config["documentation"] = ast.literal_eval(item_value)

        return template_config

    def build(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
