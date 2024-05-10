from django.shortcuts import render
from website.forms import ContactForm, NewsletterForm
from django.http.response import HttpResponseRedirect
from django.contrib import messages

def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        # creating a copy of the POST data
        dummy_form = request.POST
        copy_dummy_form = dummy_form.copy()
        # modifying the value of the 'name' field in the copied data
        copy_dummy_form['name'] = 'unknown'
        # re-initializing the form with the modified data
        form = ContactForm(copy_dummy_form)
        if form.is_valid():
            # saving the data to the database
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your ticket has been submitted successfully!')
        else:
            messages.add_message(request, messages.ERROR, 'Your ticket has not been submitted successfully!')
    
    form = ContactForm()
    return render(request, 'website/contact.html', {'form':form})

def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your ticket has been submitted successfully!')
            return HttpResponseRedirect('/')
    else:
        messages.add_message(request, messages.ERROR, 'Your ticket has not been submitted successfully!')
        return HttpResponseRedirect('/')


