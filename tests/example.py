import os
import time

import carrierpigeon as cp


BASE_DIR = os.path.dirname(__file__)


schema = os.path.join(BASE_DIR, "schemas", "greeting.v1.json")
Greeting = cp.message_for(schema)

greet = Greeting(greeting="Hi", name="Daniel")
print(f"{greet.greeting}, {greet.name}!")

print()

msg_1 = greet.create()
print(f"Message to send: {msg_1}")

print()

read_msg = Greeting.read('{"version": 1, "greeting": "Hello", "name": "world"}')
print(f"{read_msg.greeting}, {read_msg.name}!")

print()

roundtrip_msg = Greeting.read(msg_1)
print(f"Roundtrip greeting says: {read_msg.greeting}, {read_msg.name}!")


print()

blog_schema = os.path.join(BASE_DIR, "schemas", "post_created.v1.json")
PostCreated = cp.message_for(blog_schema)

post = PostCreated(
    title="First Post!",
    content="This is my very first blog entry. OBVIOUSLY, there will be many more to come...",
    author_id=1,
    created=time.time(),
)
print(post.create())

print()

library = cp.load_library(os.path.join(BASE_DIR, "schemas"))
print("Library loaded.")
print(f"Available classes: {library.available_classes()}")

new_greet = library.Greeting(greeting="Hey", name="friendo")
print(new_greet.create())
