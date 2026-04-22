import sys
import asyncio

# Fix for Python 3.14 compatibility with Streamlit
# In Python 3.14, asyncio.get_event_loop() raises RuntimeError if there's no loop.
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from streamlit.web import cli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(cli.main())
