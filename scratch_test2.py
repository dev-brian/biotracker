import urllib.request
content = urllib.request.urlopen("http://localhost:8501").read().decode('utf-8')
print("stSidebar" in content)
