from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from reportapp.models import Report, Comment
from .forms import ReportCreateForm, ReportSearchForm, ReportCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
@login_required
def index(request):
    return render(request, "reportapp/top.html")

class ReportCreate(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['content', 'comment']
    success_url = reverse_lazy('reportapp:report_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ReportList(LoginRequiredMixin, ListView):
    model = Report
    def get_queryset(self):
        data = self.request.GET.get("data")
        author = self.request.GET.get("author")
        qs = Report.objects.all()
        if data:
            qs = qs.filter(data=data)
        if author:
            qs = qs.filter(author=author)
        
        order = self.request.GET.get('order')
        if order == 'new':
            qs = qs.order_by('-created_at')
        elif order == 'like':
            qs = qs.annotate(like_count=Count('likes')).order_by('-like_count')
        else:
            qs = qs.order_by('created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportSearchForm(self.request.GET or None)
        return context

class ReportDetail(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reportapp/report_detail.html'

class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'reportapp/user_list.html'

class UserReportList(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reportapp/user_report_list.html'
    
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Report.objects.filter(author=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_obj"] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author and not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class ReportUpdate(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Report
    fields = ['content', 'comment']
    success_url = reverse_lazy('reportapp:report_list')

class ReportDelete(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('reportapp:report_list')

@login_required
def like_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    liked = False
    if request.user in report.likes.all():
        report.likes.remove(request.user)
    else:
        report.likes.add(request.user)
        liked = True
    
    context = {
        'liked': liked,
        'like_count': report.likes.count()
    }
    return JsonResponse(context)

@login_required
def comment_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.report = report
            comment.author = request.user
            comment.save()
            return redirect('reportapp:report_detail', pk=report.pk)
    else:
        form = ReportCommentForm()
    return render(request, 'reportapp/report_comment.html', {'form': form, 'report': report})
    