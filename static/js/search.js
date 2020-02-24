function exists(ele){
    if (ele !== null && ele !== undefined){return true}else{return false}
}
function search(data){
    var url = window.location.origin +"/gigs/search-gigs/";
    // const data = {
    //     q:keywords,category:category
    // }
    const http = new XMLHttpRequest();
        http.open('POST', url);
        http.setRequestHeader('Content-type', 'application/json');
        // http.setRequestHeader('Authentication','id_token');
        http.send(JSON.stringify(data)); // Make sure to stringify
        http.onload = function() {
        state = true;
        var resp = http.responseText;
        var json_resp = JSON.parse(resp);
        // You can now use the response for what you want
        if(json_resp['success']){
            // look for id of element that will hold the results and append to it
            // objects received from calling api
            $("#found-gigs").text("")
            for(var i=0;i<json_resp.objects.length;i++){
                var object = json_resp.objects[i]
                var card = constructCard(object);
                $("#found-gigs").append(card)
            }
            $('.scrolling-wrapper').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 3000,
              });

        }
        console.log(json_resp)
        }
    }

function constructCard(object){
    var service = object.service
    var start_price = object.start_price
    var comment = object.detail
    var html = `<div class="col-xl-4 col-md-6">
    <div class="card">
        <div class="scrolling-wrapper">
            <div class="img">
                <img src="/static/services/bnw.png" alt="img">
            </div>
            <div class="img">
                <img src="/static/services/logo_color.png" alt="img">
            </div>
            <div class="img">
                <img src="/static/images/products/products/ed1.jpg" alt="img">
            </div>
        </div>
        <div class="card-body">
            <div class="item-card7-desc">
                <div class="item-card7-text">
                    <a href="jobs.html" class="text-dark"><h4 class="font-weight-semibold">${service}</h4></a>
                </div>
                <ul class="d-flex mt-2">
                    <li class=""><a href="#" class="icons"><i class="icon icon-location-pin text-muted mr-1"></i> USA</a></li>
                    <li><a href="#" class="icons"><i class="icon icon-event text-muted mr-1"></i>1 min ago</a></li>
                    <li class=""><a href="#" class="icons"><i class="icon icon-phone text-muted mr-1"></i> 14 675 65</a></li>
                </ul>
                <p class="mb-0">${comment}</p>
            </div>
        </div>
        <div class="card-body">
            <a href="mr-4" class="icons">GHC ${start_price}</a>
            <a class="mr-4 float-right"><i class="fa fa-clock-o  text-muted mr-1"></i>Full Time Job</a>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center pt-2 mt-auto">
                <img src="/static/images/users/male/7.jpg" class="avatar brround avatar-md mr-3" alt="avatar-img">
                <div>
                    <a href="profile.html" class="text-default">Tanner Mallari</a>
                    <small class="d-block text-muted">2 days ago</small>
                </div>
                <div class="ml-auto text-muted">
                    <a class="btn btn-warning text-white">See Details</a>
                </div>
            </div>
        </div>
    </div>
</div>`
    return html
}
function execute_search(){
var search_q = localStorage.getItem('query')
if(exists(search_q)){
    $("#query").val(JSON.parse(search_q).q)
    search(JSON.parse(search_q))
}
}
document.getElementById('query').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.getElementById('search-btn').click();
    }

}
// when search button at home page is clicked
$('#search-btn').on("click", function (event) {
    // we save what the user searched for
    var query = $("#query").val()
    var category = ""
    const search = {q:query,category:category}
    localStorage.setItem('query',JSON.stringify(search))
    execute_search()
});
execute_search()