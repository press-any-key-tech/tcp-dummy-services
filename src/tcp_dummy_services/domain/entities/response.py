from typing import Optional

from pydantic import BaseModel, Field, field_validator, validator


class Response(BaseModel):
    """
    Represents a data structure for a websockets response.
    """

    status: int = Field(
        ...,
        json_schema_extra={"description": "Call status response", "example": "200"},
    )

    message: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Response message", "example": "OK"},
    )
