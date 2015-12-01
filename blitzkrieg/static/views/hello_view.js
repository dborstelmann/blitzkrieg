var HelloView = Backbone.View.extend({

    el: '#hello',

    initialize: function() {
        this.helloTemplate = _.template($('#hello-template').text());
        this.logTemplate = _.template($('#log-in-template').text());
        this.signTemplate = _.template($('#register-template').text());
        this.template = this.helloTemplate;

        this.render();
    },

    render: function() {
        this.$el.html(this.template());

        this.$el.find('.buttz').css({top: $(window).height() - 140});
        this.$el.find('.outer-div').css({height: $(window).height() - 15});
        this.$el.find('.buttz').css({
            width: this.$el.find('.outer-div').width()
        });
    },

    logRender: function() {
        this.$el.html(this.template());

        this.$el.find('.buttzzz').css({top: $(window).height() - 180});
        this.$el.find('.outer-div').css({height: $(window).height() - 15});
        this.$el.find('.buttzzz').css({
            width: this.$el.find('.outer-div').width()
        });
    },

    signRender: function() {
        this.$el.html(this.template());

        this.$el.find('.buttzzz').css({top: $(window).height() - 180});
        this.$el.find('.outer-div').css({height: $(window).height() - 15});
        this.$el.find('.buttzzz').css({
            width: this.$el.find('.outer-div').width()
        });
    },

    events: {
        "click #log-in-button": "logIn",
        "click #register-button": "register",
        "click .new-log-in-button": "moveLog",
        "click .new-sign-up-button": "newSign",
        "click .back-home": "goBack"
    },

    goBack: function () {
        this.template = this.helloTemplate;
        this.render();
    },

    moveLog: function () {
        this.template = this.logTemplate;
        this.logRender();
    },

    newSign: function () {
        this.template = this.signTemplate;
        this.signRender();
    },

    logIn: function () {
        var email = $('#email').val(),
            password = $('#password').val();

        if (email && password) {

            $.ajax({
                type: 'POST',
                url: 'log_in',
                data: {
                    email: email,
                    password: password
                },
                success: function (data) {
                    if (data.data === 'invalid_login') {
                        Materialize.toast('User does not exist!', 3000);
                    } else {
                        window.location.href = 'home';
                    }
                }
            });

        } else {
            Materialize.toast('Please input your email and password!', 3000);
        }
    },

    register: function () {
        var email = $('#email').val(),
            password = $('#password').val(),
            firstName = $('#first-name').val(),
            lastName = $('#last-name').val();

        if (email && password && firstName && lastName) {

            $.ajax({
                type: 'POST',
                url: 'register',
                data: {
                    email: email,
                    password: password,
                    first_name: firstName,
                    last_name: lastName
                },
                success: function (data) {
                    if (data.data === 'user_exists_error') {
                        Materialize.toast('We already have a user with this email address!', 3000);
                    } else {
                        window.location.href = 'home';
                    }
                }
            });

        } else {
            Materialize.toast('Please fill all the fields!', 3000);
        }
    }

});

var hello_view = new HelloView();
