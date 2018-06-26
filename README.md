# track

## Installation

`pip install track` (Not yet). Until we get pypi set up, use

```
pip install --upgrade git+git://github.com/richardliaw/track.git#egg=track
```

Or if your project has a `setup.py`, it should contain the following:

```

install_requires = [
    # ...
    'track',                                                                                ]

setup(name="your_package_name",
      install_requires=install_requires,
      dependency_links=[
setup(name="asn4sql", author="RISE Lab",
      install_requires=install_requires,
      dependency_links=[
          'https://github.com/richardliaw/track/archive/master.zip#egg=track',])
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
        
    
