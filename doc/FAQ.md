# Frequently Asked Questions


### Are the step-by-step instructions aligned with subgoals?

Yes, each step-by-step instruction has a corresponding subgoal in the training and validation trajectories. If you use this alignment during training, please see the [submission guidelines](https://leaderboard.allenai.org/alfred/submissions/get-started) for leaderboard submissions. 

### Getting 100% success rate with ground-truth trajectories

You should be able to achieve **>99%** success rate on training and validation tasks with the ground-truth actions and masks from the dataset. Occasionally, some [non-determistic behaviors](https://github.com/askforalfred/alfred/issues/19) in THOR can lead to failures, but they are extremely rare. 

### Can you train an agent without mask prediction?

Mask prediction is an important part of the ALFRED challenge. Unlike non-interactive environments (e.g vision-language navigation) here it's necessary for the agent to specify *what* exactly it wants to interact with.

### Why do `feat_conv.pt` in [Full Dataset](https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/full_2.1.0.7z) have 10 more frames than the number of images?

The last 10 frames are copies of the features from the last image frame. 

### Can I train with templated goal descriptions?

Yes. Run the training script with `--use_templated_goals`.

### How do I get panoramic image observations?

You can use [augment_trajectories.py](../gen/scripts/augment_trajectories.py) to replay all the trajectories and augment the visual observations. At each [step](https://github.com/askforalfred/alfred/blob/a88bafac23a21725087d5a7b484dfcadeef1c5dc/gen/scripts/augment_trajectories.py#L137), use the THOR API to look around and take 6-12 shots of the surrounding. Then stitch together these shots to create a panoramic image for each frame. You might have to set `'forceAction': True` for [smooth moveahead/rotate/look](https://github.com/askforalfred/alfred/blob/a88bafac23a21725087d5a7b484dfcadeef1c5dc/env/thor_env.py#L258). Note that getting panoramic images during test time would incur the additional cost of looking around with the agent.  

### Why do `feat_conv.pt` in [Modeling Quickstart](https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/json_feat_2.1.0.7z) contain fewer frames than in [Full Dataset](https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/full_2.1.0.7z)

The [Full Dataset](https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/full_2.1.0.7z) contains extracted Resnet features for each frame in `['images']` which include filler frames inbetween each low-action (used to generate smooth videos), whereas [Modeling Quickstart](https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/json_feat_2.1.0.7z) only contains features for each `low_idx` that correspond to frames after taking each low-level action. 

### Can I train the model on a smaller dataset for quick debugging?

Yes, run the training script with `--fast_epoch`.
