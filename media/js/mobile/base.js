angularModule = 

angular.module("chilechilechile", [
    "ngRoute",
    "ngTouch",
    "ngResource",
    "mobile-angular-ui",
    "infinite-scroll",
    ]
)
.factory('mySharedService', function($rootScope) {
    var $sharedService = {};

    $sharedService.message = '';

    $sharedService.prepForBroadcast = function(msg) {
        this.message = msg;
        this.broadcastItem();
    };

    $sharedService.broadcastItem = function() {
        $rootScope.$broadcast('handleBroadcast');
    };

    return $sharedService;
})
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
        '/article_search/:query',
        {templateUrl:
            function(params){ return '/articles/list/?query=' + params.query;},
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
.controller("ArticleListCtrl", function($scope, $location, $http) {
    $scope.day = 0;
    $scope.max_page = 0;
    $scope.next_page = 0;
    $scope.articles = [];

    $scope.init = function(day, max_page){
        $scope.day = day;
        $scope.max_page = max_page;
        $scope.next_page = 0;

        $scope.getArticles($scope.day, 0);
    }

    $scope.loadNextPage = function(){
        console.log("loading...");
        if($scope.next_page < $scope.max_page){
            $scope.getArticles($scope.day,
                               $scope.next_page);
            $scope.next_page++;
        }
    }

    $scope.getArticles = function(day, page){
        var response_promise = $http.get("/api/articles/list/?day=" + day + "&page=" + page);
        response_promise.success(function(data, status, headers, config){
            $scope.articles = $scope.articles.concat(data["articles"]);
        });
        response_promise.error(function(data, status, headers, config){
            console.log(data);
        });
    };
})
.controller("ArticleDetailsCtrl", function($rootScope, $scope, $location, $http) {

    $scope.send_comments_init = function(article_id) {
        params = {
            "sender": "ArticleDetailsCtrl",
            "receiver": "CommentCtrl",
            "name": "comments_init",
            "args": {"article_id": article_id}
        };
        $rootScope.$broadcast("comments_init", angular.toJson(params));
    };
})
.controller("CommentCtrl", function($scope, $location, $http) {
    $scope.article_id = "";
    $scope.comments = [];
    $scope.my_comment = {};

    $scope.init = function(article_id){
        $scope.article_id = article_id;
        var response_promise = $http.get("/api/articles/comments/" + article_id);
        response_promise.success(function(data, status, headers, config){
            $scope.comments = data["comments"];
        });
        response_promise.error(function(data, status, headers, config){
            console.log(data);
        });
    };

    $scope.submit_comment = function(){

        url = "/api/articles/comments/" + $scope.article_id;
        $http.post(
            url,
            $.param({
                "user_name": $scope.my_comment.user_name,
                "user_email": $scope.my_comment.user_email,
                "content": $scope.my_comment.comment_content,
            }),
            {
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }
        )
        .success(function(data){
            $scope.init($scope.article_id);
            $scope.my_comment = {};
        })
        .error(function(data){
            console.log(data);
        });
    };

    $scope.$on('comments_init', function(event, msg) {
        args = angular.fromJson(msg)["args"];
        article_id = args["article_id"];
        $scope.init(article_id)
    });
})
;


function resize_iframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}
