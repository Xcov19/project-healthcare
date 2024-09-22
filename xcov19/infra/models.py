"""
Database Models and Delete Behavior Design Principles

1. Query-Patient-Location Relationship:
   - Every Query must have both a Patient and a Location associated with it.
   - A Patient can have multiple Queries.
   - A Location can be associated with multiple Queries.

2. Delete Restrictions:
   - Patient and Location records cannot be deleted if there are any Queries referencing them.
   - This is enforced by the "RESTRICT" ondelete option in the Query model's foreign keys.

3. Orphan Deletion:
   - A Patient or Location should be deleted only when there are no more Queries referencing it.
   - This is handled by custom event listeners that check for remaining Queries after a Query deletion.

4. Cascading Behavior:
   - There is no automatic cascading delete from Patient or Location to Query.
   - Queries must be explicitly deleted before their associated Patient or Location can be removed.

5. Transaction Handling:
   - Delete operations and subsequent orphan checks should occur within the same transaction.
   - Event listeners use the existing database connection to ensure consistency with the main transaction.

6. Error Handling:
   - Errors during the orphan deletion process should not silently fail.
   - Exceptions in event listeners are logged and re-raised to ensure proper transaction rollback.

7. Data Integrity:
   - Database-level constraints (foreign keys, unique constraints) are used in conjunction with SQLAlchemy model definitions to ensure data integrity.

These principles aim to maintain referential integrity while allowing for the cleanup of orphaned Patient and Location records when appropriate.
"""

from __future__ import annotations

import json
from typing import Annotated, Dict, List, Tuple, Any
from pydantic import GetCoreSchemaHandler, TypeAdapter
from pydantic_core import CoreSchema, core_schema
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.type_api import _BindProcessorType
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import BindParameter, Column, Dialect, Text, Float, Index, func
from sqlalchemy.orm import relationship, Mapped
import uuid
from sqlalchemy.dialects.sqlite import TEXT, NUMERIC, JSON, INTEGER
from sqlalchemy.types import UserDefinedType


class PointType(UserDefinedType):
    """Defines a geopoint type.

    It also sets the type as a pydantic type when plugged into TypeAdapter.
    """

    def get_col_spec(self):
        return "POINT"

    def result_processor(self, dialect: Dialect, coltype: Any) -> Any | None:
        def process(value):
            if not value:
                return None
            parsed_value = value[6:-1].split()
            return tuple(map(float, parsed_value))

        return process

    def bind_processor(self, dialect: Dialect) -> _BindProcessorType | None:
        def process(value):
            if not value:
                return None
            lat, lng = value
            return f"POINT({lat} {lng})"

        return process

    def bind_expression(self, bindvalue: BindParameter) -> ColumnElement | None:
        return func.GeomFromText(bindvalue, type_=self)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Tuple, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Pydantic validates the data as a tuple."""
        return core_schema.no_info_after_validator_function(cls, handler(tuple))

    @classmethod
    def pydantic_adapter(cls) -> TypeAdapter:
        return TypeAdapter(cls)


def generate_uuid() -> str:
    return str(uuid.uuid4())


### These tables map to the domain models for Patient
class Patient(SQLModel, table=True):
    patient_id: str = Field(
        sa_column=Column(TEXT, unique=True, primary_key=True, default=generate_uuid),
        allow_mutation=False,
    )
    queries: Mapped[List["Query"]] = Relationship(
        passive_deletes="all",
        cascade_delete=True,
        sa_relationship=relationship(back_populates="patient"),
    )


class Query(SQLModel, table=True):
    """Every Query must have both a Patient and a Location."""

    query_id: str = Field(
        sa_column=Column(TEXT, unique=True, primary_key=True, default=generate_uuid),
        allow_mutation=False,
    )
    query: str = Field(allow_mutation=False, sa_column=Column(Text))
    # Restrict deleting Patient record when there is atleast 1 query referencing it
    patient_id: str = Field(foreign_key="patient.patient_id", ondelete="RESTRICT")
    # Restrict deleting Location record when there is atleast 1 query referencing it
    location_id: str = Field(foreign_key="location.location_id", ondelete="RESTRICT")
    location: Location = Relationship(back_populates="queries")
    patient: Patient = Relationship(back_populates="queries")


class Location(SQLModel, table=True):
    __table_args__ = (
        Index("ix_location_composite_lat_lng", "latitude", "longitude", unique=True),
    )
    location_id: str = Field(
        sa_column=Column(TEXT, unique=True, primary_key=True, default=generate_uuid),
        allow_mutation=False,
    )
    latitude: float = Field(sa_column=Column(Float))
    longitude: float = Field(sa_column=Column(Float))
    queries: Mapped[List["Query"]] = Relationship(
        cascade_delete=True,
        passive_deletes=True,
        sa_relationship=relationship(back_populates="location"),
    )


###


### These tables map to the domain models for Provider
class Provider(SQLModel, table=True):
    provider_id: str = Field(
        sa_column=Column(TEXT, unique=True, primary_key=True, default=generate_uuid),
        allow_mutation=False,
    )
    name: str = Field(
        sa_column=Column(TEXT, nullable=False),
    )
    address: str = Field(sa_column=Column(TEXT, nullable=False), allow_mutation=False)
    geopoint: Annotated[
        tuple, lambda geom: PointType.pydantic_adapter().validate_python(geom)
    ] = Field(sa_column=Column(PointType, nullable=False), allow_mutation=False)
    contact: int = Field(sa_column=Column(NUMERIC, nullable=False))
    facility_type: str = Field(sa_column=Column(TEXT, nullable=False))
    ownership_type: str = Field(sa_column=Column(TEXT, nullable=False))
    specialties: List[str] = Field(sa_column=Column(JSON, nullable=False))
    stars: int = Field(sa_column=Column(INTEGER, nullable=False, default=0))
    reviews: int = Field(sa_column=Column(INTEGER, nullable=False, default=0))
    available_doctors: List[Dict[str, str | int | float | list]] = Field(
        sa_column=Column(JSON, nullable=False, default=json.dumps([]))
    )


###

# TODO: Add Model events for database ops during testing
# @event.listens_for(Query, "after_delete")
# def delete_dangling_location(mapper: Mapper, connection: Engine, target: Query):
#     """Deletes orphan Location when no related queries exist."""
#     local_session = sessionmaker(connection)
#     with local_session() as session:
#         stmt = (
#             select(func.count())
#             .select_from(Query)
#             .where(Query.location_id == target.location_id)
#         )
#         if (
#             num_queries := session.execute(stmt).scalar_one_or_none()
#         ) and num_queries <= 1:
#             location: Location = session.get(Location, target.location_id)
#             session.delete(location)
#         session.flush()


# @event.listens_for(Query, "after_delete")
# def delete_dangling_patient(mapper: Mapper, connection: Engine, target: Query):
#     """Deletes orphan Patient records when no related queries exist."""
#     local_session = sessionmaker(connection)
#     with local_session() as session:
#         stmt = (
#             select(func.count())
#             .select_from(Query)
#             .where(Query.patient_id == target.patient_id)
#         )
#         if (
#             num_queries := session.execute(stmt).scalar_one_or_none()
#         ) and num_queries <= 1:
#             patient: Patient = session.get(Patient, target.patient_id)
#             session.delete(patient)
#         session.flush()
