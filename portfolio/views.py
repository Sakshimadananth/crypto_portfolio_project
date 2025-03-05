from django.shortcuts import render

# Create your views here.
# portfolio/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.views.decorators.http import require_POST
from .utils import fetch_crypto_data

from .forms import RegistrationForm, AddCryptoForm

from .models import Portfolio
from django.http import JsonResponse
from .utils import get_eth_balance
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_eth_transaction
from django.shortcuts import render


def analysis_view(request):
    return render(request, 'portfolio/analysis.html')


def wallet_balance_page(request):
    """Render the wallet balance form page."""
    return render(request, 'wallet_balance.html')


@csrf_exempt
def send_crypto(request):
    """API to send Ethereum transactions."""
    if request.method == 'POST':
        data = json.loads(request.body)
        from_address = data.get('from_address')
        private_key = data.get('private_key')
        to_address = data.get('to_address')
        amount = data.get('amount')

        try:
            tx_hash = send_eth_transaction(from_address, private_key, to_address, amount)
            return JsonResponse({"status": "success", "transaction_hash": tx_hash})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


def wallet_balance(request, wallet_address):
    """API to fetch Ethereum wallet balance."""
    try:
        balance = get_eth_balance(wallet_address)
        return JsonResponse({"wallet_address": wallet_address, "eth_balance": balance})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to home page after successful registration
            return redirect('holdings_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# login



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to holdings list after successful login
            return redirect(reverse_lazy('holdings_list'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# logout
#@require_POST
# def user_logout(request):
#     logout(request)
#     # Redirect to the home page after logout
#     return redirect(reverse('holdings_list'))
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('holdings_list'))  
# @require_POST
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('login'))
# @require_POST
# def user_logout(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect(reverse('login'))
#     else:
#         return render(request, 'error.html', {'message': 'Invalid request method'})
@require_POST
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('login'))
    # Handle GET requests here if needed
    return redirect(reverse('login'))  # Redirect to login page on GET requests
# homepage data
# views.py
from .forms import RegistrationForm, AddCryptoForm, SearchForm

# def holdings_list(request):
#     search_form = SearchForm(request.GET)
#     query = search_form.cleaned_data.get('query') if search_form.is_valid() else ''
    
#     crypto_data = fetch_crypto_data()
#     holdings = [
#         {
#             "cryptocurrency": data["name"],
#             "image": data["image"],
#             "symbol": data["symbol"],
#             "current_price": data["current_price"],
#             "market_cap": data["market_cap"],
#             "market_cap_rank": data["market_cap_rank"],
#             "fully_diluted_valuation": data["fully_diluted_valuation"],
#             "total_volume": data["total_volume"],
#             "high_24h": data["high_24h"],
#             "low_24h": data["low_24h"],
#             "price_change_24h": data["price_change_24h"],
#             "price_change_percentage_24h": data["price_change_percentage_24h"],
#             "market_cap_change_24h": data["market_cap_change_24h"],
#             "market_cap_change_percentage_24h": data["market_cap_change_percentage_24h"],
#             "circulating_supply": data["circulating_supply"],
#             "total_supply": data["total_supply"],
#             "max_supply": data["max_supply"],
#             "ath": data["ath"],
#             "ath_change_percentage": data["ath_change_percentage"],
#             "ath_date": data["ath_date"],
#             "atl": data["atl"],
#             "atl_change_percentage": data["atl_change_percentage"],
#             "atl_date": data["atl_date"],
#             "roi": data["roi"],
#             "last_updated": data["last_updated"],
#             "purchase_price": 0,
#             "purchase_date": None
#         }
#         for data in crypto_data
#         if query.lower() in data["name"].lower()  # Filter by search query
#     ]
#     return render(request, 'portfolio/holdings_list.html', {'holdings': holdings, 'search_form': search_form})
# def holdings_list(request):
#     search_form = SearchForm(request.GET)
#     query = search_form.cleaned_data.get('query') if search_form.is_valid() else ''
    
#     # Fetch the currency parameter; default is 'inr'
#     currency = request.GET.get('currency', 'inr')
#     crypto_data = fetch_crypto_data(currency)  # Pass currency to the fetch function
    
#     holdings = [
#         {
#             "cryptocurrency": data["name"],
#             "image": data["image"],
#             "symbol": data["symbol"],
#             "current_price": data["current_price"],
#             "market_cap": data["market_cap"],
#             "market_cap_rank": data["market_cap_rank"],
#             "fully_diluted_valuation": data["fully_diluted_valuation"],
#             "total_volume": data["total_volume"],
#             "high_24h": data["high_24h"],
#             "low_24h": data["low_24h"],
#             "price_change_24h": data["price_change_24h"],
#             "price_change_percentage_24h": data["price_change_percentage_24h"],
#             "market_cap_change_24h": data["market_cap_change_24h"],
#             "market_cap_change_percentage_24h": data["market_cap_change_percentage_24h"],
#             "circulating_supply": data["circulating_supply"],
#             "total_supply": data["total_supply"],
#             "max_supply": data["max_supply"],
#             "ath": data["ath"],
#             "ath_change_percentage": data["ath_change_percentage"],
#             "ath_date": data["ath_date"],
#             "atl": data["atl"],
#             "atl_change_percentage": data["atl_change_percentage"],
#             "atl_date": data["atl_date"],
#             "roi": data["roi"],
#             "last_updated": data["last_updated"],
#             "purchase_price": 0,
#             "purchase_date": None
#         }
#         for data in crypto_data
#         if query.lower() in data["name"].lower()  # Filter based on the search query
#     ]
#     return render(request, 'portfolio/holdings_list.html', {
#         'holdings': holdings,
#         'search_form': search_form,
#         'currency': currency  # Pass the selected currency to the template
#     })
# def holdings_list(request):
#     search_form = SearchForm(request.GET)
#     query = search_form.cleaned_data.get('query') if search_form.is_valid() else ''

#     # Fetch the currency parameter; default is 'inr'
#     currency = request.GET.get('currency', 'inr').lower()
#     currency_symbols = {"inr": "₹", "usd": "$", "eur": "€"}
#     symbol = currency_symbols.get(currency, "₹")

#     crypto_data = fetch_crypto_data(currency=currency)

#     holdings = [
#         {
#             "cryptocurrency": data["name"],
#             "image": data["image"],
#             "symbol": data["symbol"],
#             "current_price": data["current_price"],
#             "market_cap": data["market_cap"],
#             "market_cap_rank": data["market_cap_rank"],
#             "fully_diluted_valuation": data["fully_diluted_valuation"],
#             "total_volume": data["total_volume"],
#         }
#         for data in crypto_data if query.lower() in data["name"].lower()
#     ]
#     return render(request, 'portfolio/holdings_list.html', {
#         'holdings': holdings,
#         'search_form': search_form,
#         'currency': currency,
#         'symbol': symbol
#     })

def holdings_list(request):
    search_form = SearchForm(request.GET)
    query = search_form.cleaned_data.get('query') if search_form.is_valid() else ''

    # Fetch the currency parameter; default to 'inr'
    # currency = request.GET.get('currency', 'inr').lower()
    # currency_symbols = {"inr": "₹", "usd": "$", "eur": "€"}  # Currency to symbol mapping
    # symbol = currency_symbols.get(currency, "₹")  # Default to INR symbol
    currency = request.GET.get('currency', 'inr').lower()
    currency_symbols = {"inr": "₹", "usd": "$", "eur": "€"}  # Mapping
    symbol = currency_symbols.get(currency, "₹")  # Get the correct symbol


    # Fetch cryptocurrency data with the selected currency
    crypto_data = fetch_crypto_data(currency=currency)

    holdings = [
        {
            "cryptocurrency": data["name"],
            "image": data["image"],
            "symbol": data["symbol"],
            "current_price": data["current_price"],
            "market_cap": data["market_cap"],
            "market_cap_rank": data["market_cap_rank"],
            "fully_diluted_valuation": data["fully_diluted_valuation"],
            "total_volume": data["total_volume"],
        }
        for data in crypto_data if query.lower() in data["name"].lower()
    ]

    return render(request, 'portfolio/holdings_list.html', {
    'holdings': holdings,
    'search_form': search_form,
    'currency': currency,
    'symbol': symbol
})



# add new crypto in their portfolio
@login_required
def add_to_portfolio(request):
    if request.method == 'POST':
        form = AddCryptoForm(request.POST)
        if form.is_valid():
            # Create a new Portfolio instance and associate it with the authenticated user
            portfolio = Portfolio(
                user=request.user,
                image=form.cleaned_data['image'],
                cryptocurrency=form.cleaned_data['cryptocurrency'],
                symbol=form.cleaned_data['symbol'],
                quantity=form.cleaned_data['quantity'],
                purchase_price=form.cleaned_data['purchase_price'],
                purchase_date=form.cleaned_data['purchase_date']
            )
            # Save the portfolio instance
            portfolio.save()
            # Redirect to holdings list after adding the cryptocurrency
            return redirect('portfolio')
    else:
        form = AddCryptoForm()
    return render(request, 'portfolio/portfolio.html', {'form': form})

# own portfolio
@login_required
def portfolio(request):
    # Retrieve the user's portfolio data
    user_portfolio = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolio/portfolio.html', {'portfolio': user_portfolio})
