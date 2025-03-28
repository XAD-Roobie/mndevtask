Requires python3 (Tested on 3.10.8)

Install package requirements

```
pip3 install -r requirements.txt
```

For the first run follow the Makefile commands

```
make init_db
make run
```

Now you can run curl commands against the endpoint

e.g
```
curl -XPOST http://127.0.0.1:1337/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "42.00", "user_id": 1, "t": 0}'
```

Note: The endpoint is on the port of 1337 to avoid conflicts with other local services


I have included a full suite of tests using pytest which can be fired with the below make commands

```
make test
make test_cov
```

Additionally there is a python script in the main directory which directly hits the flask server when its running,
which can be triggered with `python3 tests.py` and finally all of the logs for the server can be read from the flask.log with `tail -f flask.log`
