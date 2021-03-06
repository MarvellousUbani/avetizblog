# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import advertForm, UserForm, ProfileForm
from .models import Advert, Transaction, Wallet, Report
from blog.models import Post, Comment
from .forms import  PostForm, TransactionForm, reportForm
from account.models import Profile
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
import random, string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
import pdb

# Create your views here
class Dashboard(LoginRequiredMixin, View):
	login_url='account/login'

	def get(self,request, *args, **kwargs):
		comment_count=Comment.objects.filter(post__author=self.request.user).count()
		draft_count=Post.objects.filter(Q(status__icontains='draft'), author=self.request.user).count()
		amount=Wallet.objects.get(Owner=self.request.user).amount
		published_count=Post.objects.filter(status__icontains='publish').filter(author=self.request.user).count()
		submitted_count=Post.objects.filter(status__icontains='submit').filter(author=self.request.user).count()
		monthdis=monthCount(self.request.user, n=[])
		#pdb.set_trace()
		context={
		'comment_count':comment_count,
		'draft_count':draft_count,
		'amount':amount,	
		'published_count':published_count,
		'submitted_count':submitted_count,
		'monthdis':monthdis,
		}
		return render(self.request, 'advert/dashboard.html', context)
		

class postList(LoginRequiredMixin, ListView):
	model=Post
	template_name='advert/post_list.html'
	login_url='account/login'
	context_object_name='posts'
	paginate_by=10
	def get_queryset(self):
		return Post.objects.filter(author=self.request.user).order_by('-published_date').order_by('-created_date')

class AdvertListView(LoginRequiredMixin,ListView):
	model=Advert
	template_name='advert/advert.html'
	login_url='account/login'
	context_object_name='adverts'

	def get_queryset(self):
		return Advert.objects.filter(publisher=self.request.user)


class AjaxableResponseMixin(object):
	partial_file=None
	partial_success_file=None

	def form_invalid(self, form):
		return HttpResponseRedirect(reverse('advert:post_list'))
        
	def form_valid(self,form):
		post=form.save(commit=False)
		post.author=self.request.user
		post.save()
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		dic['form_is_valid']=True
		dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		return HttpResponseRedirect(reverse('advert:post_list'))
		

	def render_to_json_response(self, data):
		return JsonResponse(data)


class createPost(LoginRequiredMixin,AjaxableResponseMixin, CreateView):
	model=Post
	form_class=PostForm
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	partial_file='advert/includes/partial_post_create.html'

	def get(self,request, *args, **kwargs):
		form=PostForm()
		data={'form':form}
		dic = dict()
		dic['html_form'] = render_to_string(self.partial_file, data, request=self.request)
		return self.render_to_json_response(dic)
	

class createAdvert(LoginRequiredMixin,AjaxableResponseMixin, CreateView):
	model=Post
	form_class=advertForm
	login_url='account/login'
	partial_success_file='advert/includes/partial_advert_list.html'
	partial_file='advert/includes/partial_advert_create.html'

	def get(self,request, *args, **kwargs):
		form=advertForm()
		data={'form':form}
		dic = dict()
		dic['html_form'] = render_to_string(self.partial_file, data, request=self.request)
		return self.render_to_json_response(dic)

	def form_valid(self,form):
		advert=form.save(commit=False)
		advert.setUp(self.request.user)
		advert.save()
		dic=dict()
		data=Advert.objects.filter(publisher=self.request.user)
		context={'adverts':data}
		#dic['form_is_valid']=True
		#dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		#return JsonResponse(dic)
		return HttpResponseRedirect(reverse('advert:advert_list'))

class createReport(LoginRequiredMixin,AjaxableResponseMixin, CreateView):
	model=Report
	form_class=reportForm
	login_url='account/login'
	partial_success_file='advert/includes/partial_report_list.html'
	partial_file='advert/includes/partial_report_create.html'

	def get(self,request, *args, **kwargs):
		form=reportForm()
		data={'form':form}
		dic = dict()
		dic['html_form'] = render_to_string(self.partial_file, data, request=self.request)
		return self.render_to_json_response(dic)

	def form_valid(self,form):
		report=form.save(commit=False)
		report.setUp(self.request.user)
		return HttpResponseRedirect(reverse('advert:report'))		


class postUpdate(LoginRequiredMixin, UpdateView):
	model=Post
	context_object_name = 'post'
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	partial_file='advert/includes/partial_post_update.html'

	def get(self, request, *args,**kwargs):
		dic=dict()
		self.object=self.get_object()
		form=PostForm(instance=self.object)
		data={'form':form, 'post':self.object}
		dic['html_form']=render_to_string(self.partial_file, data, request=self.request)
		return JsonResponse(dic)


	def post(self,request, *args, **kwargs):
		dic=dict()
		self.object=self.get_object()
		form=PostForm(instance=self.object, data=request.POST, files=request.FILES)
		form.save()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		dic['form_is_valid']=True
		dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		#return JsonResponse(dic)
		return HttpResponseRedirect(reverse('advert:post_list'))


class PostDeleteView(LoginRequiredMixin,DeleteView):
	model=Post
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'post': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_post_delete.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		self.object=self.get_object()
		self.object.delete()
		dic['form_is_valid']=True
		dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		return HttpResponseRedirect(reverse('advert:post_list'))


class ReportEyeView(LoginRequiredMixin,DetailView):
	model=Report
	login_url='account/login'
	partial_success_file='advert/includes/partial_report_list.html'
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		#posts=Post.objects.filter(created_date__range=[ self.object.rfrom, self.object.rto]).filter(author=self.request.user)
		posts=Post.objects.filter(Q(created_date__gte= self.object.rfrom), created_date__lte=self.object.rto).filter(author=self.request.user)
		
		count=posts.count()
		context = {'report': self.object, 'posts': posts, 'count':count, 'username':request.user.username}

		data['html_form'] = render_to_string('advert/includes/partial_report_view.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)


class ReportDeleteView(LoginRequiredMixin,DeleteView):
	model=Report
	login_url='account/login'
	partial_success_file='advert/includes/partial_report_list.html'
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'report': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_report_delete.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		self.object=self.get_object()
		self.object.delete()
		return HttpResponseRedirect(reverse('advert:report'))


class ReportSendView(LoginRequiredMixin,DeleteView):
	model=Report
	login_url='account/login'
	partial_success_file='advert/includes/partial_report_list.html'
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'report': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_report_send.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		report=self.get_object()
		report.send(self.request)
		return HttpResponseRedirect(reverse('advert:report'))		

	



class PostSubmitView(LoginRequiredMixin, UpdateView):
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	model=Post
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'post': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_post_submit.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		self.object=self.get_object()
		result=self.object.submit()
		if result:
			dic['form_is_valid']=True
			dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		else:
			dic['form_is_valid']=False
			dic['error_message']='No field can be empty. Make sure your upload a thumbnail for you post.'

		return HttpResponseRedirect(reverse('advert:post_list'))

class SendReport(LoginRequiredMixin, ListView):
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	model=Post
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'post': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_post_publish.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		post=self.get_object()
		result=post.publish()
		if result:
			return HttpResponseRedirect(reverse('advert:all_post_list'))
		

class PostPublishView(LoginRequiredMixin, UpdateView):
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	model=Post
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'post': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_post_publish.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'posts':data}
		post=self.get_object()
		result=post.publish()
		if result:
			return HttpResponseRedirect(reverse('advert:all_post_list'))


class PostFeatureView(LoginRequiredMixin, UpdateView):
	login_url='account/login'
	partial_success_file='advert/includes/partial_post_list.html'
	model=Post
	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'post': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_post_feature.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		post=self.get_object()
		lastfeature=Post.objects.filter(featured_post=True).order_by('-created_date').reverse()[0]
		lastfeature.featured_post=False
		lastfeature.save()
		post.featured_post=True
		post.save()	
		return HttpResponseRedirect(reverse('advert:all_post_list'))



class AuthorListView(LoginRequiredMixin, ListView):
	model=User
	login_url='account/login'
	context_object_name='authors'
	template_name='advert/author.html'
	paginate_by=10


class AuthorPostView(LoginRequiredMixin, ListView):
	model=Post
	login_url='account/login'
	context_object_name='posts'
	template_name='advert/post_list.html'
	paginate_by=10
	def get_queryset(self, *args, **kwargs):
		pk=self.kwargs['pk']
		return Post.objects.filter(author__pk=pk)

class AllPostView(LoginRequiredMixin, ListView):
	model=Post
	login_url='account/login'
	context_object_name='posts'
	template_name='advert/post_list.html'
	paginate_by=10

	def get_queryset(self, *args, **kwargs):
		return Post.objects.exclude(status__icontains='draft').order_by('-created_date', 'status')

class ReportView(LoginRequiredMixin, ListView):
	model=Report
	login_url='account/login'
	context_object_name='reports'
	template_name='advert/report_list.html'
	paginate_by=10

	def get_queryset(self, *args, **kwargs):
		return Report.objects.filter(user=self.request.user).order_by('-created_date')






@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    status=post.publish()
    if status:
        return redirect('post_detail', pk=pk)
    else:
        return render(request,'blog/post_detail.html', {'post':post, 'publish_error':True} )




	
class TransactionListView(LoginRequiredMixin,ListView):
	model=Transaction
	login_url='account/login'
	context_object_name='transactions'
	template_name='advert/wallet.html'

	def get_queryset(self):
		return Transaction.objects.filter(wallet=self.request.user.wallet)

	def get_context_data(self, **kwargs):
		context=super(TransactionListView, self).get_context_data(**kwargs)
		context['wallet']=get_object_or_404(Wallet,Owner_id=self.request.user.id)
		context['pt_count']=Transaction.objects.filter(wallet=self.request.user.wallet).filter(status__icontains='pend').count()
		return context

class TransactionCreateView(LoginRequiredMixin,  CreateView):
	model=Transaction
	form_class=TransactionForm
	login_url='account/login'
	partial_success_file='advert/includes/partial_wallet_list.html'
	partial_file='advert/includes/partial_pay_form.html'

	def get(self,request, *args, **kwargs):
		form=TransactionForm()
		data={'form':form}
		dic = dict()
		dic['html_form'] = render_to_string(self.partial_file, data, request=self.request)
		return JsonResponse(dic)

	def form_valid(self, form):
		transaction=form.save(commit=False)
		transaction.wallet=self.request.user.wallet
		transaction.status='Pending'
		transaction.trans_type='Credit'
		if self.request.session['role']=='Content Writer':
			transaction.trans_type='Debit'

		if transaction.trans_type == 'Debit':
			amount=transaction.wallet.amount

			if self.request.POST['amount'] > amount:
				return HttpResponseRedirect(reverse('advert:transaction_list'))

		ref=id_generator()
		transaction.ref=ref
		transaction.save()
		data=dict()
		data['html_list']=render_to_string(self.partial_success_file, data, request=self.request)
		data['form_is_valid']=True
		data['id']=transaction.id
		data['amount']=transaction.amount
		data['email']=self.request.user.email
		return HttpResponseRedirect(reverse('advert:transaction_list'))

	def form_invalid(self,form):
		dic=dict()
		data['form_is_valid']=False
		data['html_form']=form
		return JsonResponse(data)

class AdvertUpdateView(LoginRequiredMixin, UpdateView):
	model=Advert
	context_object_name =Advert
	login_url='account/login'
	partial_success_file='advert/includes/partial_advert_list.html'
	partial_file='advert/includes/partial_advert_update.html'

	def get(self, request, *args,**kwargs):
		dic=dict()
		self.object=self.get_object()
		form=advertForm(instance=self.object)
		data={'form':form, 'advert':self.object}
		dic['html_form']=render_to_string(self.partial_file, data, request=self.request)
		return JsonResponse(dic)
		
	def post(self,request, *args, **kwargs):
		dic=dict()
		self.object=self.get_object()
		form=advertForm(instance=self.object, data=request.POST, files=request.FILES)
		form.save()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'adverts':data}
		dic['form_is_valid']=True
		dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		#return JsonResponse(dic)
		return HttpResponseRedirect(reverse('advert:advert_list'))

class AdvertDeleteView(LoginRequiredMixin,DeleteView):
	model=Advert
	login_url='account/login'
	partial_success_file='advert/includes/partial_advert_list.html'

	def get(self,request, *args, **kwargs):
		data=dict()
		self.object=self.get_object()
		context = {'advert': self.object }
		data['html_form'] = render_to_string('advert/includes/partial_advert_delete.html',
		context,
		request=self.request,
		)
		return JsonResponse(data)

	def post(self,request, *args, **kwargs):
		dic=dict()
		data=Post.objects.filter(author=self.request.user).order_by('-published_date')
		context={'adverts':data}
		self.object=self.get_object()
		self.object.delete()
		dic['form_is_valid']=True
		dic['html_list']=render_to_string(self.partial_success_file,context,request=self.request)
		return HttpResponseRedirect(reverse('advert:advert_list'))


class ProfileUpdateView(LoginRequiredMixin, View):
	login_url='account/login'
	def get(self, request, *args, **kwargs):
		userform=UserForm(instance=self.request.user)
		profile=Profile.objects.get(user=self.request.user)
		profileform=ProfileForm(instance=profile)
		latestpost=Post.objects.filter(author=self.request.user)[:3]
		context={'user':request.user, 'userform':userform, 'profileform':profileform,'posts':latestpost, 'xyzw':True}
		return render(self.request, 'advert/profile.html',context)

	def post(self, request, *args, **kwargs):
		userform=UserForm(data=self.request.POST, instance=self.request.user)
		profile=Profile.objects.get(user=self.request.user)
		profileform=ProfileForm(data=self.request.POST, instance=profile, files=request.FILES)
		userform.save()
		profileform.save()
		profile=Profile.objects.get(user=self.request.user)
		request.session['img_url']=profile.avatar.url
		userform=UserForm(instance=self.request.user)
		profile=Profile.objects.get(user=self.request.user)
		profileform=ProfileForm(instance=profile)
		latestpost=Post.objects.filter(author=self.request.user)[:4]
		context={'user':request.user, 'userform':userform, 'profileform':profileform, 'posts':latestpost, 'xyzw':True}
		return render(self.request, 'advert/profile.html',context)










class ApprovePaytView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		#pdb.set_trace()
		ref=self.request.GET.get('reference')
		transaction=Transaction.objects.get(ref=ref)
		transaction.approve()
		return HttpResponseRedirect(reverse('advert:post_list'))






def monthCount(user, n, count=0):
	
	n.append(Post.objects.filter(Q(author=user),created_date__month=count+1).count())
	if count+1 < 12:
		return monthCount(user, n, count+1)
	else:
		return n

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))







	





	


	





       














	








