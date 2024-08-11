from config import crop_begin_date, config
import traceback

from pathlib import PurePath, Path
import time
import sys
from datetime import datetime, timedelta

sys.path.append('./')
from a_util.service.letsgrow_service import LetsgrowService

def per_5min() -> None:
    lservice = LetsgrowService()
    
    from_date = lservice.get_latest_date()
    # from_date = datetime(2024,8,8,0,0,0)
    lservice.letsgrow_to_db_day(from_date)
    
if __name__ == "__main__":
    per_5min()