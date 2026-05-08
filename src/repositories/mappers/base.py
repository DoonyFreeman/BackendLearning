from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import Base


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[Base]
    schema: Type[SchemaType]  # type: ignore

    @classmethod
    def map_to_domain_entity(cls, data: Base | dict | Row | RowMapping) -> SchemaType:  # type: ignore
        return cls.schema.model_validate(data, from_attributes=True)  # type: ignore

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel) -> Base:  # type: ignore
        return cls.db_model(**data.model_dump())
