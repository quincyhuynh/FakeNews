
import webhose
webhose.config(token="456af32b-3c58-455d-b9f8-90875bfc8f58")

r = webhose.search("foobar")
print(r.posts[0])