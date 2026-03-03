odoo.define('repair_workorder_community_v2.timer', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var core = require('web.core');

    ListController.include({
        start: function () {
            this._super.apply(this, arguments);
            this._start_timer();
        },
        _start_timer: function () {
            var self = this;
            setInterval(function () {
                if (self.model && self.renderer) {
                    self.renderer._render();
                }
            }, 10000); // Atualiza a cada 10 segundos
        },
    });
});
