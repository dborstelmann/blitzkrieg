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
        'click #get-instagram-feed': 'getInstagramFeed'
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

    getInstagramFeed: function () {
        $.ajax({
            type: 'GET',
            url: 'get_instagram_feed',
            success: function () {
            }
        });
    }

});

var home_view = new HomeView();