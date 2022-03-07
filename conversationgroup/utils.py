from sqlalchemy import select


def get_single_field(db, field, field_value):
    return db.scalars(
        select(field).where(
            field==field_value
        )
    ).all()
