# seriesDownloader

---

The essence of the program is to download series from different pages. Actually:
- tv2.hu
- supertv2.hu

# Usage

Run the main.py file, and then enter the requested information according to the program prompts.

### Select bitrate
From the list that appears, select the desired bitrate and type it.
Example: 360

If the specified resolution does not exist for the selected episode, the program will select the next one with a lower resolution.
If you want to download the best quality, select the highest resolution from the list.


### Select host
From the list that appears, select the host you want and type the host ID.

       0       http://tv2.hu
       1       http://supertv2.hu
For example, you want to http://tv2.hu then: 0

### Search series
Enter a keyword (at least 3 characters) of the name of the series to be searched.
For example, I'd like to find a series called "Jóban Rosszban": jób

Based on the keyword, the program will list the results and enter the desired series ID.

       0       Jóban rosszban
Currently there is an option, just what I was looking for: 0

If no series is found, indicate the program, try another server.

### Enter episodes to download

There are three ways to specify the series to download:
- Just give an episode
Example: 2448
- Enter interval with hyphen
Example: 5-31
- Enter multiple sections comma separated
Example: 5, 12, 54

### Download starts
More detailed errors and information can be viewed in the log/info.log file

### Example
https://asciinema.org/a/ejxxi181ge4lmyzdfxn9vthk2