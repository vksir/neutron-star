import uvicorn
import platform


if __name__ == '__main__':
    host = '0.0.0.0' if platform.system() == 'Linux' else '127.0.0.1'
    uvicorn.run('app:app',
                host=host,
                port=12599,
                reload=True)

