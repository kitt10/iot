## The backend engine for the SMARTHOME project

### Run on RPi

Get the latest ```smarthome``` version

```sh
$ git pull
```
or
```sh
$ git fetch
$ git reset --hard master/origin
```

Update the IP address for the frontend
```sh
$ cd frontend
$ nano script.js # Line 2: replace localhost by IP of the server (RPi: 147.228.124.68)
```

If not done yet, init default models:
```sh
$ cd backend
$ sudo python3 model.py -m init -df 2020-01-10 -dt 2020-01-17 # df: date_from, dt: date_to
```

Run the engine:
```sh
$ cd backend
$ sudo python3 engine.py
```

Project running on 147.228.124.68:8881