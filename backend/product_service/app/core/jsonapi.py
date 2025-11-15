from fastapi.responses import JSONResponse


class JSONAPIResponse(JSONResponse):
    media_type = "application/vnd.api+json"


def jsonapi_resource(resource_type: str, resource_id: str | int, attributes: dict) -> dict:
    return {
        "type": resource_type,
        "id": str(resource_id),
        "attributes": attributes,
    }


def jsonapi_single(resource_type: str, resource_id: str | int, attributes: dict) -> dict:
    return {"data": jsonapi_resource(resource_type, resource_id, attributes)}


def jsonapi_list(resource_type: str, items: list[dict], meta: dict | None = None) -> dict:
    data = [jsonapi_resource(resource_type, item["id"], item["attributes"]) for item in items]
    payload: dict = {"data": data}
    if meta:
        payload["meta"] = meta
    return payload


def jsonapi_error(status: int, title: str, detail: str | None = None, pointer: str | None = None) -> JSONAPIResponse:
    error: dict = {"status": str(status), "title": title}
    if detail:
        error["detail"] = detail
    if pointer:
        error["source"] = {"pointer": pointer}
    return JSONAPIResponse(status_code=status, content={"errors": [error]})
