from django import forms


class CustomRadioSelect(forms.widgets.ChoiceWidget):
    input_type = 'radio'
    template_name = 'widgets/custom_radio_select.html'

    class Media:
        css = {
            'all': ('/assets/css/widgets/custom_radio_select.css',)
        }

