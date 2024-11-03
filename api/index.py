import os, traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from . import crons
from .models import ShopOrder, Person
from .tasks import validate_and_freeze_order
from .fulfillment import fulfill
from .util import post_to_noise

app = FastAPI()
app.include_router(crons.router)


@app.exception_handler(Exception)
def slack_exception_handler(request: Request, exc: Exception):
    post_to_noise(f"""<@U06QK6AG3RD> karkalicious error!!
request url: {request.url}
---
{chr(10).join(traceback.format_exception(None, exc, exc.__traceback__))}
""")
    err = exc.__str__()
    return JSONResponse(status_code=500,
                        content={
                            "error_code": "oh_no",
                            "error_message":  err
                        })


@app.get("/cause_error")
def cause_error():
    raise ValueError("meowwww :3")
@app.get("/health-check")
def status_check():
    nora = Person.from_id("rec5TFOw9pNNgRIKb")
    nora.save()  # see if someone broke the schema
    return {"status": "we gucci!!"}

@app.post("/process/{rec}")
def freeze_single_order(rec):
    order: ShopOrder = ShopOrder.from_id(rec)
    if not order:
        raise HTTPException(status_code=404, detail="rec id not found!")
    if order.dev != (os.environ.get("ENV") == "DEV"): return {"message":"wrong env, ignoring"}
    return {"message": validate_and_freeze_order(order)}

@app.post("/fulfill/{rec}")
def fulfill_single_order(rec):
    print("meow")
    order: ShopOrder = ShopOrder.from_id(rec)
    if order.dev != (os.environ.get("ENV") == "DEV"): return {"message":"wrong env, ignoring"}
    if not order:
        raise HTTPException(status_code=404, detail="rec id not found!")
    try:
        if order.status != "in_flight": raise HTTPException(418, "huh?")
        return {"message": fulfill(order)}
    except Exception as e:
        raise HTTPException(500, {f"{repr(e)} in {str(e.__traceback__)}"})

