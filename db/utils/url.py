from sqlalchemy.engine import URL
import settings


def get_url(drive_name: str):
    return URL.create(
        drivername=drive_name,
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        database=settings.DB_NAME,
        port=settings.DB_PORT
    )
