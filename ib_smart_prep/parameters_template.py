# This file has to be renamed to parameters.py for the run_all script to work, this is only a template.

# Place the auth token from ib smart prep here
# It can be found by loading a flashcard and checking the requests labeled "answer" or "content" in the network tab of Chrome's debugger
# The string you're looking for is "BEARER <auth_token>"
auth_token = "AUTH TOKEN HERE"

# The number of parallel connections to download cards and media that are allowed
# More than 100 has previously resultet in Nginx giving back 401 (bad gateway) on their part
num_concurrent_connections = 100
