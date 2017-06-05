var myApp = angular.module("myApp", []);

myApp.controller('bookController', function($scope, $http) {

    $scope.error = null;

    $http({
        method : "GET",
        url : "http://127.0.0.1:8000/catalogue/"
    }).then(function mySuccess(response) {
        $scope.books = response.data;
    }, function myError(response) {
        $scope.error = response.statusText;
    });

    $scope.editing = false;


    $scope.book = {
        title: null,
        description: null,
        author: []
    };

    $scope.edit = function($event, book) {
        $scope.id = book.id
        $scope.book.title = book.title
        $scope.book.description = book.description

        var authors = $.map(book.author, function(value, index) {
            return value['name'];
        });

        $scope.book.author = authors
        $scope.editing = true;
    }

    $scope.delete = function($event, book) {
        $http({
            url: "http://127.0.0.1:8000/catalogue/"+book.id,
            method: 'DELETE',
            headers : {'Content-Type': 'application/json'}
        }).then(function mySuccess(response) {
            var index = $scope.books.indexOf(book);
            $scope.books.splice(index, 1);
        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    }

    $scope.createOrUpdate = function() {
        if($scope.editing == false){
            var url = "http://127.0.0.1:8000/catalogue/"
            var method = "POST"
        }else{
            var url = "http://127.0.0.1:8000/catalogue/"+$scope.id
            var method = "PUT"
        }

        $http({
            url: url,
            data: JSON.stringify($scope.book),
            method: method,
            headers : {'Content-Type': 'application/json'}
        }).then(function mySuccess(response) {
            $scope.book = {};
            $scope.bookForm.$setPristine();
            if($scope.editing == false){
                $scope.books.push(response.data);
            }else{
                $scope.editing = false;
                book = $.grep($scope.books, function(b){
                    return b.id === $scope.id;
                })[0]
                var index = $scope.books.indexOf(book);
                $scope.books.splice(index, 1);
                $scope.books.push(response.data);
            }
        }, function myError(response) {
            $scope.error = response.statusText;
        });
    };

});