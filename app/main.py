from importlib import import_module
import uvicorn


import_module('app.plugins.dst_run.routes')


if __name__ == '__main__':
    uvicorn.run('app.routes:app',
                host='0.0.0.0',
                port=12599,
                reload=True)

