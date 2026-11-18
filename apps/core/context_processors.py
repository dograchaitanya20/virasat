from django.conf import settings

def global_context(request):
    """Global context available across all Virasat templates."""
    return {
        'SITE_NAME': 'Virasat',
        'SITE_TAGLINE': 'The Eternal Tapestry of Indian Heritage',
        'SITE_NAME_HI': 'विरासत',
        'CURRENT_PATH': request.path,
        'LANGUAGES': settings.LANGUAGES,
    }
