from config import crop_begin_date, config
import traceback
import pytz

from pathlib import PurePath, Path
import time
import sys
from datetime import datetime, timedelta

sys.path.append('./')
from a_util.service.letsgrow_service import LetsgrowService

def per_5min() -> None:
    lservice = LetsgrowService()
    
    from_date = lservice.get_latest_date()
    print("############################ DB last element day : ", from_date)
    print("############################ excution_time : ", datetime.now(pytz.timezone('Europe/Amsterdam')).replace(tzinfo=None))    
    # from_date = datetime(2024,9,1,0,0,0)
    lservice.letsgrow_to_db_day(from_date.replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(days=1)) 
    lservice.letsgrow_to_db_day(from_date.replace(hour=0, minute=0, second=0, microsecond=0)) 
    lservice.letsgrow_to_db_day(from_date)    
    
    print("per_5min run successfully") 
    
if __name__ == "__main__":
    per_5min()