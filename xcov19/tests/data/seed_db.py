"""Dummy data to seed to database models.
Mapped to SQLModel.
"""

from sqlalchemy import ScalarResult
from sqlmodel import select
from xcov19.infra.models import Patient, Query, Location
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSessionWrapper


async def seed_data(session: AsyncSessionWrapper):
    """Seeds database with initial data.

    dummy GeoLocation:
    lat=0
    lng=0

    cust_id=test_cust_id
    query_id=test_query_id

    Now you can do:
    res = await self._session.exec(select(Query))
    query = res.first()
    print("query", query)
    res = await self._session.exec(select(Patient).where(Patient.queries.any(Query.query_id == query.query_id)))
    print("patient", res.first())
    res = await self._session.exec(select(Location).where(Location.queries.any(Query.query_id == query.query_id)))
    print("location", res.first())
    """
    query = Query(
        query="""
        Runny nose and high fever suddenly lasting for few hours.
        Started yesterday.
        """
    )  # type: ignore

    patient = Patient(queries=[query])  # type: ignore

    patient_location = Location(latitude=0, longitude=0, queries=[query])  # type: ignore
    session.add_all([patient_location, patient])
    await session.commit()
    query_result: ScalarResult = await session.exec(select(Query))
    if not query_result.first():
        raise RuntimeError("Database seeding failed")
