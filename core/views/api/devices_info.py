from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from core.models.devices.models import Devices
from urllib.parse import unquote
    


@login_required(login_url='sign_in')
def get_devices_list(request):
    devices :Devices = Devices.objects.values('name', 'model').annotate(total_quantity=Count('name'))

    data_list = [
        {
            'name': device['name'],
            'model': device['model'],
            'total_quantity': device['total_quantity'],
        }
        for device in devices
    ]

    return JsonResponse(data_list, safe=False)

def get_devices_info(request, device_name, device_model):
    try:
        # 解码设备型号
        device_name = unquote(device_name)
        device_model = unquote(device_model)


        # 查询设备名称为device_name、设备型号为device_model的所有数据
        devices = Devices.objects.filter(name=device_name, model=device_model)

        # 构建弹窗内容
        PopUpContent = ''
        for device in devices:
            PopUpContent += (
                '<p><strong>物资类别：</strong>' + (device.category or '') + '</p>' +
                '<p><strong>固定资产编号：</strong>' + (device.fixed_asset_number or '') + '</p>' +
                '<p><strong>物资名称：</strong>' + (device.name or '') + '</p>' +
                '<p><strong>型号：</strong>' + (device.model or '') + '</p>' +
                '<p><strong>生产/出厂日期：</strong>' + (str(device.production_date) if device.production_date else '') + '</p>' +
                '<p><strong>发票号码：</strong>' + (device.invoice_number if device.invoice_number else '') + '</p>' +
                '<p><strong>单价：</strong>' + (str(device.unit_price) if device.unit_price else '') + '</p>' +
                '<p><strong>数量：</strong>' + (str(device.quantity) if device.quantity else '') + '</p>' +
                '<p><strong>价格：</strong>' + (str(device.total_price) if device.total_price else '') + '</p>' +
                '<p><strong>采购日期：</strong>' + (str(device.purchase_date) if device.purchase_date else '') + '</p>' +
                '<p><strong>采购人：</strong>' + (device.purchaser if device.purchaser else '') + '</p>' +
                '<p><strong>采购人电话：</strong>' + (device.purchaser_phone if device.purchaser_phone else '') + '</p>' +
                '<p><strong>领用团队：</strong>' + (device.team or '') + '</p>' +
                '<p><strong>领用人：</strong>' + (device.recipient if device.recipient else '') + '</p>' +
                '<p><strong>领用人电话：</strong>' + (device.recipient_phone if device.recipient_phone else '') + '</p>' +
                '<p><strong>存放地点：</strong>' + (device.storage_location or '') + '</p>' +
                '<p><strong>责任人：</strong>' + (device.responsible_person or '') + '</p>' +
                '<p><strong>当前状态：</strong>' + (device.current_status or '') + '</p>' +
                '<hr>'  # 添加分隔线，区分不同设备信息
            )

        # 返回 JSON 格式的数据
        return JsonResponse({'popupContent': PopUpContent})

    except Exception as e:
        # 出现异常时返回错误信息
        return JsonResponse({'error': str(e)})
