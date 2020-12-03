#Fantasy Football Reality 2020
Compare weekly projected fantasy rankings (by ESPN analysts) of NFL skill-position players with actual performance.

## Setup Instructions
This project is made using Python 3.7.9, so if this version (or at least 3.7+) isn't installed on your file system, visit [python.org](https://www.python.org/downloads/release/python-379/) and follow the instructions to download and install python (as well as its package manager, pip).

After you clone this project to your desktop, you will need to install the requisite libraries (including flask, pandas, et al.). Open a terminal window, navigate to the root project directory, and execute the following command:

`pip install -r requirements.txt`
or
`pip3 install -r requirements.txt`
(depending on how your python versions are mapped to commands)

After all libraries have successfully installed, you're ready to run the app on a local flask server. While still in the root project directory, execute the following command in the terminal window:

`python main.py`
or
`python3 main.py`
(depending on how your python versions are mapped to commands)

Then open [http://localhost:5000](http://localhost:5000) to view it in the browser.

## Usage
The user interface has selection options for week (of the NFL season), position (QB, RB, WR, TE), and analyst ('All', or one of any individual ESPN fantasy analyst). After making selections through the dropdown menus, press the 'Show Tables' button.

Note: Weeks 1-16 appear in the dropdown menu, but only weeks that have completed will successfully return comparison tables.

For a spotlight on how well a particular analyst projected the player rankings:
Select an individual analyst's name, and you will see a single table that displays the rankings of players at the position selected, as projected by the analyst (along with the consensus of analysts) and as they actually performed during that week's games. Other columns show the fantasy points scored (+1 PPR rules) by each player and how different each projected ranking was from the result.

For a side-by-side comparison of all analysts' projection accuracy:

Select 'All', and three tables will appear: Expert Projected Rankings, Actual Results & Difference from Experts' Projections, and Standard Deviation of Differences. The sample standard deviation for each analyst is calculated from the difference between the projected and resulting ranking for each player.

## Credits
Data for projected rankings by ESPN analysts is provided by ESPN: https://fantasy.espn.com/football/tools/fantasyRankings

Data for actual player rankings is provided by FantasyPros: https://www.fantasypros.com/nfl/reports/leaders
