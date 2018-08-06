from django import forms


class URLScraperForm(forms.Form):
    requested_url = forms.CharField(max_length=512, help_text="Please enter a URL to scrape.")

    def clean_url_data(self):
        data = self.cleaned_data['requested_url']

        return data
