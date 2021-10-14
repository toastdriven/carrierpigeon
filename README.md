# carrierpigeon

Contract-based messages.

You define (or are given) a contract, which at present is a
(JSONSchema)[https://json-schema.org/understanding-json-schema/index.html].

`carrierpigeon` takes that contract & builds Python objects for
reading/writing those messages. It doesn't handle transport, so you're free
to integrate it into any messaging environment you'd like.

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


## Why Contracts?

When you have multiple services communicating, it's useful to define what
messages should look like up front.

Without a contract, you risk passing around a non-standardized bag of data.
It's easy for typos to creep in, difficult to tell when new things have been
added, & drift between libraries/services tends to grow.

With a contract, you can choose what version(s) of messages you'll accept,
validation will guarantee the data coming in or going out looks correct, &
producing/consuming those messages can be more standardized.

To make things easier, `carrierpigeon` includes tooling to help create
those contracts as well. See the `bin/schema_creator.py` script for a way
to easily/interactively create the JSONSchema cntracts.


## Why JSONSchema?

Interoperability, simplicity, & readability are the biggest drivers. There
are many libraries (in most languages) that can use JSONSchema. JSON itself
is pretty readable & widely-supported. And debugging should never be a chore.


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
* [ ] BSON support?
* [ ] XML support?
