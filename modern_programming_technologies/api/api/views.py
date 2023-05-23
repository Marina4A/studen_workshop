from rest_framework import generics
from modern_programming_technologies.api.api.serializers import RepairJobSerializer
from django.shortcuts import render, redirect
from .models import RepairJob
from .forms import RepairJobForm


class RepairJobList(generics.ListCreateAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer


class RepairJobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer


def repair_jobs(request):
    # Получаем все объекты модели RepairJob из базы данных
    repair_jobs = RepairJob.objects.all()

    # Создаем словарь с переменными контекста
    context = {
        'repair_jobs': repair_jobs,
    }

    # Возвращаем ответ HTTP-запроса, используя шаблон 'repair_jobs.html'
    return render(request, 'repair_jobs.html', context)


def repair_job_create(request):
    if request.method == 'POST':
        # Создаем экземпляр формы и заполняем его данными из запроса
        form = RepairJobForm(request.POST)

        # Если отправленная форма действительна, то сохраняем объект в базе данных
        if form.is_valid():
            form.save()

            # Перенаправляем пользователя на страницу со списком ремонтных работ
            return redirect('repair_jobs')
    else:
        # Если GET-запрос, то создаем пустой экземпляр формы
        form = RepairJobForm()

    # Создаем словарь с переменными контекста
    context = {
        'form': form,
    }

    # Возвращаем ответ HTTP-запроса, используя шаблон 'repair_job_create.html'
    return render(request, 'repair_job_create.html', context)
