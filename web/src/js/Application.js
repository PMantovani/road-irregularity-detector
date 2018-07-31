var app = angular.module("MyApp", ['ngAnimate', 'ngAria', 'ngMessages', 'ngMaterial']);

app.service('Map', MapService);

app.config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('red', {
            'default': '900'
        })
        .accentPalette('orange');
});

app.filter('formatDate', function() {
    return function(input) {
        if (typeof input === "string") {
            if (input.length > 10) {
                var year = input.substr(2,2);
                var month = input.substr(5,2);
                var day = input.substr(8,2);
                var time = input.substr(11,8);
                var monthStr = ["Jan", "Feb", "Mar", "Abr", "Mai", "Jun",
                                "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
                month = monthStr[month-1];
                input = time + " " + day + " " + month + " " + year;
            }
        }
        return input;
    };
});
