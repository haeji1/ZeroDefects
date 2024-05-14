from fastapi.params import Param


class CustomParams(Param):
    size: int = 5