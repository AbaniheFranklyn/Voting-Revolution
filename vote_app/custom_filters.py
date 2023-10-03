from django import template

register = template.Library()

@register.filter
def get_candidate_level_list(voted):
    return [v.candidate_level for v in voted]
