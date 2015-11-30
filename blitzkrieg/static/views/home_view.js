var HomeView = Backbone.View.extend({

    el: '#home',

    initialize: function() {
        this.template = _.template($('#home-template').text());
        this.render();

        this.pulse = false;
        this.rando = false;

    },

    render: function() {
        this.$el.html(this.template());

        var $insta = this.$el.find('.instagram-div'),
            pos = $(window).height() - $insta.position().top + $insta.outerHeight() - 224;

        this.$el.find('#start-beacon-button').css({'margin-top': pos});
        this.$el.find('#testing-beacon').css({
            width: this.$el.find('.outer-div').width() - 40,
            height: this.$el.find('.outer-div').width() - 40,
            opacity: 0
        });
        this.$el.find('.back-div').css({
            'pointer-events': 'none',
            opacity: 0
        });

    },

    events: {
        'click #log-out-button': 'logOut',
        'click #instagram-log-out': 'logOutInstagram',
        'click #twitter-button': 'twitterLogin',
        'click #twitter-log-out': 'logOutTwitter',
        'click .start-beacon': 'startBeacon',
        'click .start-random-beacon': 'startRandomBeacon',
        'click #lights-button': 'stopBeacon',
        'click .branding-img': 'clickBeacon'
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
        window.location.href = 'twitter_login';
    },

    logOutTwitter: function () {
        $.ajax({
            type: 'POST',
            url: 'twitter_log_out',
            success: function () {
                window.location.reload();
            }
        });
    },

    startBeacon: function () {
        this.pulse = true;

        this.$el.find('.facebook-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.twitter-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.instagram-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.start-beacon-outer').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.back-div').animate({
            opacity: 1
        }, 500);
        this.$el.find('.back-div').css({
            'pointer-events': 'all'
        });

        this.beacon();
        this.beaconInterval = setInterval(this.beacon, 15000);
    },

    startRandomBeacon: function () {
        this.pulse = true;
        this.rando = true;

        this.$el.find('.facebook-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.twitter-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.instagram-div').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.start-beacon-outer').animate({
            'pointer-events': 'none',
            opacity: 0
        }, 500);
        this.$el.find('.back-div').animate({
            opacity: 1
        }, 500);
        this.$el.find('.back-div').css({
            'pointer-events': 'all'
        });

        this.randomBeacon();
        this.randomBeaconInterval = setInterval(this.randomBeacon, 15000);
    },

    stopBeacon: function () {
        if (this.rando) {
            clearInterval(this.randomBeaconInterval);
        } else {
            clearInterval(this.beaconInterval);
        }

        this.$el.find('.facebook-div').animate({
            'pointer-events': 'all',
            opacity: 1
        }, 500);
        this.$el.find('.twitter-div').animate({
            'pointer-events': 'all',
            opacity: 1
        }, 500);
        this.$el.find('.instagram-div').animate({
            'pointer-events': 'all',
            opacity: 1
        }, 500);
        this.$el.find('.start-beacon-outer').animate({
            'pointer-events': 'all',
            opacity: 1
        }, 500);
        this.$el.find('.back-div').animate({
            opacity: 0
        }, 500);
        this.$el.find('.back-div').css({
            'pointer-events': 'none'
        });

        this.pulse = false;
        this.rando = false;

    },

    clickBeacon: function () {
        if (typeof Android !== 'undefined') {
            Android.notifyMe();
        }
        $('#testing-beacon').animate({opacity: 1}, 500);
        setTimeout( function () {
            $('#testing-beacon').animate({opacity: 0}, 500);
        }, 500);
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
                        $('#testing-beacon').animate({opacity: 1}, 500);
                        setTimeout( function () {
                            $('#testing-beacon').animate({opacity: 0}, 500);
                        }, 500);
                    }, pingDate - nowDate);
                });
            }
        });
    },

    randomBeacon: function () {
        setTimeout( function () {
            if (typeof Android !== 'undefined') {
                Android.notifyMe();
            }
            $('#testing-beacon').animate({opacity: 1}, 500);
            setTimeout( function () {
                $('#testing-beacon').animate({opacity: 0}, 500);
            }, 500);
        }, Math.random() * 15000);
        setTimeout( function () {
            if (typeof Android !== 'undefined') {
                Android.notifyMe();
            }
            $('#testing-beacon').animate({opacity: 1}, 500);
            setTimeout( function () {
                $('#testing-beacon').animate({opacity: 0}, 500);
            }, 500);
        }, Math.random() * 15000);
        setTimeout( function () {
            if (typeof Android !== 'undefined') {
                Android.notifyMe();
            }
            $('#testing-beacon').animate({opacity: 1}, 500);
            setTimeout( function () {
                $('#testing-beacon').animate({opacity: 0}, 500);
            }, 500);
        }, Math.random() * 15000);
    }

});

var home_view = new HomeView();
