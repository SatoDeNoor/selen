# Selen ![develop](https://github.com/SatoDeNoor/selen/actions/workflows/python-app.yml/badge.svg?branch=develop)

---

Selen is a selenium wrapper. 

## Installation
```commandline
pip install git+https://github.com/SatoDeNoor/selen.git
```

## Features

###### Shadow Root

For define element under shadow root:
```python
from selen.client.driver import Operations
...
shadow_element = Operations.shadow_element(shadow_root='shadow root css',
                                           selector='css selector',
                                           option='basic')
...
```

###### Javascript drag and drop

For javascript drag and drop use next:
```python
from selen.client.driver import Operations
...
source = Operations.web_element('//source')
destination = Operations.web_element('//destination')
Operations.drag_n_drop(source, destination, option='js')
...
```