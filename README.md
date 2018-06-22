# track

## Installation
`pip install track` (Not yet)

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
        
    
