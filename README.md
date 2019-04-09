# Twitter_RT_Analyzer

This is a simple tool to stream Twitter feeds into your sqlite database, built on python3. It runs from command line, and has a twitter schema premade which captures most information in tweets. 
Edit the follow_ids.json to dictate which accounts to follow. Creds are in twitter_cred.json.

follow_ids.json should maintain json styling ({"":"","":""}, etc. For each tuple, the first position is a human readable name just for us, and the second is twitter's numeric ID for that account. You can use https://tweeterid.com/ for example to find the correct id which Twitter will understand.

Git clone the project,
Run "python3 createCredentials.py"
Run "python3 -i main.py"
Available commands are printed to screen.


Im working on beefing up the built in sql queries to be usable to non tech people, so let me know if there's any functionality you'd like.
