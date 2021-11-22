from app.routes import app
from app.plugins.dst_run.models import Players


@app.get('/plugins/dst-run/player-list',
         response_model=Players, tags=['dst-run'])
async def plugins():
    return Players()
