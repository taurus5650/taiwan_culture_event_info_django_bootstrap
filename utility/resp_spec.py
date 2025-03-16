from typing import Any


class RespCommonResultCode:
    SUCCESS = "0000"
    FAILED = "0001"
    UNKNOWN_ERROR = "9999"


class RespCommonMsg:
    SUCESS = "SUCCESS"
    FAILED = "FAILED"
    UNKNOWN_ERROR = "UNKNOWN"


def resp_spec(result: str, message: str, result_obj: Any):
    resp = {
        "Result": result,
        "Message": message,
        'ResultObject': result_obj
    }
    print(resp)
    return resp
