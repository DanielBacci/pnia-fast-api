from fastapi import FastAPI, Request

from source.models import PhoneBusiness, PrefixTrie

app = FastAPI()


@app.post("/load-file")
def load_file():
    prefix_trie = PrefixTrie()
    prefix_trie.build()
    # CACHE
    return {}


@app.post("/aggregate")
async def aggregate(request: Request):
    body = await request.body()
    retrieve_business = PhoneBusiness()
    phones = retrieve_business.phones_from_body(body)
    return retrieve_business.build(phones)
