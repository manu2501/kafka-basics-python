from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
import httpx
import os

USER_URL = os.getenv("USER_SERVICE_URL", "http://user_service:8001")
ADMIN_URL = os.getenv("ADMIN_SERVICE_URL", "http://admin_service:8002")

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "API Gateway",
        "links": {"user": "/user/", "admin": "/admin/"},
    }

@app.api_route("/user", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_user_root(request: Request):
    return await proxy_user("", request)


@app.api_route("/user/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_user(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{USER_URL}/{path}"
        body = await request.body()
        resp = await client.request(
            request.method,
            url,
            content=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
        )
        headers = {
            k: v
            for k, v in resp.headers.items()
            if k.lower() not in ("content-length", "transfer-encoding", "content-encoding", "connection")
        }
        return Response(content=resp.content, status_code=resp.status_code, headers=headers, media_type=resp.headers.get("content-type"))

@app.api_route("/admin", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_admin_root(request: Request):
    return await proxy_admin("", request)

@app.api_route("/admin/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_admin(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{ADMIN_URL}/{path}"
        body = await request.body()
        # Stream SSE endpoints
        if request.method == "GET" and path.startswith("events"):
            stream = await client.stream(
                request.method,
                url,
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            )
            headers = {
                k: v
                for k, v in stream.headers.items()
                if k.lower() not in ("content-length", "transfer-encoding", "content-encoding", "connection")
            }
            return StreamingResponse(stream.aiter_bytes(), status_code=stream.status_code, media_type=stream.headers.get("content-type"), headers=headers)

        resp = await client.request(
            request.method,
            url,
            content=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
        )
        headers = {
            k: v
            for k, v in resp.headers.items()
            if k.lower() not in ("content-length", "transfer-encoding", "content-encoding", "connection")
        }
        return Response(content=resp.content, status_code=resp.status_code, headers=headers, media_type=resp.headers.get("content-type"))
