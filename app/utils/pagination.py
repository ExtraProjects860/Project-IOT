from app import models
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def paginationData(session: AsyncSession, model: models.BaseModel, page: int = 1, quantity_records: int = 50) -> dict:
    count_result = await session.execute(select(func.count(model.id)))
    total_records: int = count_result.scalar_one()

    pagination_query = (
        select(models.TemperatureIncident)
        .order_by(models.TemperatureIncident.created_at.desc())
        .offset((page - 1) * quantity_records)
        .limit(quantity_records)
    )

    result = await session.execute(pagination_query)
    records = result.scalars().all()

    total_pages: int = (total_records + quantity_records -
                        1) // quantity_records

    return { "records": [record.to_dict() for record in records], "total_pages": total_pages, "page": page }
