# carrierpigeon

Contract-based messages.

[![Build Status](https://travis-ci.com/toastdriven/carrierpigeon.svg?token=H4mXeuGAKKquLkHVssh3&branch=main)](https://travis-ci.com/toastdriven/carrierpigeon)


## Quick Start

```python
import carrierpigeon as cp

# Create a class from a JSONSchema.
Greeting = cp.message_for("schemas/greeting.json")

# It's a Python object.
greet = Greeting(greeting="Hello", name="world")
print(f"{greet.greeting}, {greet.name}!")
# "Hello, world!"

# You can create a contract-driven, serialized message to transfer over
# the wire.
print(greet.create())
# '{"version": 1, "greeting": "Hello", "name": "world"}'

# ...And you can read similar messages back.
read_msg = Greeting.read('{"version": 1, "greeting": "Bonjour", "name": "madame"}')
print(f"{read_msg.greeting}, {read_msg.name}!")
# "Bonjour, madame!"
```

...or, if you have a bunch of schemas/contracts:

```python
import carrierpigeon as cp

library = cp.load_library("schemas/")

# All contract objects will now be present on the library for use.
greet = library.Greeting(greeting="Hey", name="friendo")

print(greet.create())
# '{"version": 1, "greeting": "Hey", "name": "friendo"}'
```


## Requirements

* Python 3.6+
* `jsonschema`


## License

New BSD


## Running Tests

```shell
$ pytest tests
```

Highly recommend that you either use `poetry` or `virtualenv` to isolate the
package before testing.


## TODO

* [x] Actual tests, rather than just an example script
* [x] Better validation errors w/ JSONSchema
* [x] The `version` expectations may be too heavy-handed
* [x] Interactive schema-creation tool (`bin/schema_creator.py`)
* [ ] Still JSON-heavy
* [ ] Validation support (fields)
* [ ] Documentation
* [ ] Needs benchmarking/testing for efficiency
* [ ] Protobuf support?
* [ ] XML support?
* [ ] JSONb support?
