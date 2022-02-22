from django import forms


from .models import Project, Image, Tag, ProjectRate, Comment,Report


class DateInput(forms.DateInput):
    input_type = 'date'

class NumberInput(forms.NumberInput):
    input_type = 'number'

class SelectOptions(forms.CheckboxSelectMultiple):
    input_type = 'checkbox'

class ImageInput(forms.FileInput):
    input_type = 'file'


class AddProjectForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(item.id, item.title) for item in Tag.objects.all()])

    class Meta:
        # fields= '__all__'
        fields= ['title','details','start_date','end_date','total_target','category','main_photo']
        model = Project
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'total_target': NumberInput(),
            'tags': SelectOptions(),
        }
    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.fields['main_photo'].required = True
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ImagesProject(forms.ModelForm):

    class Meta:
        # file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        fields = ['image']
        model = Image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].widget.attrs.update({'multiple': True})


################ Create Form #################
class AddProjectRate(forms.ModelForm):

    class Meta:
        fields = ['is_upvote']
        model = ProjectRate


###############################################
class DonationForm( forms.Form):
    donate = forms.IntegerField(min_value=1)
##############################################


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets ={
            'body': forms.Textarea(attrs={'class': 'class-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'input'})
