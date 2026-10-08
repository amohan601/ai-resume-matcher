from fastmcp import FastMCP
from . import storage as db
from schema import Application
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr,   # explicit, never stdout
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("resume-matcher-mcp")

mcp = FastMCP("Resume matcher MCP Server")

mcp_app = mcp.http_app(path="/", stateless_http=True)


@mcp.tool
def add_application(application: Application) -> Application:
    """Add a new job application to the system."""
    logger.info("add_application called with %s", application.model_dump())
    return db.create_application(
        application=application
    )

@mcp.tool
def list_applications() -> list[Application]:
    """List all job applications."""
    return db.list_all_applications()


if __name__ == "__main__":
    mcp.run()
