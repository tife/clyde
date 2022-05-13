odoo.define("vixo_add_to_quotation.website_sale", function (require) {

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.oe_website_sale_custom = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'change #customer_note': '_onChangeCustomerNote',
            'change #customer_ref': '_onChangeCustomerRef',
            'change #order_project_name': '_onChangeProjectName',
        },

        init: function () {
            this._super.apply(this, arguments);
        },

        _onChangeCustomerNote: function (ev) {
            ajax.jsonRpc("/update/customer/notes", 'call', {
                'sale_order_line_id': $(ev.currentTarget).data('order_line_id'),
                'value': $(ev.currentTarget).val(),
            }).then(function (data) {
            })
        },
        _onChangeCustomerRef: function (ev) {
            ajax.jsonRpc("/update/customer/ref", 'call', {
                'sale_order_line_id': $(ev.currentTarget).data('order_line_id'),
                'value': $(ev.currentTarget).val(),
            }).then(function (data) {
            })
        },
        _onChangeProjectName: function (ev) {
        console.log(">>>>>>>>>>Dsadas")
            ajax.jsonRpc("/update/project/name", 'call', {
                'sale_order_id': $(ev.currentTarget).data('order_id'),
                'value': $(ev.currentTarget).val(),
            }).then(function (data) {
            })
        },
    });

});