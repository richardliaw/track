# tracker

## Installation

`pip install tracker` (Not yet). Until we get pypi set up, use

```
pip install git+git://github.com/richardliaw/tracker.git#egg=tracker
```

## Usage

```
import tracker 

def training_function():
    trial = tracker.Trial("~/results", "remote_dir")
    trial.start()
    for i in range(N):
        # train model ...
        trial.metric()
        
    trial.close()
```
        
    
