import uuid

class ResponseFormatter:
    @staticmethod
    def format_success_response(request_info, data, status=200):
        return {
            "ResponseInfo": {
                "apiId": request_info.get('apiId', 'birth-reg'),
                "ver": request_info.get('ver', '1.0'),
                "ts": int(uuid.uuid1().time),
                "resMsgId": str(uuid.uuid4()),
                "msgId": request_info.get('msgId', str(uuid.uuid4())),
                "status": "SUCCESS"
            },
            "BirthRegistrationApplications": data
        }

    @staticmethod
    def format_error_response(request_info, error_message, status=400):
        return {
            "ResponseInfo": {
                "apiId": request_info.get('apiId', 'birth-reg'),
                "ver": request_info.get('ver', '1.0'),
                "ts": int(uuid.uuid1().time),
                "resMsgId": str(uuid.uuid4()),
                "msgId": request_info.get('msgId', str(uuid.uuid4())),
                "status": "FAILED"
            },
            "error": str(error_message)
        } 