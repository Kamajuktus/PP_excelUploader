import pytz
from django.shortcuts import render
from .models import ACS, Employee
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import FileFieldForm


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'index.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                empexceldata = pd.read_excel(f,
                                             usecols=['Сотрудник', 'Фирма', 'Дата и Время', 'Направление', 'Дверь'],
                                             skiprows=3)
                print(type(empexceldata))
                dbframe = empexceldata
                dbframe = dbframe.sort_values(by=['Дата и Время'])
                list1 = []

                list2 = []
                for dbframe_employee in dbframe.itertuples():
                    if not Employee.objects.filter(employee_name=dbframe_employee[1]).exists():
                        obj = Employee.objects.create(employee_name=dbframe_employee[1])
                        obj_id = obj.id
                        # print(obj_id)
                        obj.save()

                        wow = str(Employee.objects.get(pk=obj_id))

                        list1.append(wow)
                        list2.append(obj_id)

                    else:
                        wow = str(Employee.objects.get(pk=obj_id))
                        list1.append(wow)
                        pass

                kek = zip(list1, list2)
                d = dict(kek)

                for dbframe_acs in dbframe.itertuples():
                    local_timezone = pytz.timezone('Etc/Gmt-6')
                    date_zero = local_timezone.localize(dbframe_acs[3]) - local_timezone.utcoffset(
                        dbframe_acs[3])

                    if d.get(dbframe_acs[1]) != None:
                        obj = ACS.objects.create(employee_id=d.get(dbframe_acs[1]), company=dbframe_acs[2],
                                                 datetime=date_zero,
                                                 direction=dbframe_acs[4], door=dbframe_acs[5])

                        obj.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        return render(request, 'index.html')