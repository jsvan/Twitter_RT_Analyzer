# Twitter_RT_Analyzer
 Working project, run from command line, adds twitter feeds to a db and allows sql queries on it. 
Edit the follow_ids.json to dictate which accounts to follow. Creds are in twitter_cred.json.

follow_ids.json should maintain json styling ({"":"","":""}, etc. For each tuple, the first position is a human readable name just for us, and the second is twitter's numeric ID for that account. You can use https://tweeterid.com/ for example to find the correct id which Twitter will understand.

Git clone the project,
Run "python3 createCredentials.py"
Run "python3 -i main.py"
Available commands are printed to screen.
