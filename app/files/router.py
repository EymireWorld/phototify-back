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
    if file.content_type not in ('image/jpeg', 'image/png', 'video/mp4'):
        raise HTTPException(
            status_code= status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail= 'Use .jpg/.jpeg/.png/.mp4 file.'
        )
    
    return {'file': await services.add_file(file)}
