from neutronstar import app
from neutronstar.routes.plugins.dst_run.models import Players


@app.get('/plugins/dst-run/player-list', response_model=Players, tags=['dst-run'])
async def plugins():
    return Players()
