import os
import sys

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app

app.app.testing = True
client = app.app.test_client()

# Mock session
with client.session_transaction() as sess:
    sess["user_id"] = 1

response = client.get("/forecast-dashboard")
html = response.get_data(as_text=True)

print("Status:", response.status_code)
print("Length of HTML:", len(html))
print("Contains navbar.html text:", "Groundwater Monitor" in html)
print("Contains '<nav':", "<nav" in html)

# Let's inspect where navbar is positioned in HTML
idx = html.find("Groundwater Monitor")
if idx != -1:
    print("Snippet around Brand logo:")
    print(html[idx-100:idx+200])
else:
    print("Brand logo NOT found in HTML!")
