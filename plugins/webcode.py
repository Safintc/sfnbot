from aiohttp import web as webserver

# -------------------- Routes --------------------
routes = webserver.RouteTableDef()

# -------------------- Web App --------------------
async def bot_run():
    """
    Returns an aiohttp Application for the bot's web server.
    Used to keep the Replit instance alive via UptimeRobot.
    """
    _app = webserver.Application(client_max_size=30_000_000)
    _app.add_routes(routes)
    return _app

# -------------------- Root Route --------------------
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """
    Handles GET requests to the root URL.
    Returns a simple JSON message for UptimeRobot.
    """
    return webserver.json_response({
        "status": "online",
        "message": "Safin SfnBot Web Supported! This is a preview of Web."
    })
