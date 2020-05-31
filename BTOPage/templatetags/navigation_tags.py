# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/
from django import template
from wagtail.core.models import Page


register = template.Library()

@register.simple_tag()
def page_objects_count():

    count_of_pages = (
        Page.objects.count() - 1
    )  # Ignore the ROOT page, it is not renderable
    return count_of_pages


@register.inclusion_tag("BTOPage/page_objects_all.html", takes_context=True)
def page_objects_all(context):

    page_objects_all = [
        thing for thing in Page.objects.all() if thing.live and thing.title != "Root"
    ]

    return {
        "page_objects_all": page_objects_all,
    }


@register.simple_tag(takes_context=True)
def footer_text_get(context):
    ###footer_text = ""
    ###if FooterText.objects.first() is not None:
    ###footer_text = FooterText.objects.first().body
    footer_text = "Hello, world! I am some hard-wired FooterText"

    return footer_text


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    ###return context["request"].site.root_page
    return context['request'].site.root_page.specific


def has_children(page):
    # Generically allow index pages to list their children
    return page.get_children().live().exists()


def is_active(page, current_page):
    # To give us active state on main navigation
    return current_page.url_path.startswith(page.url_path) if current_page else False


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }
