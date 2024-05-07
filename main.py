import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from starlette.staticfiles import StaticFiles

from handlers import other_handlers, user_handlers, tasks_handlers, form_handlers
from keyboards.main_menu import set_main_menu
import utils
import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import uvicorn
from app.get_data_service import get_results
import json
from fastapi.templating import Jinja2Templates
from stats import get_stats, buf
import base64
from login import get_current_username
from fastapi import Depends
from typing import Annotated
from settings import bot
import starlette.status as status


logger = logging.getLogger(__name__)


templates = Jinja2Templates(directory="templates")


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/results/", response_class=HTMLResponse)
async def results(request: Request):
    data = await get_results()
    data = json.dumps(data)
    await get_stats()
    buf.seek(0)
    line = (str(base64.b64encode(buf.getvalue())).replace('\'', ''))[1:]
    return templates.TemplateResponse("basic.html",
                                      {
                                              "request": request,
                                              "variable": data,
                                              "b64string": line,
                                              "username": "User"
                                      }
                                      )


@app.post("/results/login")
async def process_login():
    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_303_SEE_OTHER)


@app.get("/admin", response_class=HTMLResponse)
async def process_admin(username: Annotated[str, Depends(get_current_username)], request: Request):
    data = await get_results()
    data = json.dumps(data)
    await get_stats()
    buf.seek(0)
    line = (str(base64.b64encode(buf.getvalue())).replace('\'', ''))[1:]
    return templates.TemplateResponse("index.html",
                                      {
                                              "request": request,
                                              "variable": data,
                                              "b64string": line,
                                              "username": username
                                      }
                                      )


@app.post("/tguser/")
async def process_user(request: Request):
    user = await request.json()
    data = json.dumps(await utils.merge_to_report(user['name'], mode=True))
    return JSONResponse(content=data)


@app.post("/publication/")
async def process_publication(request: Request):
    data = await request.json()
    if data['publication']:
        await utils.send_publication(data['publication'])
        return json.dumps([{"response": "Success"}])
    return json.dumps([{"response": "Failed"}])


@app.get("/")
async def root():
    return {"message": "hello"}



async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Инициализируем Redis
    storage = MemoryStorage()

    dp: Dispatcher = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(form_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(tasks_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    uvicorn.run(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    asyncio.run(main())
