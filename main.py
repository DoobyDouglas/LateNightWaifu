import uvicorn
# в разарботке убрать хост и порт
if __name__ == '__main__':
    uvicorn.run(
        'api.app:LATE_NIGHT_WAIFU',
        host='web',
        port=8000,
        reload=True
    )
