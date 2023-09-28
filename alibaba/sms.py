#sdk写法
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_sms_code(mobile, sms_code):

    client = AcsClient('', '', '')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', "MIS")
    request.add_query_param('TemplateCode', "SMS_462475333")
    request.add_query_param('TemplateParam', {'code': sms_code})
    response = client.do_action_with_exception(request)
    return response

