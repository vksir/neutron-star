from app import app
from app.routes.plugins.dst_run.models import Players


@app.get('/plugins/dst-run/player-list', response_model=Players, tags=['dst-run'])
async def plugins():
    return Players()
