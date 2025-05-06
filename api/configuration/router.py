from dataclasses import dataclass

from handlers import database


@dataclass(frozen=True)
class Router:
    routers = [
        (database.router, "/api/database", ["database"])
    ]
