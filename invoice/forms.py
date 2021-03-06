# -*- coding: utf-8 -*-

from django import forms
from invoice.models import Address, Code, Event, Invoice, Invoice_Material, Invoice_Service, Manufacturer, Material, Material_Group, Material_Transactions, Organization, Project, Service, Warehouse, Tax, Unit
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from django.utils.translation import ugettext_lazy
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm

class InvoiceForm(forms.ModelForm):
    BOOLEAN_OPTION = ((0, 'N'),(1, 'Y'),)

    name = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control',}))
    type =  forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='TYPE'), widget= forms.Select(attrs={'class': 'select2' }))
    create_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    sales_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    status = forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='STATUS'), widget= forms.Select(attrs={'class': 'select2' }))
    additional_address_ind = forms.ChoiceField(label='Additional Address', choices=BOOLEAN_OPTION, widget= forms.Select(attrs={'class': 'select2' }))
    company = forms.ModelChoiceField(queryset = Organization.objects.all().filter(is_owner=1), widget=forms.Select(attrs={'class':'select2'}))
    customer = forms.ModelChoiceField(queryset = Organization.objects.all().filter(is_customer=1), widget=forms.Select(attrs={'class':'select2'}))
    payment_method = forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='PAYMENT_METHOD'), widget= forms.Select(attrs={'class': 'select2' }))
    class Meta:
        model = Invoice
        fields = ['id','name', 'type', 'create_date', 'payment_date','sales_date','status','additional_address_ind','company','customer', 'payment_method']

class InvoiceServiceForm(forms.ModelForm):
    quantity = forms.CharField(required =False, widget= forms.TextInput(attrs={'class': 'form-control',}))
    service = forms.ModelChoiceField(required =False, queryset = Service.objects.all(), widget=forms.Select(attrs={'class':'select2'}))

    class Meta():
        model = Service
        fields = ['service','quantity',]

class InvoiceMaterialForm(forms.ModelForm):
    quantity = forms.CharField(required =False, widget= forms.TextInput(attrs={'class': 'form-control',}))
    material = forms.ModelChoiceField(queryset = Material.objects.all(), widget=forms.Select(attrs={'class':'select2'}), required =False)
    warehouse =  forms.ModelChoiceField(queryset=Warehouse.objects.all(), widget= forms.Select(attrs={'class': 'select2' }), required=False)
    class Meta():
        model = Material
        fields = ['material','quantity', 'warehouse',]

class EventForm(forms.ModelForm):
    project = forms.ModelChoiceField(required =False, label='Project', queryset = Project.objects.all(), widget=forms.Select(attrs={'style':'width: 100%','class':'project-select', 'id':'project-select'}))
    name = forms.CharField(required =False, label='Description', widget= forms.Textarea(attrs={'class': 'form-control','id':'event-name', }))
    hour = forms.CharField(required =False, label='Hour', widget= forms.TextInput(attrs={'class': 'form-control','id':'event-hour',}))
    start_date = forms.DateField(required =False, label='Start Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-start-date', }))
    end_date = forms.DateField(required =False, label='End Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-end-date',}))
    type_code = forms.CharField(required =False, label='Event Type', initial='TS', widget= forms.TextInput(attrs={'readonly' : 'True','class': 'form-control','id':'event-type'}))
    class Meta:
        model = Event
        fields = ['id','name', 'hour','start_date','end_date','type_code','project']

class EventForm(forms.ModelForm):
    project = forms.ModelChoiceField(required =False, label='Project', queryset = Project.objects.all(), widget=forms.Select(attrs={'style':'width: 100%','class':'project-select', 'id':'project-select'}))
    name = forms.CharField(required =False, label='Description', widget= forms.Textarea(attrs={'class': 'form-control','id':'event-name', }))
    hour = forms.CharField(required =False, label='Hour', widget= forms.TextInput(attrs={'class': 'form-control','id':'event-hour',}))
    start_date = forms.DateField(required =False, label='Start Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-start-date', }))
    end_date = forms.DateField(required =False, label='End Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-end-date',}))
    type_code = forms.CharField(required =False, label='Event Type', initial='TS', widget= forms.TextInput(attrs={'readonly' : 'True','class': 'form-control','id':'event-type'}))
    class Meta:
        model = Event
        fields = ['id','name', 'hour','start_date','end_date','type_code','project']

class TaxForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'tax-name', }))
    value = forms.CharField(required =True, label='Value', widget= forms.TextInput(attrs={'class': 'form-control','id':'tax-value', }))
    class Meta:
        model = Tax
        fields = ['name','value']

class UnitForm(forms.ModelForm):
    code = forms.CharField(required =True, label='Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'unit-code', }))
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'unit-name', }))
    class Meta:
        model = Unit
        fields = ['code','name']

class MaterialForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'material-name', }))
    unit = forms.ModelChoiceField(queryset = Unit.objects.all() , label='Unit', widget= forms.Select(attrs={'class': 'select','id':'material-unit', }))
    tax = forms.ModelChoiceField(queryset = Tax.objects.all() , label='Tax', widget= forms.Select(attrs={'class': 'select','id':'material-tax', }))
    group = forms.ModelChoiceField(required =False, queryset = Material_Group.objects.all().exclude(parrent__isnull=True) , label='Group', widget= forms.Select(attrs={'class': 'select','id':'material-group', }))
    manufacturer = forms.ModelChoiceField(required =False, queryset = Manufacturer.objects.all() , label='Manufacturer', widget= forms.Select(attrs={'class': 'select','id':'material-manufacturer', }))
    dealer = forms.ModelChoiceField(required =False, queryset = Organization.objects.filter(is_dealer=1) , label='Dealer', widget= forms.Select(attrs={'class': 'select','id':'material-dealer', }))
    price = forms.DecimalField(required =False, label='Price', widget= forms.NumberInput(attrs={'class': 'form-control','id':'material-price', }))
    class Meta:
        model = Material
        fields = ['name','unit', 'price','tax','group','manufacturer','dealer']

class ManufacturerForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'manufacturer-name', }))
    class Meta:
        model = Manufacturer
        fields = ['name']

class MaterialGroupForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'material-group-name', }))
    parrent = forms.ModelChoiceField(required =False, queryset = Material_Group.objects.order_by('name').distinct(), label='Parrent', widget= forms.Select(attrs={'class': 'select','id':'material-group-parrent', }))
    class Meta:
        model = Material_Group
        fields = ['name','parrent']

class MaterialTransactionForm(forms.ModelForm):
    transaction_time = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control','id':'transaction-time', }), label='Transaction Time', )
    warehouse = forms.ModelChoiceField(queryset = Warehouse.objects.all(), label='Warehouse', widget= forms.Select(attrs={'class': 'select','id':'warehouse', }))
    invoice = forms.ModelChoiceField(queryset = Invoice.objects.all(), label='Invoice', widget= forms.Select(attrs={'class': 'select','id':'invoice', }))
    material = forms.ModelChoiceField(queryset = Material.objects.all(), label='Material', widget= forms.Select(attrs={'class': 'select','id':'material', }))
    units = forms.DecimalField(label='Units', widget= forms.NumberInput(attrs={'class': 'form-control','id':'units', }))
    class Meta:
        model = Material_Transactions
        fields = ['warehouse','invoice','material','units','transaction_time']

class OrganizationForm(forms.ModelForm):
    OPTIONS = (
                (1, "Yes"),
                (0, "No"),
                (-1, "N/A"),
                )
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-name', }))
    main_address = forms.ModelChoiceField(required =False, label='Main Address', widget= forms.Select(attrs={'class': 'select','id':'organization-main-address', }), queryset=Address.objects.filter(address_type=1) )
    additional_address = forms.ModelChoiceField(required =False, label='Additional Address', widget= forms.Select(attrs={'class': 'select','id':'organization-additional-address', }), queryset=Address.objects.filter(address_type=2) )
    phone = forms.CharField(required =False, label='Phone', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-phone', }))
    email = forms.CharField(required =False, label='Email', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-email', }))
    org_nbr_1 = forms.CharField(required =False, label='NIP', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-org-nbr-1', }))
    org_nbr_2 = forms.CharField(required =False, label='REGON', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-org-nbr-2', }))
    org_nbr_3 = forms.CharField(required =False, label='PESEL', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-org-nbr-3', }))
    is_owner =  forms.NullBooleanField(required =False, widget= forms.CheckboxInput(attrs={'class': 'checkbox','id':'is_owner', }))
    is_customer = forms.NullBooleanField(required =False, widget= forms.CheckboxInput(attrs={'class': 'checkbox'}))
    is_dealer = forms.NullBooleanField(required =False, widget= forms.CheckboxInput(attrs={'class': 'checkbox','id':'is_dealer', }))
    is_manufacturer = forms.NullBooleanField(required =False, widget= forms.CheckboxInput(attrs={'class': 'checkbox','id':'is_manufacturer', }))
    class Meta:
        model = Organization
        fields = ['name','main_address','additional_address', 'phone','email','org_nbr_1','org_nbr_2','org_nbr_3','is_owner','is_customer','is_dealer','is_manufacturer']

class AddressForm(forms.ModelForm):

    ADDRESS_TYPE_OPTIONS = ((1, 'Główny'),(2, 'Dodatkowy'),)

    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-name', }))
    address_type = forms.ChoiceField(label='Address Type', choices=ADDRESS_TYPE_OPTIONS, widget= forms.Select(attrs={'class': 'form-control','id':'organization-address-type', }))
    street_name = forms.CharField(required =False, label='Street Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-street-name', }))
    street_number = forms.CharField(required =False, label='Street Number', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-street-number', }))
    zip_code = forms.CharField(required =False, label='Zip Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-zip-code', }))
    city = forms.CharField(required =False, label='City', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-city', }))
    country = forms.CharField(required =False, label='Country', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-country', }))

    class Meta:
        model = Address
        fields = ['name','address_type', 'street_name','street_number','zip_code','city','country']

class ProjectForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'project-name', }))
    customer = forms.ModelChoiceField(queryset = Organization.objects.all().filter(is_customer=1) , label='Customer', widget= forms.Select(attrs={'class': 'form-control','id':'project-customer', }))
    code = forms.CharField(required =True, label='Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'project-code', }))

    class Meta:
        model = Project
        fields = ['name','code','customer']


class ServiceForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-name', }))
    version = forms.CharField(required =False, label='Version', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-version', }))
    tax = forms.ModelChoiceField(queryset = Tax.objects.all() , label='Tax', widget= forms.Select(attrs={'class': 'form-control','id':'service-tax', }))
    unit = forms.ModelChoiceField(queryset = Unit.objects.all() , label='Unit', widget= forms.Select(attrs={'class': 'form-control','id':'service-unit', }))
    unit_price = forms.DecimalField(required =False, label='Unit Price', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-unit-price', }))

    class Meta:
        model = Service
        fields = ['name','version','tax','unit','unit_price']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email', 'aria-describedby' : 'basic-addon1'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password', 'aria-describedby' : 'basic-addon2'}))

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset = Group.objects.all() , label='Group', widget= forms.Select(attrs={'class': 'form-control','id':'user-group', }))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class GroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Group
        fields = ['name']

class PermissionForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'permision-name', }))
    content_type = forms.CharField(required =True, label='Content Type', widget= forms.TextInput(attrs={'class': 'form-control','id':'permision-content_type', }))
    codename = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'permision-name', }))

    class Meta:
        model = Permission
        fields = ['name','content_type','codename']

invoice_service_formset = inlineformset_factory(Invoice, Invoice_Service, form=InvoiceServiceForm, extra=1, can_delete=True)
invoice_material_formset = inlineformset_factory(Invoice, Invoice_Material, form=InvoiceMaterialForm, extra=1, can_delete=True)
