import datetime

from datetime import datetime, timezone
import pytz
from werkzeug.security import generate_password_hash

# url = "http://userapi/users/" + str('12323'),
# print(url)

#
# a = [1, 2, 3, 4]
#
#
# for i in a:
#     if i % 2 == 0:
#         continue
#     print(i)


A = datetime.strptime("2025-03-30", "%Y-%m-%d")
B = datetime.strptime("2025-03-30", "%Y-%m-%d")

A1 = datetime.strptime("2025-03-30", "%Y-%m-%d")
B2 = datetime.strptime("2025-03-30", "%Y-%m-%d")

print((A <= A1) & (B2 <= B))
