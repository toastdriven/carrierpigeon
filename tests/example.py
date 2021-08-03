import os

import carrierpigeon as cp


BASE_DIR = os.path.dirname(__file__)


schema = os.path.join(BASE_DIR, "schemas", "greeting.v1.json")
Greeting = cp.message_for(schema)

greet = Greeting(greeting="Hi", name="Daniel")
print(f"{greet.greeting}, {greet.name}!")

print()

read_msg = Greeting.read('{"version": 1, "greeting": "Hello", "name": "world"}')
print(f"{read_msg.greeting}, {read_msg.name}!")
