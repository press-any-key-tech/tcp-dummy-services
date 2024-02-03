from typing import Optional

from pydantic import BaseModel, Field, field_validator, validator


class Thing(BaseModel):
    """
    Represents a data structure for a Thing.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Thing ID",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: str = Field(
        ...,
        max_length=150,
        json_schema_extra={"description": "Thing name", "example": "A thing"},
    )

    location: Optional[str] = Field(
        default=None,
        max_length=150,
        json_schema_extra={"description": "Thing location", "example": "Somewhere"},
    )
