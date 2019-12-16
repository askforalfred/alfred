# ALFRED

[<b>A Benchmark for Interpreting Grounded Instructions for Everyday Tasks</b>](https://arxiv.org/abs/1912.01734)  
[Mohit Shridhar](https://mohitshridhar.com/), [Jesse Thomason](https://jessethomason.com/), [Daniel Gordon](https://homes.cs.washington.edu/~xkcd/), [Yonatan Bisk](https://yonatanbisk.com/),  
[Winson Han](https://allenai.org/team.html), [Roozbeh Mottaghi](http://roozbehm.info/), [Luke Zettlemoyer](https://www.cs.washington.edu/people/faculty/lsz), [Dieter Fox](https://homes.cs.washington.edu/~fox/)

**ALFRED** (**A**ction **L**earning **F**rom **R**ealistic **E**nvironments and **D**irectives), is a new benchmark for learning a mapping from natural language instructions and egocentric vision to sequences of actions for household tasks. Long composition rollouts with non-reversible state changes are among the phenomena we include to shrink the gap between research benchmarks and real-world applications.

![](media/instr_teaser.png)

## Quickstart

Clone repo:
```bash
$ git clone https://github.com/askforalfred/alfred.git alfred
$ export ALFRED_ROOT=$(pwd)/alfred
```

Install requirements:
```bash
$ virtualenv -p $(which python3) --system-site-packages alfred_env # or whichever package manager you prefer
$ source alfred_env/bin/activate

$ cd $ALFRED_ROOT
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

Download JSONs and Resnet feats (~215GB):
```bash
$ cd $ALFRED_ROOT/data
$ sh download_data.sh json_feat
```

Train models:
```bash
$ python models/train/train_seq2seq.py --data data/json_feat_2.1.0 --model seq2seq_im_mask --dout exp/model:{model},name:pm_and_subgoals_01 --splits data/splits/oct21.json --gpu --batch 8 --pm_aux_loss_wt 0.2 --subgoal_aux_loss_wt 0.2
```

## Guides 

- [**Dataset**](data/README.md): Downloading full dataset, Folder structure, JSON structure.
- [**Models**](models/README.md): Training and Evaluation, File structure.
- [**Data Generation**](gen/README.md): Generation, Replay Checks, Data Augmentation (depth, segementation masks etc.)

## Leaderboard

Coming soon...

## Citation

```
@misc{ALFRED19,
  title ={{ALFRED: A Benchmark for Interpreting Grounded
           Instructions for Everyday Tasks}},
  author={Mohit Shridhar and Jesse Thomason and
          Daniel Gordon and Yonatan Bisk and
          Winson Han and Roozbeh Mottaghi and
          Luke Zettlemoyer and Dieter Fox},
  year = {2019},
  url  = {https://arxiv.org/abs/1912.01734}
}
```

## License

MIT License

## Contact

Questions or issues? Contact [askforalfred@googlegroups.com](askforalfred@googlegroups.com)