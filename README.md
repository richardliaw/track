# track

## Installation

`pip install track` (Not yet). Until we get pypi set up (there's another `track` package...), use

```
pip install https://github.com/richardliaw/track/archive/vlad-convenience.zip#egg=track
```

## Usage

```
import track 

def training_function():
    trial = track.Trial("~/results", "remote_dir")
    trial.start()
    for i in range(N):
        # train model ...
        trial.metric()
        
    trial.close()
```
        
    
