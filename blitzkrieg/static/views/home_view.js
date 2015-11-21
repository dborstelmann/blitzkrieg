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
        'click #twitter-button': 'twitterLogin',
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

    twitterLogin: function () {
        $.ajax({
            type: 'POST',
            url: 'twitter_login',
            success: function (data) {
                debugger;
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
        $this.text('Start Beacon');
    },

    beacon: function () {
        $.ajax({
            url: 'ping_user_data',
            success: function (data) {
                _.each(data, function (ping) {
                    var nowDate = new Date(),
                        pingDate = new Date(ping);

                    setTimeout( function () {
                        if (typeof Android !== 'undefined') {
                            Android.notifyMe();
                        }
                        $('#testing-beacon').toggleClass('black');
                        setTimeout( function () {
                            $('#testing-beacon').toggleClass('black');
                        }, 500);
                    }, pingDate - nowDate);
                });
            }
        });
    }

});

var home_view = new HomeView();
