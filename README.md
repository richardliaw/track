# tracker

## Installation

`pip install tracker` (Not yet). Until we get pypi set up, use

```
pip install --upgrade git+git://github.com/richardliaw/tracker.git#egg=tracker
```

Or if your project has a `setup.py`, it should contain the following:

```

install_requires = [
    # ...
    'tracker',                                                                                ]

setup(name="your_package_name",
      install_requires=install_requires,
      dependency_links=[
setup(name="asn4sql", author="RISE Lab",
      install_requires=install_requires,
      dependency_links=[
          'https://github.com/richardliaw/tracker/archive/master.zip#egg=tracker',])
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
        
    
