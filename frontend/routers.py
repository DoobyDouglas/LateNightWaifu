from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from api.routers import get_anime_list, get_anime, search_anime


FRONTEND_ROUTER = APIRouter(tags=['frontend'])

templates = Jinja2Templates(directory='templates/')


@FRONTEND_ROUTER.get('/')
async def main_page(request: Request, anime_list=Depends(get_anime_list)):
    context = {
        'request': request,
        'anime_list': anime_list,
    }
    return templates.TemplateResponse('main.html', context)


@FRONTEND_ROUTER.get('/anime/{anime_id}')
async def anime_page(request: Request, anime_id: int):
    anime = await get_anime(anime_id)
    context = {
        'request': request,
        'anime': anime,
    }
    return templates.TemplateResponse('anime/anime_page.html', context)


@FRONTEND_ROUTER.get('/search/{query}')
async def search(request: Request, query: str):
    anime_list = await search_anime(query)
    context = {
        'request': request,
        'anime_list': anime_list,
    }
    return templates.TemplateResponse('main.html', context)
