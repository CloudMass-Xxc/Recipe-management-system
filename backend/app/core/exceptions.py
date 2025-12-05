"""
自定义异常类定义
"""


class APIException(Exception):
    """
    API自定义异常类
    """
    def __init__(self, status_code: int, detail: str, error_type: str = "api_error"):
        self.status_code = status_code
        self.detail = detail
        self.error_type = error_type
        super().__init__(self.detail)
