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

from typing import List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text, Float, Index
from sqlalchemy.orm import relationship, Mapped
import uuid
from sqlalchemy.dialects.sqlite import TEXT


class Patient(SQLModel, table=True):
    patient_id: str = Field(
        sa_column=Column(
            TEXT, unique=True, primary_key=True, default=str(uuid.uuid4())
        ),
        allow_mutation=False,
    )
    queries: Mapped[List["Query"]] = Relationship(
        # back_populates="patient",
        passive_deletes="all",
        cascade_delete=True,
        sa_relationship=relationship(back_populates="patient"),
    )


class Query(SQLModel, table=True):
    """Every Query must have both a Patient and a Location."""

    query_id: str = Field(
        sa_column=Column(
            TEXT, unique=True, primary_key=True, default=str(uuid.uuid4())
        ),
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
        sa_column=Column(
            TEXT, unique=True, primary_key=True, default=str(uuid.uuid4())
        ),
        allow_mutation=False,
    )
    latitude: float = Field(sa_column=Column(Float))
    longitude: float = Field(sa_column=Column(Float))
    queries: Mapped[List["Query"]] = Relationship(
        # back_populates="location",
        cascade_delete=True,
        passive_deletes=True,
        sa_relationship=relationship(back_populates="location"),
    )


# TODO: Define Provider SQL model fields
# class Provider(SQLModel, table=True):
#     # TODO: Compare with Github issue, domain model and noccodb
#     ...


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
