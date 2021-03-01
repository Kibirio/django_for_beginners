import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from main import models

from main import forms

logger = logging.getLogger(__name__)


# Create your views here.
class ContactUsView(FormView):
    template_name = 'main/contact_us.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(models.ProductTag, slug=tag)
        if self.tag:
            products = models.Product.objects.filter(tags=self.tag)
        else:
            products = models.Product.objects
        return products.order_by('name')


class SignUpView(FormView):
    template_name = 'main/signup.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get('/')
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('passowrd1')
        logger.info(
            'New signup for email=%s through SignUpView', email
        )

        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        form.send_mail()

        messages.info(
            self.request, 'You have signed up successfully.'
        )
        return response


class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address
    fields = [
        'name',
        'address1',
        'address2',
        'zip_code',
        'city',
        'country',
    ]
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = [
        'name',
        'address1',
        'address2',
        'zip_code',
        'city',
        'country',
    ]
    success_url = reverse_lazy('address_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = [
        'name',
        'address1',
        'address2',
        'zip_code',
        'city',
        'country',
    ]
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def add_to_basket(request):
    product = get_object_or_404(models.Product, pk=request.GET.get('product_id'))
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session['basket_id'] = basket.id

    basketline, created = models.BasketLine.objects.get_or_create(basket=basket, product=product)
    if not created:
        basketline.quantity += 1
        basketline.save()
    return HttpResponseRedirect(reverse('product', args=(product.slug,)))


def manage_basket(request):
    if not request.basket:
        return render(request, 'main/basket.html', {'formset': None})
    if request.method == 'POST':
        formset = forms.BasketLineFormSet(request.POST, instance=request.basket)
        if formset.is_valid():
            formset.save()
    else:
        formset = forms.BasketLineFormSet(instance=request.basket)

    if request.basket.is_empty():
        return render(request, 'main/basket.html', {'formset': None})
    return render(request, 'main/basket.html', {'formset': formset})
