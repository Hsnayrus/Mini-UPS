from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Package, UPSAccount


class UserSignUpForm(UserCreationForm):
    # user_type = forms.CharField(label='Please select user type', widget=forms.Select(choices=USER_TYPES))
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2')

    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            print(user.email, user.username, user.password)
        return user


class UPSAccountForm(forms.ModelForm):
    class Meta:
        model = UPSAccount
        fields = ['world_id', 'acct_number', 'user']


class PackageForm(forms.ModelForm):
    # class Meta:
    #     model = User
    #     exclude = ['username']
    class Meta:
        model = Package
        fields = ['destination_pos_x', 'destination_pos_y']

class AdminPackageForm(forms.ModelForm):
        # package_id = models.IntegerField(primary_key=True) # we will treat package_id the same as tracking_number
        # world_id = models.IntegerField()
        # truck = models.ForeignKey(Truck, null=True, on_delete=models.CASCADE)
        # ups_account = models.ForeignKey(UPSAccount, blank=True, null=True, on_delete=models.CASCADE)
        # destination_pos_x = models.IntegerField()
        # destination_pos_y = models.IntegerField()
        # warehouse_id = models.IntegerField()
        # warehouse_pos_x = models.IntegerField()
        # warehouse_pos_y = models.IntegerField()
        # status = models.CharField(max_length=50, choices=PACKAGE_STATUS)
    class Meta:
        # model = User
        # exclude = ['password']
        model = Package
        fields = ['package_id',
                  'world_id',
                  'truck',
                  'ups_account',
                  'destination_pos_x',
                  'destination_pos_y',
                  'warehouse_id',
                  'warehouse_pos_x',
                  'warehouse_pos_y',
                  'status']