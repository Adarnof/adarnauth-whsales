from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_extras.contrib.auth.shortcuts import get_owned_object_or_40x
from eve_sso.decorators import token_required
from whsales.models import User, Listing, System
from whsales.forms import ListingAddForm, ListingSearchForm
import requests

LISTINGS_PER_PANEL_PAGE = 12
LISTINGS_PER_LIST_PAGE = 30

def get_page(model_list, per_page, page_num):
    p = Paginator(model_list, per_page)
    try:
        listings = p.page(page_num)
    except PageNotAnInteger:
        listings = p.page(1)
    except EmptyPage:
        listings = p.page(p.num_pages)
    return listings

@token_required(new=True)
def login_view(request, tokens):
    token = tokens[0]
    user = authenticate(token=token)
    if user.is_active:
        login(request, user)
        token.delete()
        return redirect(listings_panel)
    return render(request, 'error.html', context={'error':'Your account has been disabled.'})

@login_required
def logout_view(request):
    logout(request)
    return redirect(listings_panel)

def listings_panel(request):
    all_listings = Listing.objects.filter(sold__isnull=True).order_by('-created')
    page = request.GET.get('page', 1)
    listings = get_page(all_listings, LISTINGS_PER_PANEL_PAGE, page)
    return render(request, 'listings_panel.html', context={'page_obj':listings})

def listings_list(request):
    all_listings = Listing.objects.filter(sold__isnull=True).order_by('-created')
    page = request.GET.get('page', 1)
    listings = get_page(all_listings, LISTINGS_PER_LIST_PAGE, page)
    return render(request, 'listings_list.html', context={'page_obj':listings})

def listings_sold(request):
    all_listings = Listing.objects.filter(sold__isnull=False).order_by('-created')
    page = request.GET.get('page', 1)
    listings = get_page(all_listings, LISTINGS_PER_LIST_PAGE, page)
    return render(request, 'listings_panel.html', context={'page_obj':listings})

def listing_view(request, id):
    listing = get_object_or_404(Listing, pk=id)
    return render(request, 'single_listing.html', context={'listing': listing})

@login_required
def mark_sold(request, id):
    listing = get_owned_object_or_40x(Listing, request.user, pk=id)
    if not listing.sold:
        listing.mark_sold()
    return redirect(listing_view, id)

@login_required
def delete_listing(request, id):
    listing = get_owned_object_or_40x(Listing, request.user, pk=id)
    if not listing.sold:
        listing.delete()
        return redirect(listings_panel)
    return redirect(listing_view, id)

@login_required
def my_listings(request):
    all_listings = Listing.objects.owned_by(request.user).order_by('-created')
    page = request.GET.get('page', 1)
    listings = get_page(all_listings, LISTINGS_PER_LIST_PAGE, page)
    return render(request, 'listings_list.html', context={'page_obj':listings})

@login_required
@token_required(scopes=['characterLocationRead'])
def select_token(request, tokens):
    return render(request, 'tokens.html', context={'tokens': tokens})

@login_required
@token_required(new=True, scopes=['characterLocationRead'])
def add_token(request, tokens):
    return redirect(select_token)

@login_required
@token_required(scopes=['characterLocationRead'])
def post_listing(request, tokens, token_pk):
    token = get_object_or_404(tokens, pk=token_pk)
    if request.method == 'POST':
       form = ListingAddForm(request.POST)
       if form.is_valid():
           listing = form.save(commit=False)
           listing.owner = request.user
           listing.save()
           return redirect(listing_view, listing.pk)
       else:
           return render(request, 'form.html', context={'form': form})
    else:
        custom_headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get('https://crest-tq.eveonline.com/characters/%s/location/' % token.character_id, headers=custom_headers)
        try:
            r.raise_for_status()
        except:
            token.delete()
            return redirect(select_token)
        if r.json():
            system_id = r.json()['solarSystem']['id']
            try:
                system = System.objects.get(id=system_id)
                form = ListingAddForm(initial={'system_id':system.id,'system_name':system.name, 'system':system})
                return render(request, 'form.html', context={'form': form})
            except System.DoesNotExist:
                error = "Your character is not in a recognized wormhole system."
        else:
            error = "Your character must be in-game to determine its location."
        return render(request, 'error.html', context={'error': error})

def search(request):
    if request.method == 'POST':
        form = ListingSearchForm(request.POST)
        if form.is_valid():
            qs = System.objects.all()
            if form.cleaned_data['wormhole_class']:
                qs = qs.filter(wormhole_class=form.cleaned_data['wormhole_class'])
            if form.cleaned_data['system_name']:
                qs = qs.filter(name=form.cleaned_data['system_name'])
            if form.cleaned_data['effect']:
                qs = qs.filter(effect=form.cleaned_data['effect'])
            if form.cleaned_data['statics']:
                qs = qs.filter(statics__in=form.cleaned_data['statics'])
            if form.cleaned_data['shattered']:
                qs = qs.filter(shattered=True)
            else:
                qs = qs.filter(shattered=False)
            listings = Listing.objects.filter(system__in=qs).order_by('-created')
            if not form.cleaned_data['include_sold']:
                listings = listings.exclude(sold__isnull=False)
            page = get_page(listings, listings.count()+1, 1)
            return render(request, 'listings_list.html', context={'page_obj': page})            
    else:
        form = ListingSearchForm()
    return render(request, 'form.html', context={'form': form})

def about(request):
    return render(request, 'about.html')
