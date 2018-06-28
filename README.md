# track

## Installation

`pip install track` (Not yet). Until we get pypi set up (there's another `track` package...), use

```
pip install --upgrade git+https://github.com/richardliaw/track.git@vlad-convenience#egg=track
```

## Usage

Report various metrics of interest.

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
        
