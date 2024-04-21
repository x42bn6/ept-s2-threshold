# ept-s2-threshold
A Python script that tries to find the threshold to qualify to Riyadh Masters 2024, for the ESL Pro Tour (EPT).

Most of the credit for this goes to "tkunt", who wrote [this article](https://tkunt.medium.com/computing-bounds-for-ranks-and-ti-qualification-of-the-dpc-2023-tour-3-870957df4ec5) for the Dota Pro Circuit.  I merely adopted it for the ESL Pro Tour.

The output of this is the threshold table in MediaWiki format, to be output [here](https://liquipedia.net/dota2/ESL_Pro_Tour/Leaderboard/Season_2_threshold_explanation#What_does_the_threshold_scenario_look_like?).

## Disclaimers

- I am not a Python developer
- I have limited experience with optimisation
  - I do have some form of a mathematics background, so I know some things, but optimisation on this level is beyond what I was taught

# Running the script
1. [Install Python.](https://www.python.org/downloads/)  I used Python 3.12.2 on Windows.  Any reasonable version should do.
2. [Install pip.](https://pip.pypa.io/en/stable/cli/pip_install/)  I used pip 24.0.  Any reasonable version should do.
3. (Optional) [Install Jupyter.](https://jupyter.org/install)  At work, my team uses Jupyter, so I'm a bit more familiar with it.  However, any IDE will do, or you can execute scripts manually using Python.
4. Download [the script.](https://github.com/x42bn6/ept-s2-threshold/blob/main/ept-s2.py)
5. Run it.

The output is a bunch of debugging statements, reflecting the threshold being computed for each team.  If a team cannot reach this maximum anyway, it is skipped.  At the very end, a table in MediaWiki format is output; this is the section [here.](https://liquipedia.net/dota2/ESL_Pro_Tour/Leaderboard/Season_2_threshold_explanation#What_does_the_threshold_scenario_look_like?)  The threshold is in this section: As of time of writing, this is:

    This is the following scenario where {{Team|Team Falcons}} fail to qualify with 9120 points.

This means that the threshold, to put on [the leaderboard](https://liquipedia.net/dota2/ESL_Pro_Tour/Leaderboard), is &geq; 9120 (i.e. 9121).

# Updating results
TBA
