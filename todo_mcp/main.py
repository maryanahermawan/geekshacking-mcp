from fastmcp import FastMCP
from typing import Annotated, NamedTuple
from todo_db import TodoDB

mcp = FastMCP('todo-mcp')
todo_db = TodoDB()
# todo_db.sample_data()

@mcp.tool(name = "tool_add_todo", description = "Add a single #TODO text from a source file")
def add_todo(
  filename: Annotated[str, "The source code filename where the #TODO is located"],
  text: Annotated[str, "The #TODO text content"],
  line_num: Annotated[int, "The line number of #TODO in the filename"]) -> bool:
  return todo_db.add(filename, text, line_num)

# Todo Class
class Todo(NamedTuple):
  filename: Annotated[str, "The source code filename where the #TODO is located"]
  text: Annotated[str, "The #TODO text content"]
  line_num: Annotated[int, "The line number of #TODO in the filename"]

  
@mcp.tool(name = "tool_add_all_todos_in_file", description = "Add all #TODO text from a source file")
def add_all_todos_in_file(
  todos: list[Todo]) -> int:
  for todo in todos:
    todo_db.add(todo.filename, todo.text, todo.line_num)
  return len(todos)

# Resource
@mcp.resource(name = "resource_get_todos_for_file",
              description = "Get all #TODOs for a source file",
              uri="todo://{filename}/todos")
def get_todos_for_file(
  filename: Annotated[str, "The source code filename to get #TODOs from"]) -> list[str]:
  todos = todo_db.get(filename)
  return [text for text in todos.values()]

def main():
  mcp.run()

if __name__ == "__main__":
  main()


