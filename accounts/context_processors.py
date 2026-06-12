from .models import COLOR_SCHEME_CHOICES, THEME_MODE_CHOICES, COLOR_HEX_MAP


def theme_context(request):
    context = {
        'color_schemes': COLOR_SCHEME_CHOICES,
        'theme_modes': THEME_MODE_CHOICES,
        'color_hex_map': COLOR_HEX_MAP,
    }

    if request.user.is_authenticated:
        context['user_theme'] = request.user.userprofile.theme_mode
        context['user_color'] = request.user.userprofile.color_scheme
        context['user_color_hex'] = request.user.userprofile.color_hex
    else:
        context['user_theme'] = 'light'
        context['user_color'] = 'blue'
        context['user_color_hex'] = '#3B82F6'

    return context
