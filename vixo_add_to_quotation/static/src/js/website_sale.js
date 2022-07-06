odoo.define("vixo_add_to_quotation.website_sale", function (require) {

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.oe_website_sale_custom = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'change #customer_note': '_onChangeCustomerNote',
            'change #customer_ref': '_onChangeCustomerRef',
            'change #order_project_name': '_onChangeProjectName',
            'change .custom-control-input.js_variant_change': '_onChangeAttributes',
        },

        init: function () {
            this._super.apply(this, arguments);
             setTimeout(function () {
                if($('input:checked', '.custom-control.custom-radio')){
                    $('input:checked', '.custom-control.custom-radio').each(function( index,e ) {
                        $("span.attribute_class[data-value_id='" + $(this).val() + "']").show();
                    });
                }}, 1000);
             $('.recommended-product').owlCarousel({
                loop:false,
                margin:10,
                nav:true,
                navText : ["<i class='fa fa-2x fa-chevron-circle-left'></i>","<i class='fa fa-2x fa-chevron-circle-right'></i>"],
                responsive:{
                    0:{
                        items:1
                    },
                    600:{
                        items:2,
                        slideBy: 2
                    },
                    1000:{
                        items:4,
                        slideBy: 4
                    }
                }
            })

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
            ajax.jsonRpc("/update/project/name", 'call', {
                'sale_order_id': $(ev.currentTarget).data('order_id'),
                'value': $(ev.currentTarget).val(),
            }).then(function (data) {
            })
        },
        _onChangeAttributes: function (ev) {
            $($(ev.target).parent().parent().parent().parent().parent()).find('.attribute_class').hide()
            $("span.attribute_class[data-value_id='" + $(ev.target).val() + "']").show();
        },
    });

});