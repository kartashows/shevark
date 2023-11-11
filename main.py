import logging

from aiogram.utils import executor

from bot_logic.crm_bot import dp
from db.connection_pool import get_connection
import db.database as database


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Connecting to the db...")
        with get_connection() as connection:
            logger.info("No errors while connecting to the db!")
            database.create_tables(connection)
        logger.info("Starting SHEVARK bot...")
        executor.start_polling(dp, skip_updates=True)
    finally:
        logger.info("Stopping SHEVARK bot...")


if __name__ == '__main__':
    main()
