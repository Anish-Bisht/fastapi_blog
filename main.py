from contextlib import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError

from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse ## This is used to specify that the response from the endpoint should be returned as HTML. By default, FastAPI returns responses in JSON format, but you can specify a different response class to return other types of responses, such as HTML, plain text, or even custom response classes.
from fastapi.templating import Jinja2Templates ## This is used to render HTML templates using the Jinja2 templating engine. It allows you to create dynamic HTML pages by passing data to the templates and rendering them with the provided data.
from starlette.exceptions import HTTPException as StarletteHTTPException ## This is used to handle HTTP exceptions that may occur during the processing of requests. It allows you to catch and handle specific HTTP errors, such as 404 Not Found or 500 Internal Server Error, and return custom responses or error pages.    
from typing import Annotated 
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
import models
from database import Base, engine, get_db
from sqlalchemy.orm import selectinload

from routers import posts, users
from config import settings




# Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan= lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name = "media")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])  








# @app.get("/", response_class=HTMLResponse, include_in_schema=False) # include_in_schema=False means that this endpoint will not be included in the OpenAPI schema and will not be documented in the API docs.
# @app.get("/posts", response_class=HTMLResponse) # This means that the response will be returned as HTML instead of JSON. By default, FastAPI returns responses in JSON format, but you can specify a different response class to return other types of responses, such as HTML, plain text, or even custom response classes.
# def home():
#     return f"<h1>{posts[0]['title']}</h1><p>{posts[0]['content']}</p></h1>"

@app.get("/",include_in_schema=False, name= "home")
@app.get("/posts", include_in_schema=False, name= "posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
   
    count_result = await db.execute(select(func.count()).select_from(models.Post))
    total = count_result.scalar() or 0
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).order_by(models.Post.date_posted.desc()).limit(settings.post_per_page))
    posts = result.scalars().all()
    has_more = len(posts)< total
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home", "limit": settings.post_per_page, "has_more": has_more})


@app.get("/users/{user_id}/posts", include_in_schema=False, name = "user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found",
        )
    count_result = await db.execute(select(func.count()).select_from(models.Post).where(models.Post.user_id == user_id))
    total = count_result.scalar() or 0
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.user_id== user_id).order_by(models.Post.date_posted.desc()).limit(settings.post_per_page))
    posts = result.scalars().all()
    has_more = len(posts)< total
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts", "limit": settings.post_per_page, "has_more": has_more}
    )


    

@app.get("/posts/{post_id}", include_in_schema=False, )
async def post_page(request :Request
             ,post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,"post.html",{
                "post":post, "title": title
            },
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@app.get("/account", include_in_schema=False)
async def account_page(request:Request):
    return  templates.TemplateResponse(
        request,
        "account.html",
        {"title": "Account"}
    )



@app.get("/login", include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"title": "Login"}
    )
@app.get("/register", include_in_schema=False)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"title": "Register"}
    )


@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
   
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)
        # return JSONResponse(
        #     status_code = exception.status_code,
        #     content = {"detail": message}
        # )
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code = exception.status_code
    )




@app.exception_handler(RequestValidationError)
async def validation_exception_handle(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception) 
        # return JSONResponse(
        #     status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        #     content = {"detail": exception.errors()},
        # )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    )


    