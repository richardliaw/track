# track

## Installation
`pip install track`

## Usage

```
import track 

def training_function():
    trial = track.Trial("ProjectName", "~/results")
    trial.start()
    for i in range(N):
        # train model ...
        trial.log_metric()
        
    trial.end()
```
        
    
