from django import forms, template

register = template.Library()

@register.inclusion_tag("elements/form.html")
def form_tag(form, *args, **kwargs):
    context={'form':form,'attrs':kwargs}
    return context

@register.simple_tag(takes_context=True)
def widget_type(context):
    field = context["field"]
    print(field.field.widget)
    type=None
    if isinstance(field.field.widget, forms.CheckboxSelectMultiple):
        type="CheckboxSelectMultiple"
    # how to check if wiget is instance of forms.CheckboxSelectMultiple
    # if isinstance(field.widget, forms.CheckboxSelectMultiple):
    return type