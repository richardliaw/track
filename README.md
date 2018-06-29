# track

## Installation

`pip install track` (Not yet). Until we get pypi set up (there's another `track` package...), use

```
pip install --upgrade git+https://github.com/richardliaw/track.git@master#egg=track
```

## Usage

Report various metrics of interest (if you launch within a git repository `myproject`, the local directory `~/track/myproject` is automatically inferred below).

```
import track 

def training_function(param1=0.01, param2=10):
    with track.trial("~/track/myproject", "s3://my-track-bucket/myproject"):
        model = create_model()
        for epoch in range(100):
            model.train()
            loss = model.get_loss()
            track.metric(iteration=epoch, loss=loss)
```
        
Inspect existing experiments (from anywhere, if you supply `--remote_dir`)

```
$ python -m track.trials --local_dir ~/track/myproject trial_id "start_time>2018-06-28" param2
trial_id    start_time                param2
8424fb387a 2018-06-28 11:17:28.752259 10
```

Plot results (from anywhere)

```
import track
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

remote_dir = "s3://my-track-bucket/myproject"
proj = track.Project("~/track/myproject", remote_dir)
most_recent = proj.ids["start_time"].idxmax()
most_recent_id = proj.ids["trial_id"].iloc[[most_recent]]
res = proj.results(most_recent_id)
plt.plot(res["loss"].dropna())
plt.savefig("loss.png")
```
