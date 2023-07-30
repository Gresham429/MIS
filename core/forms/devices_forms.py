from django import forms
from core.models.devices.models import Devices

def DevicesCreationForm():
    class DevicesForm(forms.ModelForm):
        # 重写 __init__ 方法，为可以为 null 的字段添加选填标记
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if Devices._meta.get_field(field_name).blank:
                    field.label += ' (选填)'

        class Meta:
            model = Devices
            fields = '__all__'

    return DevicesForm
