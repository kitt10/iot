#### Note
1/ A know-how file dialog.py is gitignored for this public repo (copied/deployed manually)

2/ On RPi: 
```
$ pip install async_generator
$ pip install PyEventEmitter
```
in backend/dialog.py (py < 3.7):
```
from async_generator import asynccontextmanager
```