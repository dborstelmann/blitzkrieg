var StaticWebsiteView = Backbone.View.extend({

    el: '#static_website',

    initialize: function() {
        this.template = _.template($('#static-website-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

    events: {
    }

});

var static_website_view = new StaticWebsiteView();
