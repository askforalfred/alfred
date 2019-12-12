# ALFRED

[<b>A Benchmark for Interpreting Grounded Instructions for Everyday Tasks</b>](https://arxiv.org/abs/1912.01734)  
[Mohit Shridhar](https://mohitshridhar.com/), [Jesse Thomason](https://jessethomason.com/), [Daniel Gordon](https://homes.cs.washington.edu/~xkcd/), [Yonatan Bisk](https://yonatanbisk.com/),  
[Winson Han](https://allenai.org/team.html), [Roozbeh Mottaghi](http://roozbehm.info/), [Luke Zettlemoyer](https://www.cs.washington.edu/people/faculty/lsz), [Dieter Fox](https://homes.cs.washington.edu/~fox/)

**ALFRED** (**A**ction **L**earning **F**rom **R**ealistic **E**nvironments and **D**irectives), is a new benchmark for learning a mapping from natural language instructions and egocentric vision to sequences of actions for household tasks. Long composition rollouts with non-reversible state changes are among the phenomena we include to shrink the gap between research benchmarks and real-world applications.

## Dataset

Each expert demonstration contains 3 or more language annotations in `traj_data.json`:

Task Info:
```
['task_id'] = "trial_00003_T20190312_234237"		(unique trajectory ID)
['task_type'] = "pick_heat_then_place_in_recep"		(one of 7 task types)
['pddl_params'] = {'object_target': "AlarmClock",	(object)
				   'parent_target': "DeskLamp",		(receptacle)
                   'mrecep_target': "",				(movable receptacle)
                   "toggle_target": "",				(toggle object)
                   "object_sliced": false			(should object be sliced?)
				  }
```

Scene Info:
```
['scene'] =  {'floor_plan': "FloorPlan7",			(THOR scene name)
              'scene_num' : 7,						(THOR scene number)
              'random_seed': 3810970210, 		 	(seed for initializing object placements)
              'init_action' : <API_CMD> 		 	(called to set the starting position of the agent)
              'object_poses': <LIST_OBJS> 		 	(initial 6DOF poses of objects in the scene)
              'object_toggles': <LIST_OBJS>      	(initial states of togglable objects)
              }
```

## Code

Coming soon ...

## Citation

```
@Unpublished{ALFRED,
  title={{ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks}},
  author={Mohit Shridhar and Jesse Thomason and Daniel Gordon and Yonatan Bisk and Winson Han and Roozbeh Mottaghi and Luke Zettlemoyer and Dieter Fox},
  year={2019},
}
```
