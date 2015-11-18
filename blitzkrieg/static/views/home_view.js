var HomeView = Backbone.View.extend({

    el: '#home',

    initialize: function() {
        this.template = _.template($('#home-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

    events: {
        'click #log-out-button': 'logOut',
        'click #instagram-log-out': 'logOutInstagram',
        'click .start-beacon': 'startBeacon',
        'click .stop-beacon': 'stopBeacon'
    },

    logOut: function () {
        $.ajax({
            url: 'log_out',
            success: function () {
                window.location.reload();
            }
        });
    },

    logOutInstagram: function () {
        $.ajax({
            type: 'POST',
            url: 'instagram_log_out',
            success: function () {
                window.location.reload();
            }
        });
    },

    startBeacon: function (e) {
        var $this = $(e.target);

        $this.removeClass('start-beacon');
        $this.addClass('red darken-2');
        $this.addClass('stop-beacon');
        $this.text('Stop Beacon');

        this.beacon();
        this.beaconInterval = setInterval(this.beacon, 15000);
    },

    stopBeacon: function (e) {
        var $this = $(e.target);


        clearInterval(this.beaconInterval);

        $this.removeClass('stop-beacon');
        $this.removeClass('red darken-2');
        $this.addClass('start-beacon');
        $this.text('Start Beacon Beacon');
    },

    beacon: function () {
        var _this = this;

        $.ajax({
            url: 'ping_user_data',
            success: function (data) {
                debugger;
            }
        });
    }

});

var home_view = new HomeView();
