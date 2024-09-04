from typing import Optional

from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(
            self, status_code: int = 500,
            detail: Optional[str] = None,
            data=None
    ):
        detail_structure = {
            'status': 'error',
            'data': data,
            'detail': detail
        }
        super().__init__(status_code=status_code, detail=detail_structure)


class UserNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User not fount')


class EmailAlreadyRegisteredException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Email already registered')


class InvalidDataException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Invalid data')


class InvalidInviteTokenException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Invalid invite token')


class AccountAlreadyExistsException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Account already exists')


class BadTokenException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Bad token')


class TaskNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Task not found')


class ParentDepartmentNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail='Parent department not found'
        )


class RootDepartmentNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='Root department not found'
        )


class DepartmentNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail='Department not found'
        )


class PositionNotFoundException(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail='Position not found'
        )
