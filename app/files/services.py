import os
from datetime import datetime
from hashlib import sha256

import aiofiles
from fastapi import UploadFile
from fastapi.responses import FileResponse


def get_file(file_name: str):
    return FileResponse(os.path.join('uploads', file_name))


async def add_file(file: UploadFile):
    file_name, file_extension = os.path.splitext(file.filename)
    file_name = file_name + '^' + datetime.utcnow().strftime('%d.%m.%Y,%H:%M:%S')
    file_name = sha256(file_name.encode()).hexdigest()
    file_path = os.path.join('uploads', file_name + file_extension)
    
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024 * 32):
            await f.write(chunk)

    return file_name + file_extension
