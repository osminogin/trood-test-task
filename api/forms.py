from django import forms


class UploadForm(forms.Form):
    """
    Pseudo-form for file uploads.
    """
    file = forms.FileField()
