from typing import BinaryIO, List
from fastapi import BackgroundTasks, FastAPI, Request, UploadFile, File, Form
import shutil
import os
import asyncio

# from bs4 import BeautifulSoup

# filename = "example.html"
# try:
#     soup = BeautifulSoup("<!docktype html><html></html>", "html.parser")
#     print("This is an HTML file")
# except Exception:
#     print("Not an HTML file")


app = FastAPI()
MAX_FILE_SIZE = 5 * 1024 * 1024
TMP_FOLDER = "tmp"
try:
    os.mkdir(TMP_FOLDER)
except FileExistsError as e:
    print(e)


async def save_file(file_path: str, file: bytes):
    await asyncio.sleep(1)
    with open(file_path, "wb") as buffer:
        buffer.write(file)
        # shutil.copyfileobj(file, buffer)


@app.post("/upload-image/")
async def upload_image(
    background_tasks: BackgroundTasks,
    request: Request,
    files: List[UploadFile] = [],
):  # File(...)):
    folder = f"{TMP_FOLDER}/{id(request)}"
    os.mkdir(folder)

    mimes = []
    filenames = []

    for file in files:
        # 15 MB
        # 1 MB ~ 1024 KB
        # 1 KB ~ 1024 B
        if (
            file.content_type in ["application/json", "text/html"]
            and file.size < MAX_FILE_SIZE
        ):
            filenames.append(f"{file.filename} {file.size} bytes")  # .file.__sizeof__()
            mimes.append(file.content_type)
            background_tasks.add_task(
                save_file,
                file_path=f"{folder}/{file.filename}",
                file=file.file.read(),
            )

    return {
        "filenames": filenames,
        "mimes": mimes,
        "id": id(request),
    }
