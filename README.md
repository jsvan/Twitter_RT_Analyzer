# Twitter_Stream_2_SQLite

This is a simple tool to stream Twitter feeds into your sqlite database, built on python3. It runs from command line, and has a twitter schema premade which captures most information in tweets. 
Edit the follow_ids.json to dictate which accounts to follow. Creds are in twitter_cred.json.

follow_ids.json should maintain json styling ({"":"","":""}, etc. For each tuple, the first position is a human readable name just for us, and the second is twitter's numeric ID for that account. You can use https://tweeterid.com/ for example to find the correct id which Twitter will understand.

1. Git clone the project
2. Edit createCredentials.py, then run "python3 createCredentials.py"
3. Edit follow_id.json to include who you want to follow
4. Run "python3 -i main.py"
5. Available commands are printed to screen.


Im working on beefing up the built in sql queries to be usable to non tech people, so let me know if there's any functionality you'd like.



Commands:

* reader.run(growRTs=False) 					
  * runs the twitter collection. Edit follow_ids.json to choose who to follow.				
  * Optional parameter growRTs, if True, will expand on the list of who it follows to include retweeters of the initial accounts. 
  
* reader.query( "SQL_QUERY", slow=False). 	
  * Set the optional parameter slow to True for the output to be line by line, rather than a dump.

* reader.tables() 				
  * gives you the tables

* reader.help() 				
  * to see this menu again

* \<ctrl\>+c 					
  * terminates .run() and .query()

* exit() 					
  * terminates this program
