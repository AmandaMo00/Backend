
from django.shortcuts import render
from	django.http	import	Http404, HttpResponse
from django.template import loader

from jobs.models import Cities, Job, JobTypes

# Create your views here.

# def	hello(request):
#     return	HttpResponse("Hello	world")


# end def
def joblist(request):
    job_list = Job.objects.order_by('job_type')
    context =  {'job_list': job_list}
    for job in job_list:
        job.city_name = Cities[job.job_city][1]


        if job.job_type >= 0 and job.job_type < len(JobTypes):# 出错是因为两个职位不是【1】的index位置的职位类型
            job.type_name = JobTypes[job.job_type][1]
        else:
            print(f"Error: job_type {job.job_type} is out of range.")
        # job.type_name = JobTypes[job.job_type][1]
    return render(request, 'joblist.html', context)


def detail(request, job_id): # 职位详情页
    try:
        job =  Job.objects.get(pk = job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job	does    not	exist")
    return render(request, "job.html", {'job':job})