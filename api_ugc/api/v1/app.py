from main import app, producer


@app.get("/v1/api")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/v1/api/movies/event")
def read_item() -> dict[str, str]:
    event = producer.send_generated_event()

    return {"msg": f"Event sent: {event}"}
