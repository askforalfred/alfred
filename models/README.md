# Models

We provide PyTorch code and pre-trained models for baseline seq2seq models describe in the paper.

![](../media/model.png)

## Training

Following the [quickstart](../README.md) installation, to start training seq2seq models:

```bash
$ cd $ALFRED_ROOT
$ python models/train/train_seq2seq.py --data data/json_feat_2.1.0 --model seq2seq_im_mask --dout exp/model:{model},name:pm_and_subgoals_01 --splits data/splits/oct21.json --gpu --batch 8 --pm_aux_loss_wt 0.2 --subgoal_aux_loss_wt 0.2 ---preprocess
```

Run this once with `--preprocess` to save preprocessed jsons inside the trajectory folders. This could take a few minutes, but subsequent runs can be deployed without any data preprocessing. See [train_seq2seq.py](train/train_seq2seq.py) for hyper-parameters and other settings. 


## Evaluation

The evaluation is measures the performance of 

### Task Evaluation

### Subgoal Evaluation

## File Structure


## Pre-trained Models

Coming soon ...