from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AddProjectForm,ImagesProject,AddProjectRate,CommentForm,ReportForm
from datetime import datetime
from .models import Project, Image, Comment
from . import models
from .utils import searchProjects


# Create your views here.

@login_required(login_url='login')
def AddProjects(request):
    context = {}
    form = {
        'AddProjectForm':AddProjectForm,
        'AddImages':ImagesProject
    }
    context['MODEL'] = form
    print(context)
    if (request.method == 'GET'):
        return render(request, 'projects/createProjects.html', context)
    else:
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_check = datetime.strptime(start_date, '%Y-%m-%d')
        end_check = datetime.strptime(end_date, '%Y-%m-%d')

        if start_check > end_check:
            messages.error(request, 'Invalid Start Date')
            return render(request, 'projects/createProjects.html', context)
        elif start_check.date() < datetime.today().date():
            messages.error(request, "The Start Date Can't Be Before Today")
            return render(request, 'projects/createProjects.html', context)
        else:
            form = AddProjectForm(request.POST,request.FILES)
            form2 =ImagesProject(request.POST,request.FILES)

            if (form.is_valid() and form2.is_valid()):
                print(request.POST)
                profile = request.user.profile

                ###### First Form #####################
                project = form.save(commit=False)
                project.owner = profile
                project.save()
                for v in request.POST.getlist('tags'):
                    project.tags.add(v)
                project_id = project.id
                print(project_id,'fff')
                print(request.FILES.getlist('image'))
                print(Image.id)

                ###### SEC Form #################

                imagesform = form2.save(commit=False)
                obje = Project.objects.get(id=project_id)
                imagesform.project = obje
                for img in request.FILES.getlist('image'):
                    Image.objects.create(project=obje,image=img)
                messages.success(request, 'Project Created Successfully')
                get_projects = Project.objects.get(id=project_id)
                get_projects_images = Image.objects.all().filter(project_id=project_id)
                project_data = {
                    'project_obj': get_projects,
                    'prject_img': get_projects_images
                }
                context['PROJECT'] = project_data
                return redirect('view-project', pk=project_id)
            else:
                print(request.POST)
                print('no')
                messages.error(request, 'Failed To Create Project')
                return render(request, 'projects/createProjects.html', context)
        context['MODEL'] = form
        return (request, 'projects/createProjects.html', context)



def ViewProject(request,pk):
    context = {}
    get_projects = Project.objects.get(id=pk)
    get_projects_images = Image.objects.all().filter(project_id=pk)
    get_comments = Comment.objects.all().filter(project_id=pk)
    form = ReportForm()
    project_data = {
        'project_obj': get_projects,
        'prject_img': get_projects_images,
        'project_rate': AddProjectRate,
        'project_comment': CommentForm,
        'project_comment_data': get_comments,
        'project_report_form': form,
    }
    context['PROJECT'] = project_data
    #########################################################
    # UPDATE AA
    # calc remaining amount of donations to be send with context instead of
    # making custom filters

    # determine current user vote on project( no vote, upvote, downvote )
    user_upvoted_proj = user_downvoted_proj = False
    if models.ProjectRate.objects.filter(user=request.user.profile, project=pk).exists():
        user_cur_vote = models.ProjectRate.objects.get(user=request.user.profile, project=pk)
        if user_cur_vote.is_upvote:
            user_upvoted_proj = True
        else:
            user_downvoted_proj = True
    context['rem_sum_required'] = get_projects.total_target - get_projects.collected_donations
    context['user_downvoted_proj'] = user_downvoted_proj
    context['user_upvoted_proj'] = user_upvoted_proj
    ########################################
    return render(request,'projects/viewProject.html',context)

@login_required(login_url='login')
def AddComment(request,pk):
    if (request.method == 'POST'):
        profile = request.user.profile
        project = Project.objects.get(id=pk)
        form = CommentForm(request.POST)
        if (form.is_valid()):
            comment = form.save(commit=False)
            comment.project = project
            comment.owner = profile
            comment.save()
            messages.success(request,'Comment Added')
            return redirect('view-project', pk=pk)
        else:
            messages.error(request,'Comment Faild')
            return HttpResponse('test')



def AllProjects(request):
    projects, search_query = searchProjects(request)
    top_five_projects = Project.objects.filter(is_deleted=False)[:5]
    latest_five_projects = Project.objects.filter(is_deleted=False).order_by('-created')[:5]
    featured_five_projects = Project.objects.filter(is_deleted=False,is_featured=True)[:5]
    return render(request,'projects/allProject.html',{'projects': projects,'search_query':search_query,'top':top_five_projects,'latest':latest_five_projects,'featured':featured_five_projects})



@login_required(login_url='login')
def DeleteProject(request,pk):
    project = Project.objects.get(id=pk)
    pro = project.collected_donations
    context = {}
    get_projects = Project.objects.get(id=pk)
    get_projects_images = Image.objects.all().filter(project_id=pk)
    project_data = {
        'project_obj': get_projects,
        'prject_img': get_projects_images
    }
    context['PROJECT'] = project_data
    allowed_value = project.total_target / 4
    if pro > allowed_value:
        messages.error(request, "Project Can't Be Deleted Because The Donation Amount Is Above 25%")
        return render(request,'projects/viewProject.html',context)
    else:
        Project.objects.filter(id=pk).update(is_deleted=True)
        messages.success(request, "Project Deleted")
        return redirect('all-projects')


########################################################################
@login_required
def donate(request, project_id):
    if request.method == 'POST':
        project = models.Project.objects.get(id=project_id)
        # It is NOT allowed that donations exceed project target
        donation = int(request.POST.get('user_donation'))
        rem_donations = project.total_target - project.collected_donations
        if donation > rem_donations and donation <= 0:
            messages.error(request,'you can not donate this amount!')
            return redirect(f'/projects/view-project/{project_id}' )
        else:
            project.collected_donations += donation
            project.save()
            request.session['last_donate'] = donation
            return redirect(f'/projects/view-project/{project_id}')


@login_required(login_url='login')
def AddReport(request,pk):
    project = Project.objects.get(id=pk)
    print(project)
    form = ReportForm()
    if (request.method=='POST'):
        form = ReportForm(request.POST)
        report = form.save(commit=False)
        report.project = project
        report.owner = request.user.profile
        report.save()
        messages.success(request,'Your report was successfully submitted!')
        return redirect('project', pk=project.id)
    return render(request, 'projects/viewProject.html', {'project': project, 'form': form})


@login_required
def update_rating(request, project_id):
    if request.method == 'POST':
        profile = request.user.profile
        project = models.Project.objects.get(id=project_id)
        user_voted_before = models.ProjectRate.objects.filter(user=profile.id, project=project.id).exists()
        # user_vote_on_project = 0 # just workaround to overcome 'local variable 'user_vote_on_project' referenced before assignment'
        user_vote_on_project = models.ProjectRate.objects.filter(user=profile.id, project=project.id).first()

        # check action type
        action_type = request.POST.get('action_type')
        if action_type == 'Vote Up':
            if not user_voted_before:  # no up
                models.ProjectRate.objects.create(is_upvote=True, user=profile, project=project)
                project.total_votes += 1
                project.total_upvotes += 1
            elif user_vote_on_project.is_upvote == False:  # down up
                project.total_upvotes += 1

                user_vote_on_project.is_upvote = True
                user_vote_on_project.save()

            else:  # up up -> back to
                models.ProjectRate.objects.filter(user=profile.id, project=project.id).delete()
                project.total_votes -= 1
                project.total_upvotes -= 1
        else:
            if not user_voted_before:  # no down
                models.ProjectRate.objects.create(is_upvote=False, user=profile, project=project)
                project.total_votes += 1
                # return HttpResponse('t++')
            elif user_vote_on_project.is_upvote == True:  # up down
                project.total_upvotes -= 1
                user_vote_on_project.is_upvote = False
                user_vote_on_project.save()
            else:  # down down -> back to no
                models.ProjectRate.objects.filter(user=profile.id, project=project.id).delete()
                project.total_votes -= 1
        project.save()
        return redirect(f'/projects/view-project/{project_id}')

