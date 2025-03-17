from typing import Any
from utility.logger import logger, log_func

class RespCommonResultCode:
    SUCCESS = "0000"
    FAILED = "0001"
    UNKNOWN_ERROR = "9999"


class RespCommonMsg:
    SUCESS = "SUCCESS"
    FAILED = "FAILED"
    UNKNOWN_ERROR = "UNKNOWN"

@log_func
def resp_spec(result: str, message: str, result_obj: Any):
    resp = {
        "Result": result,
        "Message": message,
        'ResultObject': result_obj
    }
    logger.info(resp)
    return resp
