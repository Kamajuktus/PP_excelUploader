import os

import pytz
from django.shortcuts import render
from .models import ACS, Employee
import pandas as pd
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from .models import UploadExcel


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
                dbframe = empexceldata
                dbframe = dbframe.sort_values(by=['Дата и Время'])
                list_of_employee = []
                list_of_ids = []
                for dbframe_employee in dbframe.itertuples():
                    obj, created = Employee.objects.get_or_create(employee_name=dbframe_employee[1])
                    obj_id = obj.id
                    obj.save()

                    employees = str(Employee.objects.get(pk=obj_id))

                    list_of_employee.append(employees)
                    list_of_ids.append(obj_id)

                zip_emp = zip(list_of_employee, list_of_ids)
                dict_emp = dict(zip_emp)

                for dbframe_acs in dbframe.itertuples():
                    local_timezone = pytz.timezone('Etc/Gmt-6')
                    date_zero = local_timezone.localize(dbframe_acs[3]) - local_timezone.utcoffset(
                        dbframe_acs[3])

                    if dict_emp.get(dbframe_acs[1]) != None:
                        obj, created = ACS.objects.get_or_create(employee_id=dict_emp.get(dbframe_acs[1]),
                                                                 company=dbframe_acs[2],
                                                                 datetime=date_zero,
                                                                 direction=dbframe_acs[4], door=dbframe_acs[5])

                        obj.save()
               

                read_file = pd.read_excel(f, usecols='A', nrows=1)
                name = read_file
                print(str(read_file))

                document = default_storage.save(f.name, f)
                dir_path = os.getcwd()
                kek = 'wow.xlsx'

                path = '%s\media\%s' % (str(dir_path), str(f))
                path2 = '%s\media\%s.xlsx' % (str(dir_path), name)
                print(f)
                print(path)

                # os.rename(path, path2)


            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        return render(request, 'index.html')
