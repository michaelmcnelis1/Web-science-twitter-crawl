# Web-science-twitter-crawl

Fetching the tweets:

To fetch tweets, run the file "web_twitter_crawl.py".
This creates a file called "all_data.csv" containing all the tweets fetched.
It should be noted that this code took approximately 2 hours to run when collecting the data. To reduce this runtime, less tweets could be fetched. This can be achieved by editing the end of lines 50 and 77 to read .items(100) instead of .items(1500).


Processing the tweets:

To clean the data, run the file "web_process_data.py".
It should be noted that the file "all_data.csv" must be saved in the appropriate directory first.
This will lead to the creatation of the final six csv files containing the clean data for each emotion.
