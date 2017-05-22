# seriesDownloader

---

The purpose of the program is to download series from the following sites:
- tv2.hu
- supertv2.hu

# Usage

Run the main.py file then enter the requested information according to the program prompts.

### Select bitrate
From the list that appears, select the desired bitrate and type it.
Example: 360

If the specified resolution does not exist for the selected episode, the program will select the next one with a lower resolution.
If you want to download the best quality, select the highest resolution from the list.


### Select host
From the list that appears, select the host you would like to download the episode(s). (by typing in the host's ID)

       0       http://tv2.hu
       1       http://supertv2.hu
For example, if you choose http://tv2.hu then: 0

### Search series
Enter a keyword (at least 3 characters) of the name of the series you're looking for.
For example, if you'd like to find a series called "Jóban Rosszban", type: jób

Based on the keyword, the program will list the results with the series' ID and name.

       0       Jóban rosszban
In this example there is only one result, just what I was looking for: 0

No matching result will be indicated by the program, you should try another host.

### Enter episodes to download

There are three ways to specify the series to download:
- Just give an episode
Example: 2448
- Enter interval with hyphen
Example: 5-31
- Enter multiple episode numbers comma separated
Example: 5, 12, 54

### Download starts
More detailed errors and information can be viewed in the log/info.log file

### Example
[![asciicast](https://asciinema.org/a/2lt45as46y0nd26qxo4z9cdg6.png)](https://asciinema.org/a/2lt45as46y0nd26qxo4z9cdg6)