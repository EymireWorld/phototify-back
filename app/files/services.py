import os
from datetime import datetime
from hashlib import sha256

import aiofiles
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse


def get_file(file_name: str):
    if file_name not in os.listdir('uploads'):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= 'File not found.'
        )
    
    return FileResponse(os.path.join('uploads', file_name))


async def add_file(file: UploadFile):
    if file.content_type not in ('image/jpeg', 'image/png', 'video/mp4'):
        raise HTTPException(
            status_code= status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail= 'Use .jpg/.jpeg/.png/.mp4 file.'
        )
    if file.size > 1024 * 1024 * 32:
        raise HTTPException(
            status_code= status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail= 'Max file size is 32MB.'
        )
    
    file_name, file_extension = os.path.splitext(file.filename)
    file_name = file_name + '^' + datetime.utcnow().strftime('%d.%m.%Y,%H:%M:%S')
    file_name = sha256(file_name.encode()).hexdigest()
    file_path = os.path.join('uploads', file_name + file_extension)
    
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024 * 4):
            await f.write(chunk)

    return file_name + file_extension
