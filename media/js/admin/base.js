angularModule = 

angular.module("chilechilechile", [
    "ngRoute",
    "ngTouch",
    "ngResource",
    "mobile-angular-ui",
    "infinite-scroll",
    ]
)
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    }
)
.config(function($routeProvider, $locationProvider) {
    $routeProvider.when(
        '/',
        {templateUrl: "/admin/comments/all/",
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/all_comments/',
        {templateUrl: "/admin/comments/all/",
         controller: "MainCtrl"
        });
})
;

angularModule
.controller("MainCtrl", function($rootScope, $scope, $location, $http, $window) {
    $scope.cur_ctrl = "";

    $rootScope.$on("$routeChangeStart", function(){
      $rootScope.loading = true;
    });

    $rootScope.$on("$routeChangeSuccess", function(){
      $rootScope.loading = false;
    });

    $scope.go = function(path) {
      $location.path(path);
    };

    $scope.cur_controller = function(controller){
        return $scope.cur_ctrl == controller;
    }

    $scope.broadcast = function(eventName, args){
        $scope.$broadcast(eventName, args);
    };

    $scope.$on("controller_changed", function(event, msg){
        controller = angular.fromJson(msg)["controller"];
        $scope.cur_ctrl = controller;
    });

})
.controller("CommentListCtrl", function($rootScope, $scope, $location, $http) {
    $scope.comments = [];

    $rootScope.$broadcast(
        "controller_changed",
        {"controller": "comment_list"}
    );

    $scope.getComments = function(){
        var response_promise = $http.get("/api/admin/comments/all/");
        response_promise.success(function(data, status, headers, config){
            $scope.comments = data["comments"];
        });
        response_promise.error(function(data, status, headers, config){
            console.log(data);
        });
    };

    $scope.getComments();
})
;
