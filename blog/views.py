from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.models import Post, Comment, Category, SubscribeEmail
from account.models import Profile
from django.contrib import messages
from django.utils import timezone
from django.views import View
from advert.models import Advert
from blog.forms import PostForm, CommentForm, FacetedPostSearchForm, SubscribeForm, ContactForm
from random import choice
from django.utils.encoding import force_bytes, force_text
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from .tokens import account_activation_token
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import pdb
import json



class AboutView(TemplateView):
    template_name = 'about.html'


class ProfileView(DetailView):
    template_name = 'profile_detail.html'
    model = Profile
    slug_field = "user"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile_list'] = Profile.objects.all()
        context['post_list'] = Post.objects.all()
        context['post_count'] = Post.objects.count()
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)
        
        
        return context


class GrassToGraceView(ListView):
    template_name ='grass-to-grace.html'

    def get_context_data(self, **kwargs):
        context = super(GrassToGraceView, self).get_context_data(**kwargs)
        story_cat = Category.objects.get(name='my story')
        context['story_posts'] = Post.objects.filter(category = story_cat)
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)
        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

# Category View
def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    adverts=Advert.objects.filter(plan__name__icontains='Prem')
    advert_index=[ advert.pk for advert in adverts]
    fetch_index=choice(advert_index)
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category,slug=slug,parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "post_detail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

    return render(request,"category.html",{'post_set':parent.post_set.all().order_by('-published_date'),'sub_categories':parent.children.all(), 'ad':Advert.objects.get(pk=fetch_index)})


class PostListView(ListView):
    model = Post
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.exclude(Q(category__name__icontains='my st'), featured_post=False).filter(status__icontains='publis').order_by('-created_date')
        context['profile_list'] = Profile.objects.all()
        context['featured_posts'] = Post.objects.filter(featured_post=True).exclude(category__name__icontains='my sto').filter(status__icontains='publis').order_by('-published_date')
        context['trending_posts'] = Post.objects.filter(trending_post=True).exclude(category__name__icontains='my sto').filter(status__icontains='publis')
        context['latest_posts'] =  Post.objects.filter(published_date__lte=timezone.now()).filter(status__icontains='publis').exclude(featured_post=True).order_by('-published_date')[7:14]
        context['fashion_posts'] = Post.objects.filter(category__name__icontains = 'fashion').filter(status__icontains='publis').order_by('-published_date')
        context['business_posts'] = Post.objects.filter(category__name__icontains = 'business').filter(status__icontains='publis').order_by('-published_date')
        context['entertainment_posts'] = Post.objects.filter(category__name__icontains='entertainment').filter(status__icontains='publis').order_by('-published_date')
        context['tech_posts'] = Post.objects.filter(category__name__icontains='techn').filter(status__icontains='publis').order_by('-published_date')
        context['pol_posts'] = Post.objects.filter(category__name__icontains='politics').filter(status__icontains='publis').order_by('-published_date')
        context['post_story']=Post.objects.get(Q(category__name__icontains='my sto'), featured_post=True )#rtrtrtrt
        context['lnp']=Post.objects.filter(category__name__icontains='news').filter(status__icontains='publis').exclude(featured_post=True).order_by('-published_date')[:15]
        listed_post = Post.objects.all()
        paginator = Paginator(listed_post, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            list_posts = paginator.page(page)
        except PageNotAnInteger:
            list_posts = paginator.page(1)
        except EmptyPage:  #d
            list_posts = paginator.page(paginator.num_pages)

        context['listed_posts'] = list_posts
        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post=self.get_object()
        name=post.category.name
        context['Comments'] = Comment.objects.all()
        context['post_list'] = Post.objects.all()
        story_cat = Category.objects.get(name='my story')
        context['story_posts'] = Post.objects.filter(category = story_cat)
        context['featured_posts'] = Post.objects.filter(featured_post=True).order_by('-published_date')
        context['similar_posts']=Post.objects.filter(category__name__icontains=name).exclude(id=post.id)[:6]
        context['trending_posts'] = Post.objects.filter(trending_post=True).exclude(id=post.id)
        context['recent_posts'] = Post.objects.filter(published_date__lte=timezone.now()).exclude(id=post.id).order_by('-published_date')
        context['form'] = CommentForm
        context['approved_comments'] = Comment.objects.filter(approved_comment=True)
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)
        context['lnp']=Post.objects.filter(category__name__icontains='news').filter(status__icontains='publis').exclude(featured_post=True).order_by('-published_date')[:3]
        
        return context



class newsfeed(View):
    def get(self, request, *args, **kwargs ):
        news=dict()
        news['status']=True
        template='blog/includes/lnp.html'
        a= self.request.GET.get('no')
        a=int(a)

        if a and a > 1:
            newsfeed=Post.objects.filter(category__name__icontains='news').filter(status__icontains='publis').exclude(featured_post=True).order_by('-published_date')[:a]
            newsfeed=render_to_string(template, {'lnp':newsfeed} )
            news['news']=newsfeed
            return JsonResponse(news)
        else:
            news['status']=False
            return JsonResponse(news)     





class CommentFormView(FormView):
    form_class = CommentForm
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        comment = form.save(commit=False)
        # pdb.set_trace()
        comment.post = post
        comment.save()
        return super(CommentFormView, self).form_valid(form)


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = 'account/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.author=self.request.user
        self.object.save()
        return super(CreatePostView, self).form_valid(form)

        
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = 'account/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = 'account/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    #def form_valid

class ContactView(CreateView):
    template_name='blog/contact.html'
    form_class=ContactForm
    
    def get_context_data(self,**kwargs):
        context=super(ContactView,self).get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(featured_post=True)
        return context

    def form_valid(self,form):
        messages.success(self.request, 'Thank you for contacting us.We will get back to you shortly.')
        return super(ContactView,self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:contact_us')


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get(
            'query',
            ''))[
        :5]
    s = []
    for result in sqs:
        d = {"value": result.title, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):

  form_class = FacetedPostSearchForm
  facet_fields = ['text', 'title']
  template_name = 'search_result.html'
  paginate_by = 9
  context_object_name = 'object_list'

  def get_context_data(self, **kwargs):
        context = super(FacetedSearchView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)

        return context


#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    status=post.publish()
    if status:
        return redirect('post_detail', pk=pk)
    else:
        return render(request,'blog/post_detail.html', {'post':post, 'publish_error':True} )


@csrf_exempt
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        comment_text = request.POST.get('the_comment')
        comment_author = request.POST.get('the_author')
        response_data = {}

        comment = Comment(text=comment_text, author=comment_author)
        comment.post = post
        comment.save()
        
        response_data['result'] = 'Create comment successful!'
        response_data['text'] = comment.text
        response_data['author'] = comment.author

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
    


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

class PrivacyView(TemplateView):
    template_name='blog/privacy.html'

    def get_context_data(self, **kwargs):
        context=super(PrivacyView, self).get_context_data(**kwargs)
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)
        return context

class TermsView(TemplateView):
    template_name='blog/terms.html'
    def get_context_data(self, **kwargs):
        context=super(TermsView, self).get_context_data(**kwargs)
        adverts=Advert.objects.filter(plan__name__icontains='Prem')
        advert_index=[ advert.pk for advert in adverts]
        fetch_index=choice(advert_index)
        context['ad']=Advert.objects.get(pk=fetch_index)
        return context

class SubscribeView(CreateView):
    form_class=SubscribeForm
    success_url = "/"
    template_name='/blog/post_list.html'
    model=SubscribeEmail

    def form_valid(self,form):
        email=self.request.POST['email']
        email_test=SubscribeEmail.objects.filter(email__icontains=email)
        if email_test.exists():
            messages.warning(self.request, 'This email has already registered')
            return HttpResponseRedirect(reverse('blog:post_list'))
        current_site = get_current_site(self.request)
        unique_id = get_random_string(length=32)
        
       
        message = render_to_string('blog/includes/subscribe_email.html', {
                'domain':current_site.domain,
                'token':unique_id,
                'email':email,
            })
        messages.success(self.request, 'We have sent a verification link to your  email address . Thank You ')
        mail_subject = 'Activate your AvetiZ Blog Subscription.'
        email = EmailMessage(mail_subject, message,'contact@avetiz.com', to=[email], reply_to=['contact@avetiz.com'],)
        email.send()
        subscribeemail=form.save(commit=False)
        subscribeemail.token=unique_id
        subscribeemail.save()
        return HttpResponseRedirect(reverse('blog:post_list'))

    def form_invalid(self,form):
        messages.warning(self.request, 'Invalid Email Address ')
        return HttpResponseRedirect(reverse('blog:post_list'))



def activate(request):
    email_get=request.GET.get('email')
    token=request.GET.get('token')
    email=SubscribeEmail.objects.get(email__icontains=email_get)
    if email.token == token :
        messages.success(request, 'Subscription Successful')
        email.active=True
        email.save()
        return HttpResponseRedirect(reverse('blog:post_list'))
    else:
        return HttpResponseRedirect(reverse('blog:post_list'))


def increaseView(request):
    pk=request.GET.get('pk')
    post=get_object_or_404(Post, pk=pk)
    post.pageview+=1
    post.save()
    return JsonResponse( {'status':True} )


    




       



