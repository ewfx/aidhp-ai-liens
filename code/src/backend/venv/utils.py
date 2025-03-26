from typing import List

# Clean user data before returning it
def clean_user_data(users: List[dict]):
    for user in users:
        user.pop("_id", None)  # Remove MongoDB object ID
    return users
