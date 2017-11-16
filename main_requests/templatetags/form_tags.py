from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def field_in_group(bound_field):
   return bound_field.field.fieldname



@register.filter
def input_class(bound_field):
    css_class = ' '
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'

    if bound_field.field.widget.__class__.__name__=='DateTimeInput':
        css_class=css_class+' datetimepicker_add '

    return 'form-control form-control-sm {0} '.format(css_class)
