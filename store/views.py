from django.contrib.auth import login
from .forms import RegistrationFrom, CheckoutForm
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction


from .models import Product, Customer, Order



def home(request):
    featured_products = Product.objects.filter(featured=True)


    context = {
        "featured_products": featured_products,
    }
    return render(request, "store/home.html", context)




def product_list(request):
    products = Product.objects.all()


    search_query = request.GET.get("search", "")
    selected_category = request.GET.get("category", "")


    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
        )


    if selected_category:
        products = products.filter(category=selected_category)


    context = {
        "products": products,
        "categories": Product.CATEGORY_CHOICES,
        "search_query": search_query,
        "selected_category": selected_category,
    }
    return render(request, "store/product_list.html", context)




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)


    context = {
        "product": product,
    }
    return render(request, "store/product_detail.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("store:home")

    if request.method == "POST":
        form = RegistrationFrom(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account was created successfully.",
            )
        return redirect("store:home")

    else:
        form = RegistrationFrom()

        context = {
            "form": form,
        }
    return render(request, "store/register.html", context)



@login_required
def cart_detail(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())


    cart_items = []
    total_price = Decimal("0.00")


    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total_price += subtotal


        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )


    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "store/cart.html", context)




@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})


    product_key = str(product.id)
    current_quantity = cart.get(product_key, 0)


    if product.quantity == 0:
        messages.error(request, "This product is out of stock.")


    elif current_quantity >= product.quantity:
        messages.warning(
            request,
            "You cannot add more than the available quantity.",
        )


    else:
        cart[product_key] = current_quantity + 1
        request.session["cart"] = cart
        request.session.modified = True


        messages.success(
            request,
            f"{product.name} was added to your cart.",
        )


    return redirect("store:cart")




@login_required
@require_POST
def increase_cart_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    product_key = str(product.id)


    if product_key in cart:
        if cart[product_key] < product.quantity:
            cart[product_key] += 1
            request.session["cart"] = cart
            request.session.modified = True
        else:
            messages.warning(
                request,
                "No more stock is available for this product.",
            )


    return redirect("store:cart")




@login_required
@require_POST
def decrease_cart_quantity(request, product_id):
    cart = request.session.get("cart", {})
    product_key = str(product_id)


    if product_key in cart and cart[product_key] > 1:
        cart[product_key] -= 1
        request.session["cart"] = cart
        request.session.modified = True


    return redirect("store:cart")




@login_required
@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_key = str(product_id)


    if product_key in cart:
        del cart[product_key]
        request.session["cart"] = cart
        request.session.modified = True


        messages.success(
            request,
            "The product was removed from your cart.",
        )


    return redirect("store:cart")

@login_required
def checkout(request):
    cart = request.session.get("cart", {})


    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("store:cart")


    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = Decimal("0.00")


    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total_price += subtotal


        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )


    existing_customer = Customer.objects.filter(
        user=request.user
    ).first()


    if request.method == "POST":
        form = CheckoutForm(
            request.POST,
            instance=existing_customer,
        )


        if form.is_valid():
            for item in cart_items:
                if item["quantity"] > item["product"].quantity:
                    messages.error(
                        request,
                        f"Not enough stock for {item['product'].name}.",
                    )
                    return redirect("store:cart")


            with transaction.atomic():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()


                for item in cart_items:
                    product = item["product"]
                    quantity = item["quantity"]
                    subtotal = item["subtotal"]


                    Order.objects.create(
                        customer=customer,
                        product=product,
                        quantity=quantity,
                        total_price=subtotal,
                    )


                    product.quantity -= quantity
                    product.save(update_fields=["quantity"])


            request.session["cart"] = {}
            request.session.modified = True


            return redirect("store:order_success")
    else:
        initial_data = {}


        if existing_customer is None:
            initial_data["name"] = (
                request.user.get_full_name()
                or request.user.username
            )


        form = CheckoutForm(
            instance=existing_customer,
            initial=initial_data,
        )


    context = {
        "form": form,
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "store/checkout.html", context)




@login_required
def order_success(request):
    return render(request, "store/order_success.html")
