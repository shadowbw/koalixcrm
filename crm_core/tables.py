import django_tables2 as tables
from crm_core.custom.custom_columns import LabelColumn, ButtonsColumn, RelatedModelDetailLinkColumn, \
    ModelDetailLinkColumn, IncludeColumn
from crm_core.models import Contract, Customer, Supplier, Product, TaxRate, CustomerBillingCycle, Unit, \
    ProductCategory, CustomerGroup
from django.utils.translation import ugettext_lazy as _


class ContractTable(tables.Table):
    state = LabelColumn(verbose_name=_('Status'))
    name = ModelDetailLinkColumn(verbose_name=_('Name'))
    default_customer = RelatedModelDetailLinkColumn(accessor='default_customer.name', verbose_name=_('Customer'))
    description = tables.Column()
    price = tables.TemplateColumn("{{ record.get_price }}", accessor='prices.price', verbose_name=_('Price'))
    lastmodification = tables.DateTimeColumn()

    quote = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_quote_detail_url }}'",
                "condition": "record.has_quotes",
            },
            {
                "extra_class": 'btn-primary',
                "gl_icon": 'pencil',
                "onclick": "location.href='{{ record.get_quote_edit_url }}'",
                "condition": "record.has_quotes",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    purchase_order = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_purchaseorder_detail_url }}'",
                "condition": "record.has_purchaseorders",
            },
            {
                "extra_class": "btn-success",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_purchaseorder_edit_url }}'",
                "condition": "record.has_purchaseorders",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    invoice = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_invoice_detail_url }}'",
                "condition": "record.has_invoices",
            },
            {
                "extra_class": "btn-warning",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_invoice_edit_url }}'",
                "condition": "record.has_invoices",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    edit_status = IncludeColumn(
        'crm_core/includes/contract_row_actions_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )
    edit_contract = IncludeColumn(
        'crm_core/includes/contract_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Contract
        exclude = ('id', 'staff', 'default_supplier', 'default_currency', 'dateofcreation', 'lastmodifiedby')
        sequence = ('state', 'name', 'default_customer', 'description', 'price', 'lastmodification')
        order_by = ('state', '-lastmodification')


class CustomerTable(tables.Table):
    name_prefix = tables.TemplateColumn("""{{ record.get_prefix }}""", accessor='-prefix', verbose_name=_('Prefix'))
    new_contract = IncludeColumn(
        'crm_core/includes/customer_row_actions_toolbar.html',
        attrs={"th": {"width": "50px"}},
        verbose_name=" ",
        orderable=False
    )
    edit_customer = IncludeColumn(
        'crm_core/includes/customer_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Customer
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'contact_ptr')
        sequence = ('name_prefix', 'firstname', 'name', 'default_currency')
        order_by = ('name', 'firstname')


class SupplierTable(tables.Table):
    name = ModelDetailLinkColumn(accessor='name')
    edit_supplier = IncludeColumn(
        'crm_core/includes/supplier_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Supplier
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'contact_ptr')
        sequence = ('name', 'default_currency')
        order_by = ('name', )


class ProductTable(tables.Table):
    product = tables.TemplateColumn("<a href='{{ record.get_absolute_url }}'>{{ record.get_product_number }}</a>",
                                    accessor='product_number', verbose_name="#")
    price = tables.TemplateColumn("{{ record.get_price }}", accessor='prices.price', verbose_name=_('Price'))
    edit_product = IncludeColumn(
        'crm_core/includes/product_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Product
        exclude = ('id', 'item_category', 'item_prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'product_number', 'productitem_ptr')
        sequence = ('product', 'item_title', 'item_description', 'item_unit', 'price', 'item_tax')


class TaxTable(tables.Table):
    edit_tax = IncludeColumn(
        'crm_core/includes/tax_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = TaxRate
        exclude = ('id', )


class BillingCycleTable(tables.Table):
    edit_billingcycle = IncludeColumn(
        'crm_core/includes/billingcycle_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerBillingCycle
        exclude = ('id', )


class UnitTable(tables.Table):
    edit_unit = IncludeColumn(
        'crm_core/includes/unit_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Unit
        exclude = ('id', )


class ProductCategoryTable(tables.Table):
    edit_productcategory = IncludeColumn(
        'crm_core/includes/productcategory_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = ProductCategory
        exclude = ('id', )


class CustomerGroupTable(tables.Table):
    edit_customergroup = IncludeColumn(
        'crm_core/includes/customergroup_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerGroup
        exclude = ('id', )