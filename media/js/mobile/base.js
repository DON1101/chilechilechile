angularModule = 

angular.module("chilechilechile", [
    "ngRoute",
    "ngTouch",
    "ngResource",
    "mobile-angular-ui"
    ]
)
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    }
)
.config(function($routeProvider, $locationProvider) {
    $routeProvider.when(
        '/',
        {templateUrl: "/articles/list/",
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/article_list/:day/:page',
        {templateUrl:
            function(params){ return '/articles/list/?day=' + params.day + '&page=' + params.page;},
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/article_details/:article_id',
        {templateUrl:
            function(params){ return '/articles/details/' + params.article_id;},
         controller: "MainCtrl"
        }
    );
})
;

angularModule
.controller("MainCtrl", function($scope, $location, $http, $window) {

    $scope.go = function(path) {
      $location.path(path);
    };

    $scope.broadcast = function(eventName, args){
        $scope.$broadcast(eventName, args);
    };

})
.controller("ArticleListCtrl", function($scope, $location, $http, $window) {

})
.controller("ArticleDetailsCtrl", function($scope, $location, $http, $window) {

})
;


function resize_iframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}
