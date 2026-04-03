from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session


app = FastAPI()
app.mount("/assets",StaticFiles(directory="assets"), name="assets")


engine = create_engine(
    "sqlite:///mydb.db",
    connect_args={"check_same_thread":False},
    pool_size=5)

session_local = sessionmaker(bind=engine)


def getDb():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def main(db:Session = Depends(getDb)):

    get_data= db.execute(text("Select * from MyTable"))



    tableLoop = [f"<tr><td>{a.IdBook}</td><td>{a.BookName}</td><td>{a.Writter}</td></tr>" for a in get_data]
    return f"""
    <html>
        <head>
            <title>Task 1, retreive data from simple Database</title>
            <link href="assets/bootstrap-5.3.8-dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="assets/bootstrap-5.3.8-dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body>
            <div class="container mt-5 shadow p-3">

            <h2 class="mb-2">Task 1, retreive data from simple Database</h2>
            <table class="table">
            <thead>
            <tr><th>Book Id</th><th>Book Name</th><th>Writter</th></tr>
            </thead>
            {"".join(tableLoop)}
            </table>

            </div>
        </body>
    </html>
    """