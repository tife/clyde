odoo.define('vido_add_to_quotation.post_processing', function (require){
    "use strict";
    // require original module JS
    //var payment = require('payment.post_processing');
    var publicWidget = require('web.public.widget');
    
    // Extend widget
    /*
    payment.WeeklyTimesheet.include({
        ....
        your code to override here    
        ....
    });
    */

    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.PaymentPostProcessing.include({
        displayLoading: function () {
            //console.log("hihi");
            var msg = _t("We are processing your order, please wait ...");
            $.blockUI({
                'message': '<h2 class="text-white"><img src="/web/static/img/spin.png" class="fa-pulse"/>' +
                    '    <br />' + msg +
                    '</h2>'
            });

        }
    });
    
});