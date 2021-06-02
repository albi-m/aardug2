odoo.define('website_email_snippet.email_mail_send', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    var ajax = require('web.ajax');

    ajax.jsonRpc("/render/template", 'call', {
        'model': 'ir.ui.view',
        'method': 'read_template'
    }).then(function(data){
        if(data.partner_bottom_template != ""){
            var partner_bottom = data.partner_bottom_template
            $('#wrapwrap').append(partner_bottom)
        }
    })

    $(document).ready(function(){
        $('.a-pricelist-download').on('click', function (ev) {
            var parent = $(ev.currentTarget.parentElement.parentElement);
            var email = parent.find("input[name='name']");
            if(!email.val().includes('@') && !email.val().includes('.')){
                alert(_t("Please enter a valid email address"));
            }
            else {
                $('.email_form').ajaxSubmit({
                    url: '/website_form/email/submit',
                    data: {},
                    success: function (data) {
                        $('input[name="name"]')[0].value = ''
                        email[0].parentElement.appendChild($("<span class='text-success row ml4'>De e-mail is verstuurd!</span>")[0])
                        location.href='/prijslijst-bedankt';
                    }
                });
            }
        });
    });
});

