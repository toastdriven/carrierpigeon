import json
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

print()

invoice_data = {
    "payee_id": 27,
    "payor_name": "Mr. Owes Me",
    "amount": 25.99,
    "paid_on": time.time(),
    "version": 1,
}
invoice = library.InvoiceCreated.read(json.dumps(invoice_data))
print(f"Invoice paid by {invoice.payor_name} in amount of ${invoice.amount}.")

print()

user_followed_data = {
    "user_id": 1257,
    "follower_id": 873,
    "created": time.time(),
    "version": 2,
}
follow = library.UserFollowed.read(json.dumps(user_followed_data))
print(f"{follow.follower_id} just followed {follow.user_id}.")
