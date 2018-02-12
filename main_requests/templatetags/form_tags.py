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
            css_class = 'is-invalid this-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid this-valid'

    if bound_field.field.widget.__class__.__name__=='DateTimeInput':
        css_class=css_class+' datepicker-need '
    if bound_field.name.find('datetime')>0:
        css_class = css_class + ' datepicker-need '
    if bound_field.name.find('dateTime') > 0:
            css_class = css_class + ' datepicker-need '

    return 'form-control form-control-sm {0} '.format(css_class)

@register.filter
def grid_input_class(bound_field):
    if bound_field.field.widget.__class__.__name__=='Textarea':
        return 'col-sm-12 col-md-12  col-12'

    return 'col-sm-12 col-md-12 col-lg-6 col-12'

@register.filter
def grid_label_class(bound_field):
    if bound_field.field.widget.__class__.__name__=='Textarea':
        return 'col-4 col-sm-4 col-md-4  col-lg-2 col-12'

    return 'col-sm-4 col-md-4 col-4'


@register.filter
def large_grid_input_class(bound_field):
    if bound_field.field.widget.__class__.__name__=='Textarea':
        return 'col-sm-12 col-md-12  col-12'

    return 'col-sm-12 col-md-6 col-lg-4 col-12'


@register.filter('group_can_correct_requets')
def has_group(user):
    """
    Verifica se este usuário pertence a um grupo
    """
    groups = user.groups.all().values_list('id', flat=True)
    if 1 in groups:
        return True
    if 2 in groups:
        return True
    return False

@register.filter('set_enabled')
def initenabledfield(boundfild):
    if boundfild.field.widget.attrs['disabled'] == True:
        return "disabled"
    return ""

