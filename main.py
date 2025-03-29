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


A = datetime.strptime("05:00:00", "%H:%M:%S").time()
B = datetime.strptime("18:00:00", "%H:%M:%S").time()

print(datetime.now(pytz.timezone("Europe/Moscow")).time().minute)
print((datetime.now().time() >= A)
      & (B > datetime.now(pytz.timezone("Europe/Moscow")).time()))
print(A.hour)