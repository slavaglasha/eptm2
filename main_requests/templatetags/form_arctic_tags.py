from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def field_in_group(bound_field):
    return bound_field.field.fieldname


@register.filter
def invalid_input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'invalid'
    return css_class


@register.filter
def set_enabled(bound_field):
    if bound_field.field.widget.attrs['disabled']:
        return "disabled"
    return ""


@register.filter
def set_label_grid(bound_field):
    if bound_field.field.widget.__class__.__name__ == 'Textarea':
        return ' col-sm-4 col-md-4 col-lg-2 col-xl-2  col-4'
    for item, valu in bound_field.field.widget.attrs.items():
        if item == 'new_line':
            return ' col-sm-4 col-md-2 col-lg-2 col-xl-2  col-4'
    return ' col-4'


@register.filter
def  set_input_grid(bound_field):
    if bound_field.field.widget.__class__.__name__ == 'Textarea':
        return ' col-sm-8 col-md-8 col-lg-8 col-xl-10  col-10'
    for item, valu in bound_field.field.widget.attrs.items():
        if item == 'new_line':
            return ' col-sm-8 col-md-4 col-lg-4 col-xl-4  col-8'
    return ' col-8'


@register.filter
def set_field_grid(bound_field):
    if bound_field.field.widget.__class__.__name__ == 'Textarea':
        return ' col-sm-12 col-md-12 col-lg-12 col-xl-12  col-12'
    for item, valu in bound_field.field.widget.attrs.items():
        if item == 'new_line':
            return ' col-sm-12 col-md-12 col-lg-12 col-xl-12  col-12'
    return 'col-sm-12 col-md-6 col-lg-6 col-12'


@register.filter
def set_timeclass(bound_field):
    if (bound_field.name.find('datetime') > 0) or (bound_field.name.find('dateTime') > 0):
        return 'interval'
    else:
        return ''


@register.filter
def input_class(bound_field):
    if (bound_field.name.find('datetime') > 0) or (bound_field.name.find('dateTime') > 0):
        return 'datepicker-need'
    return ''


@register.filter
def new_line(bound_field):
    resu = 'line '
    # for ex, val in bound_field.field.widget.attrs.items:
    #     resu = resu + ex+' ' +val+'; '
    return 'lll'
