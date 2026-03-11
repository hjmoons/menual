from mcp.server.fastmcp import FastMCP
from menual.mcp import commands, planner, excel

mcp = FastMCP("menual")

# 기능별 tools 등록
commands.register(mcp)
planner.register(mcp)
excel.register(mcp)
