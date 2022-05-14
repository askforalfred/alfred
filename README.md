# ALFRED

[<b>A Benchmark for Interpreting Grounded Instructions for Everyday Tasks</b>](https://arxiv.org/abs/1912.01734)  
[Mohit Shridhar](https://mohitshridhar.com/), [Jesse Thomason](https://jessethomason.com/), [Daniel Gordon](https://homes.cs.washington.edu/~xkcd/), [Yonatan Bisk](https://yonatanbisk.com/),  
[Winson Han](https://allenai.org/team.html), [Roozbeh Mottaghi](http://roozbehm.info/), [Luke Zettlemoyer](https://www.cs.washington.edu/people/faculty/lsz), [Dieter Fox](https://homes.cs.washington.edu/~fox/)  
[CVPR 2020](http://cvpr2020.thecvf.com/)

**ALFRED** (**A**ction **L**earning **F**rom **R**ealistic **E**nvironments and **D**irectives), is a new benchmark for learning a mapping from natural language instructions and egocentric vision to sequences of actions for household tasks. Long composition rollouts with non-reversible state changes are among the phenomena we include to shrink the gap between research benchmarks and real-world applications.

For the latest updates, see: [**askforalfred.com**](https://askforalfred.com)

![](media/instr_teaser.png)

**What more?** Checkout [ALFWorld](https://github.com/alfworld/alfworld) – interactive TextWorld environments for ALFRED scenes!

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

Download Trajectory JSONs and Resnet feats (~17GB):
```bash
$ cd $ALFRED_ROOT/data
$ sh download_data.sh json_feat
```

Train models:
```bash
$ cd $ALFRED_ROOT
$ python models/train/train_seq2seq.py --data data/json_feat_2.1.0 --model seq2seq_im_mask --dout exp/model:{model},name:pm_and_subgoals_01 --splits data/splits/oct21.json --gpu --batch 8 --pm_aux_loss_wt 0.1 --subgoal_aux_loss_wt 0.1
```

## More Info 

- [**Dataset**](data/): Downloading full dataset, Folder structure, JSON structure.
- [**Models**](models/): Training and Evaluation, File structure, Pre-trained models.
- [**Data Generation**](gen/): Generation, Replay Checks, Data Augmentation (high-res, depth, segementation masks etc).
- [**Errata**](models/ERRATA.md): Updated numbers for Goto subgoal evaluation.
- [**THOR 2.1.0 Docs**](https://allenai.github.io/ai2thor-v2.1.0-documentation/installation): Deprecated documentation from Ai2-THOR 2.1.0 release.
- [**FAQ**](doc/FAQ.md): Frequently Asked Questions. 

## SOTA Models

Open-source models that outperform the Seq2Seq baselines from ALFRED:  
<br>
<b> FILM: Following Instructions in Language with Modular Methods </b>
<br>
So Yeon Min, Devendra Singh Chaplot, Pradeep Ravikumar, Yonatan Bisk, Ruslan Salakhutdinov
<br>
<a href="https://arxiv.org/pdf/2110.07342.pdf"> Paper</a>, <a href="https://github.com/soyeonm/FILM"> Code </a>

<b> A Persistent Spatial Semantic Representation for High-level Natural Language Instruction Execution </b>
<br>
Valts Blukis, Chris Paxton, Dieter Fox, Animesh Garg, Yoav Artzi
<br>
<a href="https://arxiv.org/pdf/2107.05612.pdf"> Paper</a>, <a href="https://github.com/valtsblukis/hlsm"> Code </a>

<b> Hierarchical Task Learning from Language Instructions with Unified Transformers and Self-Monitoring </b>
<br>
Yichi Zhang, Joyce Chai
<br>
<a href="https://aclanthology.org/2021.findings-acl.368/"> Paper</a>, <a href="https://github.com/594zyc/HiTUT"> Code </a>

<b> Episodic Transformer for Vision-and-Language Navigation </b>
<br>
Alexander Pashevich, Cordelia Schmid, Chen Sun
<br>
<a href="https://arxiv.org/pdf/2105.06453.pdf"> Paper</a>, <a href="https://github.com/alexpashevich/E.T."> Code </a>

<b> MOCA: A Modular Object-Centric Approach for Interactive Instruction Following </b>
<br>
Kunal Pratap Singh*, Suvaansh Bhambri*, Byeonghwi Kim*, Roozbeh Mottaghi, Jonghyun Choi
<br>
<a href="https://arxiv.org/abs/2012.03208"> Paper</a>, <a href="https://github.com/gistvision/moca"> Code </a>  

<b> Embodied BERT: A Transformer Model for Embodied, Language-guided Visual Task Completion </b>
<br>
Alessandro Suglia, Qiaozi Gao, Jesse Thomason, Govind Thattai, Gaurav Sukhatme  
<a href="https://arxiv.org/abs/2108.04927">Paper</a>, <a href="https://github.com/amazon-research/embert"> Code </a>

Contact [Mohit](https://mohitshridhar.com/) to add your model here. 

## Prerequisites

- Python 3
- PyTorch 1.1.0
- Torchvision 0.3.0
- AI2THOR 2.1.0

See [requirements.txt](requirements.txt) for all prerequisites

## Hardware 

Tested on:
- **GPU** - GTX 1080 Ti (12GB)
- **CPU** - Intel Xeon (Quad Core)
- **RAM** - 16GB
- **OS** - Ubuntu 16.04


## Leaderboard

Run your model on test seen and unseen sets, and create an action-sequence dump of your agent:

```bash
$ cd $ALFRED_ROOT
$ python models/eval/leaderboard.py --model_path <model_path>/model.pth --model models.model.seq2seq_im_mask --data data/json_feat_2.1.0 --gpu --num_threads 5
```

This will create a JSON file, e.g. `task_results_20191218_081448_662435.json`, inside the `<model_path>` folder. Submit this JSON here: [AI2 ALFRED Leaderboard](https://leaderboard.allenai.org/alfred/submissions/public). For rules and restrictions, see the [getting started page](https://leaderboard.allenai.org/alfred/submissions/get-started).  

**Rules:** 
1. You are only allowed to use **RGB** and **language instructions (goal & step-by-step)** as input for your agents. You **cannot use additional depth, mask, metadata info etc.** from the simulator on Test Seen and Test Unseen scenes. However, during training you are allowed to use additional info for auxiliary losses etc.
2. During evaluation, agents are restricted to `max_steps=1000` and `max_fails=10`. Do not change these settings in the [leaderboard script](https://github.com/askforalfred/alfred/blob/master/models/eval/leaderboard.py); these modifications will not be reflected in the evaluation server.
3. :exclamation:Do not spam the leaderboard with repeated submissions (under different email accounts) in order to optimize on the test set. Fine-tuning should be done only on the validation set, NOT on the leaderboard test set. 
4. Pick a legible model name for the submission. Just "baseline" is not very descriptive.
5. All submissions must be attempts to solve the ALFRED dataset.
6. Answer the following questions in the description: a. Did you use additional sensory information from THOR as input, eg: depth, segmentation masks, class masks, panoramic images etc. during test-time? If so, please report them. b. Did you use the alignments between step-by-step instructions and expert action-sequences for training or testing? (no by default; the instructions are serialized into a single sentence)
7. Share who you are: provide a team name and affiliation. 
8. _(Optional)_ Share how you solved it: if possible, share information about how the task was solved. Link an academic paper or code repository if public.
9. Only submit your own work: you may evaluate any model on the validation set, but must only submit your own work for evaluation against the test set.


## Docker Setup

Install [Docker](https://docs.docker.com/engine/install/ubuntu/) and [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker#ubuntu-160418042004-debian-jessiestretchbuster). 

Modify [docker_build.py](scripts/docker_build.py) and [docker_run.py](scripts/docker_run.py) to your needs.

#### Build 

Build the image:

```bash
$ python scripts/docker_build.py 
```

#### Run (Local)

For local machines:

```bash
$ python scripts/docker_run.py
 
  source ~/alfred_env/bin/activate
  cd $ALFRED_ROOT
```

#### Run (Headless)

For headless VMs and Cloud-Instances:

```bash
$ python scripts/docker_run.py --headless 

  # inside docker
  tmux new -s startx  # start a new tmux session

  # start nvidia-xconfig
  sudo nvidia-xconfig -a --use-display-device=None --virtual=1280x1024

  # start X server on DISPLAY 0
  # single X server should be sufficient for multiple instances of THOR
  sudo python ~/alfred/scripts/startx.py 0  # if this throws errors e.g "(EE) Server terminated with error (1)" or "(EE) already running ..." try a display > 0

  # detach from tmux shell
  # Ctrl+b then d

  # source env
  source ~/alfred_env/bin/activate
  
  # set DISPLAY variable to match X server
  export DISPLAY=:0

  # check THOR
  cd $ALFRED_ROOT
  python scripts/check_thor.py

  ###############
  ## (300, 300, 3)
  ## Everything works!!!
```

You might have to modify `X_DISPLAY` in [gen/constants.py](gen/constants.py) depending on which display you use.

## Cloud Instance

ALFRED can be setup on headless machines like AWS or GoogleCloud instances. 
The main requirement is that you have access to a GPU machine that supports OpenGL rendering. Run [startx.py](scripts/startx.py) in a tmux shell:
```bash
# start tmux session
$ tmux new -s startx 

# start X server on DISPLAY 0
# single X server should be sufficient for multiple instances of THOR
$ sudo python $ALFRED_ROOT/scripts/startx.py 0  # if this throws errors e.g "(EE) Server terminated with error (1)" or "(EE) already running ..." try a display > 0

# detach from tmux shell
# Ctrl+b then d

# set DISPLAY variable to match X server
$ export DISPLAY=:0

# check THOR
$ cd $ALFRED_ROOT
$ python scripts/check_thor.py

###############
## (300, 300, 3)
## Everything works!!!
```

You might have to modify `X_DISPLAY` in [gen/constants.py](gen/constants.py) depending on which display you use.

Also, checkout this guide: [Setting up THOR on Google Cloud](https://medium.com/@etendue2013/how-to-run-ai2-thor-simulation-fast-with-google-cloud-platform-gcp-c9fcde213a4a)

## Citation

If you find the dataset or code useful, please cite:

```
@inproceedings{ALFRED20,
  title ={{ALFRED: A Benchmark for Interpreting Grounded
           Instructions for Everyday Tasks}},
  author={Mohit Shridhar and Jesse Thomason and Daniel Gordon and Yonatan Bisk and
          Winson Han and Roozbeh Mottaghi and Luke Zettlemoyer and Dieter Fox},
  booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2020},
  url  = {https://arxiv.org/abs/1912.01734}
}
```

## License

MIT License

## Change Log

14/10/2020:
- Added [errata](models/ERRATA.md) for `Goto` subgoal evaluation. 

28/10/2020:
- Added `--use_templated_goals` option to train with templated goals instead of human-annotated goal descriptions.

26/10/2020:
- Fixed missing stop-frame in Modeling Quickstart dataset (`json_feat_2.1.0.zip`). 

07/04/2020:
- Updated download links. Switched from Google Cloud to AWS. Old download links will be deactivated.


28/03/2020:
- Updated the mask-interaction API to use IoU scores instead of max pixel count for selecting objects.
- Results table in the paper will be updated with new numbers.

## Contact

Questions or issues? Contact [askforalfred@googlegroups.com](askforalfred@googlegroups.com)
