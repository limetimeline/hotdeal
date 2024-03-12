from datetime import datetime

now = datetime.now()
date = datetime.strptime('2024-03-04 17:22:56', '%Y-%m-%d %H:%M:%S')

print((now - date).days)