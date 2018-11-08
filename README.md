# track

## Installation

Just use:

```
pip install track-ml
```

Right now this requires python 3.

## Usage

Report various metrics of interest, with automatically configured and persisted logging.

```python
import track 

def training_function(param1=0.01, param2=10):
    local = "~/track/myproject"
    remote = "s3://my-track-bucket/myproject"
    with track.trial(local, remote, param_map={"param1": param1, "param2": param2}):
        model = create_model()
        for epoch in range(100):
            model.train()
            loss = model.get_loss()
            track.metric(iteration=epoch, loss=loss)
            track.debug("epoch {} just finished with loss {}", epoch, loss)
            model.save(os.path.join(track.trial_dir(), "model{}.ckpt".format(epoch)))
```
        
Inspect existing experiments

```bash
$ python -m track.trials --local_dir ~/track/myproject trial_id "start_time>2018-06-28" param2
trial_id    start_time                param2
8424fb387a 2018-06-28 11:17:28.752259 10
```

Plot results

```python
import track
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

proj = track.Project("~/track/myproject", "s3://my-track-bucket/myproject")
most_recent = proj.ids["start_time"].idxmax()
most_recent_id = proj.ids["trial_id"].iloc[[most_recent]]
res = proj.results(most_recent_id)
plt.plot(res[["iteration", "loss"]].dropna())
plt.savefig("loss.png")
```

Recover saved artifacts

```python
model.load(proj.fetch_artifact(most_recent_id[0], 'model10.ckpt'))
model.serve_predictions()
```
