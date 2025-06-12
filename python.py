from datetime import datetime, UTC

timestamp = 1749679634
expiry_datetime = datetime.fromtimestamp(timestamp, UTC)
print(expiry_datetime)
