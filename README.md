# carrierpigeon

Contract-based messages.


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

greet = library.Greeting(greeting="Hey", name="friendo")
print(greet.create())
# '{"version": 1, "greeting": "Hey", "name": "friendo"}'
```


## Requirements

* Python 3.8+ (though may work on previous versions)
* `jsonschema`


## License

New BSD


## TODO

* [ ] Actual tests, rather than just an example script
* [ ] Still JSON-heavy
* [ ] Validation support (fields)
* [ ] Better validation errors w/ JSONSchema
* [ ] The `version` expectations may be too heavy-handed
* [ ] Needs benchmarking/testing for efficiency
* [ ] Protobuf support?
* [ ] XML support?
* [ ] JSONb support?
