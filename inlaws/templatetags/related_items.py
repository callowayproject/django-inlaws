"""
Related items for Django Admin
"""

from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, VariableDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

_EXCLUDED_MODELS = getattr(settings, "ADMIN_RELATED_EXCLUDES", [])

# Holds a list of "app.model" strings of the models that should be ignored.
EXCLUDED_MODELS = []
for mod in _EXCLUDED_MODELS:
    try:
        a, m = mod.split(".")
        ctype = ContentType.objects.get(app_label__iexact=a, model__iexact=m)
    except ContentType.DoesNotExist:
        raise ImproperlyConfigured(
            "ADMIN_RELATED_EXCLUDES: '%s' is not a valid model" % mod
        )
        
    EXCLUDED_MODELS.append("%s:%s" % (a.lower(), m.lower()))
    
# An integer of the number to limit in the queryset.
ITEM_LIMIT = getattr(settings, "ADMIN_RELATED_ITEM_LIMIT", 5)

register = Library()
    
class RelatedObjectsNode(Node):
    def __init__(self, obj, varname):
        super(RelatedObjectsNode, self).__init__()
        
        self.obj, self.varname = obj, varname
    
    def render(self, context):
        """
        Retreive the related objects for a specified instance.
        """
        try:
            obj = Variable(self.obj).resolve(context)
        except VariableDoesNotExist:
            return ""
            
        rel = {}
        related_models = obj._meta.get_all_related_objects()
        related_models.extend(obj._meta.get_all_related_many_to_many_objects())
        
        for related in related_models:
            # If model is specified to be excluded, just move on to the 
            # next related model.
            if related.name in EXCLUDED_MODELS:
                continue
                
            # Get the app and model
            app, model = related.name.split(":")
            
            # Build the kwargs for the queryset that will be shown
            kwgs = {'%s__pk' % related.field.name: obj.pk}
            
            # Retreive the queryset, limiting the number of item
            # that will be returned
            qs = related.model.objects.filter(**kwgs)
            
            # If the queryset is empty, just move on 
            # to the next related model.
            if not qs:
                continue
            
            # Add a display_name, items, related field name and the admin
            # url for the model changelist.
            try:
                rel[related.name] = {
                    'display_name': "%s %s" % (app, model),
                    'items': qs[:ITEM_LIMIT],
                    'related_field_name': related.field.name,
                    'url': reverse("admin:%s_%s_changelist" % (app, model))
                }
            except NoReverseMatch:
                # This error will occur naturally for models that have no
                # admin interface specified.
                pass
        
        # Set the return variable to the dictionary.
        context[self.varname] = rel
        return ""


class AdminUrlNode(Node):
    """
    Returns the admin url to change the object passed as a parameter.
    
    Optionally will set the value to a variable, otherwise outputs it.
    """
    
    def __init__(self, obj, varname=None):
        super(AdminUrlNode, self).__init__()
        
        self.obj = obj
        self.varname = varname
    
    def render(self, context):
        """
        Either write out the url, or set the variable in the context.
        """
        try:
            # Retrieve the object instance.
            obj = Variable(self.obj).resolve(context)
        except VariableDoesNotExist:
            obj = self.obj
        
        try:
            urlname = 'admin:%s_%s_change' % (
                obj._meta.app_label, obj._meta.module_name
            )
            url = reverse(urlname, args=(obj.pk,))
        except NoReverseMatch, err:
            if settings.TEMPLATE_DEBUG:
                print "Got an exception resolving an admin url: ", err
            return ''
        
        if self.varname:
            context[self.varname] = url
        else:
            return url

def get_admin_url(parser, token):
    """
    {% get_admin_url object [as varname ]%}
    """
    argv = token.contents.split()
    argc = len(argv)
    varname = None
    if argc == 0:
        raise TemplateSyntaxError(
            "%s requires an object passed as an argument." % argv[0]
        )
    elif argc == 3:
        raise TemplateSyntaxError(
            "%s requires a variable name passed after 'as'" % argv[0]
        )
    elif argc == 4 and argv[2] != 'as':
        raise TemplateSyntaxError(
            "Usage: {%% %s object [as variablename] %%}" % argv[0]
        )
    elif argc == 4:
        varname = argv[3]
    
    return AdminUrlNode(argv[1], varname)

def do_related_objects(parser, token):
    """
    Returns the objects related to the object passed. The objects returned are
    objects that have a ForeignKey or ManyToMany relation to this object.
    
    {% admin_related_objects object as varname %}
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc != 4:
        raise TemplateSyntaxError('Tag %s takes three arguments.' % argv[0])
    if argv[2] != "as":
        raise TemplateSyntaxError(
            'Second argument must be "as" for tag %s' % argv[0]
        )
        
    return RelatedObjectsNode(argv[1], argv[3])

register.tag("admin_related_objects", do_related_objects)
register.tag("get_admin_url", get_admin_url)