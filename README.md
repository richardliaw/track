# tracker

## Installation
`pip install tracker` (Not yet)

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
        
    
