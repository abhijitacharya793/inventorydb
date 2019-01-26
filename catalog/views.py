from django.shortcuts import render

# Create your views here.
from catalog.models import Item, Manufacturer, ItemInstance, Itemtype

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_items = Item.objects.all().count()
    num_instances = ItemInstance.objects.all().count()

    # Available items (status = 'a')
    num_instances_available = ItemInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_manufacturers = Manufacturer.objects.count()

    context = {
        'num_items': num_items,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_manufacturers': num_manufacturers,
    }

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_items': num_items,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_manufacturers': num_manufacturers,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class ItemListView(generic.ListView):
    model = Item
    paginate_by = 10

class ItemDetailView(generic.DetailView):
    model = Item
    paginate_by = 10

class ManufacturerListView(generic.ListView):
    model = Manufacturer
    paginate_by = 10

class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer
    paginate_by = 10

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedItemsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing items on loan to current user."""
    model = ItemInstance
    template_name ='catalog/iteminstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ItemInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewItemForm

@permission_required('catalog.can_mark_returned')
def renew_item_inventoryhead(request, pk):
    """View function for renewing a specific ItemInstance by inventoryhead."""
    item_instance = get_object_or_404(ItemInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewItemForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            item_instance.due_back = form.cleaned_data['renewal_date']
            item_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewItemForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'item_instance': item_instance,
    }

    return render(request, 'catalog/item_renew_inventoryhead.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Manufacturer

class ManufacturerCreate(CreateView):
    model = Manufacturer
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}

class ManufacturerUpdate(UpdateView):
    model = Manufacturer
    fields = ['company_name', 'address']#, 'date_of_birth', 'date_of_death']

class ManufacturerDelete(DeleteView):
    model = Manufacturer
    success_url = reverse_lazy('manufacturers')
