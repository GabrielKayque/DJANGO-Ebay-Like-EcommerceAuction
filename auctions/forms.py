from django import forms
from .models import Listing

class NewAuctionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'author','description', 'categories', 'imgurl', 'bid']
        
        
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Auction Title'}),
            'author': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Tell us more about your product Here..'}),
            'categories': forms.SelectMultiple(attrs={'class':'form-control'}),
            'imgurl': forms.TextInput(attrs={'class':'form-control','placeholder':'Put an HTML link for your image'}),
            'bid': forms.NumberInput(attrs={'class':'form-control','placeholder':'How much is the Initial bid?','step':'0.01'}),
            
        }
            
    def __init__(self, *args, **kwargs):
        super(NewAuctionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['description'].label = ""
        self.fields['categories'].label = "Categories: Hold Ctrl to choose more than one"
        
