from django import forms


class InputForm(forms.Form):
    username = forms.CharField(
        label='AtCoder Nickname',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
