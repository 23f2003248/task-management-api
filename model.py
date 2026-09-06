import sqlite3

# @app.get("/task/all")
# def get_task_all():
#     data = load_data()
#     res=[]
#     if not tasks:
#         raise HTTPException(status_code=404, detail="No tasks found")
#     for task in tasks:
#         res.append(
#             {
#             "title": task.title,
#             "status": task.status
#             }
#         )
#     return(res)