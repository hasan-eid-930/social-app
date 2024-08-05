from django import forms, template
from django.db.models import Count
from posts.models import Comment, Post, Tag

register = template.Library()



@register.inclusion_tag("includes/sidebar.html")
def sidebar_tag(tag=None,user=None, *args, **kwargs):
    categories=Tag.objects.all()
    top_posts=Post.objects.annotate(num_likes=Count("likes")).filter(num_likes__gt=0).order_by('-num_likes')[:5]
    top_comments=Comment.objects.annotate(num_likes=Count("likes")).filter(num_likes__gt=0).order_by('-num_likes')[:5]
    context={'categories':categories,
             'tag':tag,
             'top_posts':top_posts,
             'top_comments':top_comments,
             'user':user,
             }
    return context


@register.inclusion_tag("elements/form.html")
def form_tag(form, *args, **kwargs):
    context={'form':form,'attrs':kwargs}
    return context

@register.simple_tag(takes_context=True)
def widget_type(context):
    field = context["field"]
    type=None
    if isinstance(field.field.widget, forms.CheckboxSelectMultiple):
        type="CheckboxSelectMultiple"
    # how to check if wiget is instance of forms.CheckboxSelectMultiple
    # if isinstance(field.widget, forms.CheckboxSelectMultiple):
    return type