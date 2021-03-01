from django.forms import Widget


class PlusMinusNumberInput(Widget):
    template_name = 'main/widgets/plusminusnumber.html'

    class Media:
        css = {
            'all': ('main/css/plusminusnumber.css',)
        }
        js = ('main/js/plusminusnumber.js',)
