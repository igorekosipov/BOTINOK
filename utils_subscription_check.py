from datetime import datetime
from database import get_user

async def check_subscription(user_id: int) -> bool:
    user = await get_user(user_id)
    if not user or not user["subscription_end"]:
        return False
    try:
        end_date = datetime.fromisoformat(user["subscription_end"])
        return end_date > datetime.now()
    except:
        return False
