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
        {templateUrl: "/articles/list/",
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/article_search/:query/:page',
        {templateUrl:
            function(params){ return '/articles/list/?query=' + params.query + '&page=' + params.page;},
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/article_list/:category/:page',
        {templateUrl:
            function(params){ return '/articles/list/?category=' + params.category + '&page=' + params.page;},
         controller: "MainCtrl"
        });
    $routeProvider.when(
        '/article_details/:article_id',
        {templateUrl:
            function(params){ return '/articles/details/' + params.article_id;},
         controller: "MainCtrl"
        }
    );
    $routeProvider.when(
        '/info',
        {templateUrl: "/m/info",
         controller: "MainCtrl"
        }
    );
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
.controller("ArticleListCtrl", function($rootScope, $scope, $location, $http) {
    $scope.articles = [];

    $rootScope.$broadcast(
        "controller_changed",
        {"controller": "article_list"}
    );

    $scope.init = function(category, query, max_page){
        $scope.category = category;
        $scope.query = query;
        $scope.max_page = max_page;
        $scope.next_page = 0;
        $scope.more_pages = max_page > 1;

        $scope.getArticles($scope.category, 0);
    }

    $scope.loadNextPage = function(){
        if($scope.next_page < $scope.max_page){
            $scope.getArticles($scope.category,
                               $scope.next_page);
        }
    }

    $scope.getArticles = function(category, page){
        var response_promise = $http.get("/api/articles/list/?category=" + category + "&query=" + $scope.query + "&page=" + page);
        response_promise.success(function(data, status, headers, config){
            $scope.articles = $scope.articles.concat(data["articles"]);
            $scope.next_page++;
            $scope.more_pages = $scope.next_page < $scope.max_page;
        });
        response_promise.error(function(data, status, headers, config){
            console.log(data);
        });
    };
})
.controller("ArticleDetailsCtrl", function($rootScope, $scope, $location, $http) {
    $rootScope.$broadcast(
        "controller_changed",
        {"controller": "article_details"}
    );

    $scope.send_comments_init = function(article_id) {
        params = {
            "sender": "ArticleDetailsCtrl",
            "receiver": "CommentCtrl",
            "name": "comments_init",
            "args": {"article_id": article_id}
        };

        comment_init_interv = setInterval(function(){
            $rootScope.$broadcast("comments_init", angular.toJson(params));
        }, 500);
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
        if(typeof $scope.my_comment.comment_content == "undefined" || 
           $scope.my_comment.comment_content.trim().length == 0){
            alert("评论不能为空哦！");
            return;
        }

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

    $scope.$on("comments_init", function(event, msg) {
        clearInterval(comment_init_interv);
        args = angular.fromJson(msg)["args"];
        article_id = args["article_id"];
        $scope.init(article_id);
    });
})
.controller("InfoCtrl", function($rootScope, $scope) {
    $rootScope.$broadcast(
        "controller_changed",
        {"controller": "info"}
    );
})
;


function use_image_proxy(){
    $("img").each(function(){
        $(this).src = "/image-proxy/?url=" + $(this).src;
    });
}

var comment_init_interv;

MESSAGES_QUEUE = [];
function broadcast_message(message){
    MESSAGES_QUEUE.push(message);
}
function pick_message(message){
    for(var i = 0; i < MESSAGES_QUEUE.length; i++){
        if(MESSAGES_QUEUE[i] == message){
            MESSAGES_QUEUE = MESSAGES_QUEUE.splice(i, 1);
            return true;
        }
    }
    return false;
}
