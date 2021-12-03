from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views.generic import ListView, View

from bot.forms import BotRentalPropForm
from .utils import run_bot_logic, CreatePdfMixin, ProcessReportMixin
from .models import BotRentalReport
from calculator.models import UserSettings


@login_required
def run_bot(request):
    """Run bot and save model objects of data"""
    run_bot_logic(request.user)
    return redirect('bot:bot-reports')
    
@method_decorator(login_required, name='dispatch')
class BotReport(ProcessReportMixin, View):
    """The report Page"""
    model = BotRentalReport
    template = 'bot/bot_report.html'

@method_decorator(login_required, name='dispatch')
class BotReportsView(ListView):
    """Page for listing all bot reports"""
    model = BotRentalReport
    template_name = 'bot/bot_reports.html'
    paginate_by = 5
    context_object_name = 'bot_object_list'

    def get_queryset(self):
        return BotRentalReport.objects.filter(owner=self.request.user).order_by('-updated_at')

@login_required
def bot_delete_report(request, pk):
    """Delete report"""
    try:
        report = BotRentalReport.objects.get(id=pk)
    except:
        raise Http404
    if report.owner != request.user:
        raise Http404

    usr_settings = UserSettings.objects.get(user=request.user)

    if getattr(usr_settings, 'blacklist_bool'):
        addr = getattr(report, 'prop_address')
        city = getattr(report, 'prop_city')
        state = getattr(report, 'prop_state')
        zipcode = getattr(report, 'prop_zip')

        current_json = getattr(usr_settings, 'addr_blacklist')

        if not f'{addr} {city}, {state} {zipcode}' in current_json[request.user.username]['addresses']:
            new_json = current_json[request.user.username]['addresses']
            new_json.append(f'{addr} {city}, {state} {zipcode}')
        else: 
            new_json = current_json[request.user.username]['addresses']

        obj, _ = UserSettings.objects.update_or_create(
            user=request.user,
            defaults={'addr_blacklist': {
                    request.user.username: {
                        'addresses': new_json,
                    }
                } 
            }
        )

    report.delete()
    return redirect('bot:bot-reports')

@login_required
def bot_edit_rental_prop_calc(request, pk):
    """Edit a report"""
    try:
        item = BotRentalReport.objects.get(id=pk)
    except:
        raise Http404
    if item.owner != request.user:
        raise Http404
    if request.method == 'POST':
        # Initial request; pre-fill form with the current entry.
        form = BotRentalPropForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(f'/bot/bot-report/{pk}')

    else:
        # POST data submitted; process data.
        form = BotRentalPropForm(instance=item)

    # Display a blank or invalid form.
    context = {'item': item,'form': form}
    return render(request, 'bot/bot_calculator.html', context)

@method_decorator(login_required, name='dispatch')
class ViewBotReportPDF(CreatePdfMixin, View):
    """Renders PDF of report data"""
    model = BotRentalReport
    template = 'calculator/report_pdf.html'