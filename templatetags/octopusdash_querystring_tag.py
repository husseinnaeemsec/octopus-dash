from django import template
from django.http import QueryDict
from django.utils.safestring import mark_safe
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.tag
def od_querystring(parser, token):
    bits = token.split_contents()  # e.g., ['od_querystring', 'foo=bar_var']
    tag_name = bits.pop(0)

    param_map = {}

    for exp in bits:
        if "=" not in exp:
            raise template.TemplateSyntaxError(f"Invalid syntax in `{exp}`, expected key=value.")

        var_name, _, value = exp.partition("=")

        is_name_var = var_name.endswith("_var")
        is_value_var = value.endswith("_var")

        key_expr = parser.compile_filter(
            var_name.replace("_var","") if is_name_var else var_name
        )
        value_expr = parser.compile_filter(
            value.replace("_var","") if is_value_var else value
        )

        param_map[var_name] = {
            'key_expr': key_expr,
            'value_expr': value_expr,
            'is_key_var': is_name_var,
            'is_value_var': is_value_var,
        }

    return QuerystringNode(param_map)

class QuerystringNode(template.Node):
    def __init__(self, param_map: dict):
        self.param_map = param_map

    def render(self, context):
        request = context.get("request")
        if not request:
            return ""

        querydict = request.GET.copy()
        updated_keys = set()

        for _, param in self.param_map.items():
            # Always resolve the key
            
            resolved_key = param['key_expr'].resolve(context)
            resolved_value = param['value_expr'].resolve(context)
            
            
            
            

            # Only update each key once (last-write-wins)
            updated_keys.add(resolved_key)

            if resolved_value is None:
                querydict.pop(resolved_key, None)
            elif isinstance(resolved_value, (list, tuple)):
                querydict.setlist(resolved_key, resolved_value)
            else:
                querydict[resolved_key] = resolved_value

        # Final cleanup pass in case duplicate keys re-added
        for key in updated_keys:
            if querydict.get(key) in [None, ""]:
                querydict.pop(key,None)


        querystring = querydict.urlencode()

        href = mark_safe("?" + querystring if querystring  else request.build_absolute_uri(request.path))

        return href