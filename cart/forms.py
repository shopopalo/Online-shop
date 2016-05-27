from django import forms
from django.utils.translation import gettext_lazy as _


# выпадающий список с указанием количества товара (1-20)
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

# форма для обновления количества товара в корзине
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                label=_('Quantity'))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
