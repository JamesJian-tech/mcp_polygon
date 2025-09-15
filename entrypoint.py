#!/usr/bin/env python
import os
import sys
import argparse
from typing import Literal

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_polygon import server


def transport() -> Literal["stdio", "sse", "streamable-http"]:
    """
    Determine the transport type for the MCP server.
    Defaults to 'stdio' if not set in environment variables.
    """
    mcp_transport_str = os.environ.get("MCP_TRANSPORT", "stdio")

    # These are currently the only supported transports
    supported_transports: dict[str, Literal["stdio", "sse", "streamable-http"]] = {
        "stdio": "stdio",
        "sse": "sse",
        "streamable-http": "streamable-http",
    }

    return supported_transports.get(mcp_transport_str, "stdio")


def parse_transport_arg(transport_arg: str) -> Literal["stdio", "sse", "streamable-http"]:
    """
    Parse and validate transport argument from command line.
    """
    supported_transports: dict[str, Literal["stdio", "sse", "streamable-http"]] = {
        "stdio": "stdio",
        "sse": "sse",
        "streamable-http": "streamable-http",
    }
    
    return supported_transports.get(transport_arg, "stdio")


# Ensure the server process doesn't exit immediately when run as an MCP server
def start_server():
    parser = argparse.ArgumentParser(description="Start Polygon MCP Server")
    parser.add_argument(
        "--transport", 
        type=str, 
        default="stdio",
        choices=["stdio", "sse", "streamable-http"],
        help="Transport type for MCP server (default: stdio)"
    )
    
    args = parser.parse_args()
    
    polygon_api_key = os.environ.get("POLYGON_API_KEY", "")
    if not polygon_api_key:
        print("Warning: POLYGON_API_KEY environment variable not set.")
    else:
        print("Starting Polygon MCP server with API key configured.")
    
    # Use command line transport argument if provided, otherwise fall back to environment variable
    transport_type = parse_transport_arg(args.transport)
    
    server.run(transport=transport_type)


if __name__ == "__main__":
    start_server()
