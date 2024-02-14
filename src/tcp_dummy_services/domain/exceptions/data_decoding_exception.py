from fastapi.responses import Response


class DataDecodingException(Exception):
    """Exception for json data decoding errors

    Args:
        Exception (Exception): inherits from base exception
    """

    def __init__(self, *args, response: Response = None):
        super().__init__(*args)
        self.response = response
