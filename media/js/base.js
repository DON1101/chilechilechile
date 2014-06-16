function resize_iframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}

$(document).ready(function(){
    $("#datepicker").datepicker();
});
