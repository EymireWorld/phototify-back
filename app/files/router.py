from fastapi import APIRouter, HTTPException, UploadFile, status

from app.files import services


router = APIRouter(
    prefix= '/files',
    tags= ['Files']
)


@router.get('/{file_name}')
def get_file(
    file_name: str
):
    return services.get_file(file_name)


@router.post('')
async def add_file(
    file: UploadFile
):
    return {'file': await services.add_file(file)}
