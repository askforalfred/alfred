# Errata

The subgoal evaluation numbers for `Goto` in Table 4 of the [paper](https://arxiv.org/pdf/1912.01734.pdf) used the following success criteria for navigation: (1) the agent is less than **5 A-Star steps** away from the target location in the expert plan, and (2) the target object in the next subgoal is **visible**. But as noted in [issue59](https://github.com/askforalfred/alfred/issues/59), the visibility requirement cannot be satisifed for subgoals where the object is enclosed inside a receptacle, for e.g, inside a fridge.  

As of 14 Dec 2020, we have updated the `Goto` success criteria to: (1) less than **3 A-Star steps** away from the target location. The updated results for Table 4 are as follows:

| Model | Goto |
| --- | ----------- |
| Seen - No Lang | 45 |
| Seen - S2S | 51 |
| Seen - S2S + PM | 49 |
| Unseen - No Lang | 27 |
| Unseen - S2S | 33 |
| Unseen - S2S + PM | 32 |


**Note**: the main results and leaderboard evaluations are unaffected by this change.
