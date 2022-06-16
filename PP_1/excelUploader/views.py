import os
import pytz
from django.contrib import messages
from django.shortcuts import render
from .models import ACS, Employee
import pandas as pd
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.core.files.storage import default_storage


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
                try:
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

                    read_file = pd.read_excel(f)
                    report_date = str(read_file.iloc[0])
                    name_split = report_date.split("   ", 1)
                    name_replace = name_split[0].replace(":", "")
                    dir_path = os.getcwd()
                    check_name = "%s.xlsx" % (name_replace)
                    old_name = '%s\media' % (str(dir_path))
                    for i in os.walk(old_name):
                        if check_name in i[2]:
                            print("Duplicate")
                        else:
                            document = default_storage.save(f.name, f)
                            dir_path = os.getcwd()
                            old_name = '%s\media\%s' % (str(dir_path), str(f))
                            new_name = '%s\media\%s.xlsx' % (str(dir_path), name_replace)
                            os.rename(old_name, new_name)

                except ValueError:
                    messages.error(request,
                                   "В файле %s не найдены колонки: Сотрудник, Фирма, Дата и Время, Направление, Дверь!" % (
                                       str(f)))


            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        return render(request, 'index.html')

