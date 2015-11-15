var HelloView = Backbone.View.extend({

    el: '#hello',

    initialize: function() {
        this.template = _.template($('#hello-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

    events: {
        "click #log-in-button": "logIn",
        "click #register-button": "register"
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
