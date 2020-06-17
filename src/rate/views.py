import csv

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView, View

import rate.model_choices as mch
from rate.models import Rate
from rate.utils import display
from rate.utils import generate_rate_cache_key

import xlsxwriter


class RateList(ListView):
    paginate_by = 15
    queryset = Rate.objects.all()
    template_name = 'list_all.html'


class LatestRatesView(TemplateView):

    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object_list = []
        for source in mch.SOURCE_CHOICES:  # source
            source = source[0]
            for currency in mch.CURRENCY_TYPE_CHOICE:  # currency_type
                currency = currency[0]
                for type_ in mch.CURRENCY_TYPE_CHOICE:  # type
                    type_ = type_[0]

                    rate = Rate.objects.filter(
                        source=source,
                        type=type_,
                        currency_type=currency,
                    ).last()
                    if rate is not None:
                        object_list.append(rate)

        context['object_list'] = object_list
        return context


class RateDownloadCSV(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'amount',
        'type',
    )
    queryset = Rate.objects.all().iterator()

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = self.get_response()

        writer = csv.writer(response)
        writer.writerow(self.__class__.HEADERS)

        for rate in self.queryset:
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))

            writer.writerow(values)

        return response

    def get_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rate.csv"'
        return response


class RateDownloadXLSX(View):
    HEADERS = (
        'id',
        'created',
        'amount',
        'source',
        'currency_type',
        'type',
    )

    queryset = Rate.objects.all()

    def get(self, request):
        response = self.get_response

        book = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet = book.add_worksheet()

        for i, column in enumerate(self.__class__.HEADERS):
            sheet.write(0, i, column)

        for i, amount in enumerate(self.queryset, start=1):
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(amount, attr))

            for j, value in enumerate(values):
                sheet.write(i, j, value)

        book.close()

        return response

    @property
    def get_response(self):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=r.xlsx"
        return response


class LatestRate(TemplateView):
    template_name = "latest_rates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rates = []
        for bank in mch.SOURCE_CHOICES:
            source = bank[0]
            for curr in mch.CURRENCY_TYPE_CHOICE:
                currency_type = curr[0]
                cache_key = generate_rate_cache_key(source, currency_type)

                rate = cache.get(cache_key)
                if rate is None:
                    rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('created').last()
                    if rate:
                        rate_dict = {
                            'currency_type': rate.currency_type,
                            'source': rate.source,
                            'amount': rate.amount,
                            'created': rate.created,
                        }
                        rates.append(rate_dict)
                        cache.set(cache_key, rate_dict, 60*15)
                else:
                    rates.append(rate)
        context["rates"] = rates
        return context


class EditRate(UserPassesTestMixin, UpdateView):
    template_name = 'edit-rate.html'
    model = Rate
    fields = 'amount', 'source', 'currency_type', 'type'
    success_url = reverse_lazy('rate:list')

    def test_func(self):
        return self.request.user.is_authenticated and\
            self.request.user.is_superuser


class DeleteRate(UserPassesTestMixin, DeleteView):
    model = Rate
    success_url = reverse_lazy('rate:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.is_superuser
