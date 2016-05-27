from django.contrib import admin
from .models import Order, OrderItem
from django.core.urlresolvers import reverse
# imports для создания админского action
import csv
import datetime
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    meta_options = modeladmin.model._meta

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(meta_options.verbose_name)

    writer = csv.writer(response)

    fields = [field for field in meta_options.get_fields() if not field.many_to_many and not field.one_to_many]

    # записываем информацию из header (названия полей таблицы)
    writer.writerow([field.verbose_name for field in fields])
    # записываем данные выбраных строк
    for obj in queryset:
        data_row = []
        for field in fields:
            cell_value = getattr(obj, field.name)

            # если значение ячейки будет экземпляром типа datetime
            # то мы превращаем объект даты в строку
            # потому що все данные в CSV файле должны соответствовать строковому типу
            if isinstance(cell_value, datetime.datetime):
                cell_value = cell_value.strftime('%d/%m/%Y')

            data_row.append(cell_value)
        writer.writerow(data_row)
    return response

# название действия, отображаемое в админке
export_to_csv.short_desription = _('Import to CSV')



def order_detail(obj):
    return "<a href='{}'>View</a>".format(reverse('orders:admin_order_detail', args=[obj.id]))
# разрешить HTML тэги
order_detail.allow_tags = True



def order_pdf(obj):
    return "<a href='{}'>PDF</a>".format(reverse('orders:admin_order_pdf', args=[obj.id]))
order_pdf.allow_tags = True
order_pdf.short_desription = _('PDF file')



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'first_name',
                    'last_name',
                    'email',
                    'address',
                    'postal_code',
                    'city',
                    'paid',
                    'created',
                    'updated',
                    order_detail,
                    order_pdf
                    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    #добавляем action
    actions = [export_to_csv]



admin.site.register(Order, OrderAdmin)

