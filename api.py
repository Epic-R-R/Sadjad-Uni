from typing import Optional
from validator import UrlValidator
from helper import finder_url
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/url/{item_id}")
def get_link(item_id: int, q: Optional[str]):
    print(q)
    q = q.replace("#", "&")
    q = q.replace(" ", "%")
    print(q)
    if UrlValidator(q) is not None:
        link = 'https://vc2.sadjad.ac.ir/{}/output/{}.zip?download=zip'.format(finder_url(q), finder_url(q))
        print(link)
        return {"Class Link": link}
    # return {"Error": "File not found!"}