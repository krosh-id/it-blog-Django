from django import forms

PAY_CHOICE = (
    ("CREDIT_CART", "Кредитная карта"),
    ("DEBIT_CART", "Дебетовая карта"),
    ("PAYPAL", "PayPal"),
    ("YANDEX_PAY", "Яндекс Pay"),
)


class OrderForm(forms.Form):

    first_name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50,  label="Фамилия")
    mobile_number = forms.CharField(max_length=13,  label="Номер телефона")
    email = forms.EmailField(max_length=50,  label="Почта")
    address = forms.CharField(max_length=100,  label="Адрес")

    pay_by = forms.ChoiceField(choices=PAY_CHOICE,
                               widget=forms.Select(attrs={"class": "radio-input"}),
                               label="Способ оплаты")
    name_on_cart = forms.CharField(max_length=100, label="Имя на карте")
    number_cart = forms.CharField(max_length=16, label="Номер карты")
    validate_period = forms.CharField(max_length=5, label="Срок действия")
    cvv = forms.IntegerField(min_value=0, max_value=999)
