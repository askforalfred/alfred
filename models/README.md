# Models

We provide PyTorch code and pre-trained models for the baseline seq2seq models described in the paper.

![](../media/model.png)

## Training

Following the [quickstart](../README.md) installation, to start training seq2seq models:

```bash
$ cd $ALFRED_ROOT
$ python models/train/train_seq2seq.py --data data/json_feat_2.1.0 --model seq2seq_im_mask --dout exp/model:{model},name:pm_and_subgoals_01 --splits data/splits/oct21.json --gpu --batch 8 --pm_aux_loss_wt 0.2 --subgoal_aux_loss_wt 0.2 ---preprocess
```

Run this **once with** `--preprocess` to save preprocessed JSONs inside the trajectory folders. This could take a few minutes, but subsequent runs can be deployed without any preprocessing. See [train_seq2seq.py](train/train_seq2seq.py) for hyper-parameters and other settings. 


## Evaluation

### Task Evaluation

To evaluate a trained model through real-time execution on THOR:

```bash
$ python models/eval/eval_seq2seq.py --model_path <model_path>/best_seen.pth --eval_split valid_seen --data data/json_feat_2.1.0 --model models.model.seq2seq_im_mask --gpu --num_threads 3
```

Use `eval_split` to specify which split to evaluate, and `num_threads` to indicate the number of parallel evaluation threads to spawn. The experiments in the paper used `max_fails=10` and `max_steps=400`. The results will be dumped as a JSON file `task_results_<timestamp>.json` inside the `model_path` directory.

**Note:** If you are training and evaluating on different machines or if you just downloaded a checkpoint, you need to run eval with `--preprocess` once with the appropriate dataset path.


### Subgoal Evaluation

To evaluate individual subgoals for each task, run with `--subgoal`:

```bash
$ python models/eval/eval_seq2seq.py --model_path <model_path>/best_seen.pth --eval_split valid_seen --data data/json_feat_2.1.0 --model models.model.seq2seq_im_mask --gpu --num_threads 3 --subgoals all
```
This will use the expert demonstrations to reach the subgoal to be evaluated. You can specify `--subgoals all` to evaluate all subgoals, or select specific ones e.g `--subgoal GoalLocation,HeatObject`. Possible subgoals include `GotoLocation`, `PickupObject`, `PutObject`, `CleanObject`, `HeatObject`, `CoolObject`, `ToggleObject`, `SliceObject`. The results will be dumped as a JSON file `subgoal_results_<timestamp>.json` inside the `model_path` directory.


## File Structure

```
/model
    seq2seq.py           (base module with train and val loops)
    seq2seq_im_mask.py   (full model with batching and losses)
/nn
    vnn.py               (encoder, decoder, attention mechanisms)
    resnet.py            (pre-trained Resnet feature extractor)
/train
    train_seq2seq.py     (main with training args)
/eval
    eval_seq2seq.py      (main with eval args)
    eval_subgoals.py     (subgoal eval)
    eval_task.py         (overall task eval)
/config
    rewards.json         (reward values for actions; not used)
```

## Pre-trained Models

Download the [Seq2Seq+PM (both)](https://storage.googleapis.com/alfred_dataset/models/seq2seq_pm_chkpt.zip) model checkpoint:

```bash
$ wget https://storage.googleapis.com/alfred_dataset/models/seq2seq_pm_chkpt.zip 
$ unzip seq2seq_pm_chkpt.zip
```

The unzipped folder should contain `best_seen.pth` and `best_unseen.pth` checkpoints. 