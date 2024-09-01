from fasthtml.common import *


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A("Toggle", hx_get=f"/toggle/{todo.id}", hx_target=f"#{tid}")
    delete = A("Delete", hx_delete=f"/{todo.id}", hx_target=f"#{tid}")
    return Li(toggle, todo.title + (" ✅" if todo.done else ""), delete, id=tid)


app, rt, todos, Todo = fast_app(
    db_file="todos.db", live=True, id=int, title=str, done=bool, pk="id", render=render
)


@rt("/")
def get():
    f = Form(
        Group(Input(placeholder="Add a new todo", name="title"), Button("Save")),
        hx_post="/",
        hx_target="#todo-list",
        hx_swap="beforeend",
    )
    return Titled("📝 Todo App", Card(Ul(*todos(), id="todo-list"), header=f))


@rt("/")
def post(todo: Todo):
    todos.insert(todo)


@rt("/{tid}")
def delete(tid: int):
    todos.delete(tid)


@rt("/toggle/{tid}")
def get(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo


serve()
