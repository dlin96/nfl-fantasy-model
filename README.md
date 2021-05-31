[![Build Status](https://travis-ci.com/dlin96/nfl-fantasy-model.svg?branch=master)](https://travis-ci.com/dlin96/nfl-fantasy-model)

## Model

The model was created using nfldb, a currently unmaintained project by BurntSushi. This took NFL game data and put it into a Postgres database upon which much of the analysis is performed. 

Right now, if you take a look at the fantasy_points_model.ipynb Jupyter Notebook, you can see the output and steps I took to create this model. Since nfldb only contains data from 2009-2016 so far, I used the 09-15 data to predict who are the best players for 2016. These predictions are done for each of the offensive positions (QB, RB, WR, and TE). I sorted the output by the predicted values, and also used z-scores to determine which players at which position are standouts. For example, Jamaal Charles had a z-score of 2.99 in that time frame (obviously no longer the case for 2020), and would most likely be the best selection since there aren't many runningbacks that would give you the same production. 

## Depth-Chart and Schedules
I wrote scrapers using BeautifulSoup4 to get the depth-chart information and schedules from official team websites. This data is crucial for future predictions as the strengh-of-schedule is an often-cited metric (although the definition is still hotly contested) for projections of player performance. I.e. the teams that have a tougher schedule most likely will not perform as well. This is an oversimplification of the feature, since with fantasy sports the points are awarded on stats, not wins. For example, if Tom Brady has 154 passing yards and 1 TD and wins, but Patrick Mahomes has 550 yards and 4 TDs but loses, it would be preferable to have Patrick Mahomes. Where this fact conflicts with strength-of-schedule is if the increased competition will result in more playing time, and thus more opportunities to rack up stats. 

The depth-chart tells where each player stands in terms of their position. The higher up you are on this chart (represented by lower numbers e.g. first on the depth chart means you're starting), the more playing time you're likely to get, and thus more opportunities to perform.

## Future work

This model so far is more of a proof of concept for future seasons. Right now, future work is mostly to get the database up-to-date by updating and maintaining the nfldb package. I have already forked it and will begin work on it. 

After nfldb has been updated, the next step would be to add new features to improve the model. If you look at the bottom of the jupyter notebook, you can see a "Features for consideration" section for features I wish to add after nfldb has been updated.

The web client will be static. Previously, I had a feature that allowed comparison of two players, but I realized that the hosting of the Postgres db on AWS via RDS was too expensive. So for now the website will only contain predictions for players and possibly depth-chart/schedule information. These will be stored on Redis on a cloud provider (since this data is much smaller than the entire nfldb, it falls within the free tier for many providers). 

## Feedback

I welcome any feedback on how to make this any better, and if you made it this far through the README, thank you for your time!
