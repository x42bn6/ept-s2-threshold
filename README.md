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

# Updating the script for results
I have created a new section in the script for ESL One Birmingham [here](https://github.com/x42bn6/ept-s2-threshold/blob/4162ca581a4333fae3d413b11ab3276fcb1c58e5/ept-s2.py#L348).  There is one section per team, for convenience.  This is because I envisage the following:

- As the tournament progresses, some teams will qualify to the next stage, progress to the top 6, then top 4, etc.  This means that they start to be unable to finish in lower positions.  So before a team has a final placement, we must eliminate all the positions below it.
- Once a team has a final placement, however, it can be replaced entirely by a single "this team finished here" constraint.

Thus to begin with, we must add statement like the following:

    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 11)
    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 12)

In this example, this states that BetBoom Team cannot finish last in their group.  Then, say, BetBoom Team accumulate enough wins to avoid elimination.  Their constraints would look like:

    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 9)
    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 10)
    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 11)
    team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 12)

This will become a long list.  However, say BetBoom Team finish 3rd.  All of these constraints can be replaced by:

    team_finished(x_birmingham, 'BetBoom Team', 3)

Which is much tidier.

In practical terms, I'm not expecting most of the first set of constraints to change much anyway, at least not until the latter phases of the tournament.

# Things to beware:
- On Liquipedia, the "G2.iG" team template redirects to "G2 x iG".  The script still uses "G2.iG" all over.  Use this.
- For shared positions, that grant the same EPT points, arbitrarily choose one team for one, and the other for the other.  For example, if BetBoom Team and Xtreme Gaming both finish last in their group, assign BetBoom Team 11th, and Xtreme Gaming 12th.  Do not assign one team to two positions.  This prevents the solver from finding a result.
- If the constraints are wrong, you will not get a single result for any team.  An example would be if you assign a team that did not qualify for ESL One Birmingham a finishing position at ESL One Birmingham, or assign one team two positions as stated above.  For this reason, I recommend backing-up the script before each update, just in case you need to undo.
