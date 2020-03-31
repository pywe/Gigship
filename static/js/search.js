function exists(ele) {
    if (ele !== null && ele !== undefined) {
        return true
    } else {
        return false
    }
}
function Image(path){
    // var fileInput = document.getElementById(id+"file");
    // var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif|\.svg)$/i;
    if(allowedExtensions.exec(path)){
        // alert('This is an image');
        // fileInput.value = '';
        return true;
    }else{
        return false
    }
}

function Video(path){
    // var fileInput = document.getElementById(id+"file");
    // var filePath = fileInput.value;
    var allowedExtensions = /(\.mp4|\.mpeg|\.webm)$/i;
    if(allowedExtensions.exec(path)){
        // alert('This is a video');
        // fileInput.value = '';
        return true;
    }else{
        return false
    }
}

function search(data) {
    var url = window.location.origin + "/gigs/search-gigs/";
    // const data = {
    //     q:keywords,category:category
    // }
    const http = new XMLHttpRequest();
    http.open('POST', url);
    http.setRequestHeader('Content-type', 'application/json');
    // http.setRequestHeader('Authentication','id_token');
    http.send(JSON.stringify(data)); // Make sure to stringify
    http.onload = function () {
        state = true;
        var resp = http.responseText;
        var json_resp = JSON.parse(resp);
        // You can now use the response for what you want
        if (json_resp['success']) {
            // look for id of element that will hold the results and append to it
            // objects received from calling api
            $("#found-gigs").text("")
            if((json_resp.objects).length>0){
            for (var i = 0; i < (json_resp.objects).length; i++) {
                var object = json_resp.objects[i]
                var card = constructCard(object);
                $("#found-gigs").append(card)
            }}else{
                var card = `<p>Sorry, No Gigs Found matching your query. You could try using categories</p>`
                $("#found-gigs").append(card)
            }
            $('.scrolling-wrapper').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 3000,
                adaptiveHeight: true,
                pauseOnFocus:true,
                variableWidth:false
            });
            // hide loader
            $("#global-loader").removeClass('show');
            $("#global-loader").addClass('hidden');

        }
        console.log(json_resp)
    }
}

// TODO: remember to remove trailing slash in production
function contructFiles(files){
    var div = ``
    for (var i=0;i<files.length;i++){
        if(Image(files[i])){
            div += `<div class="img">
            <img src="${files[i]}" alt="img">
        </div>`
        }else{
            div += `<div class="img">
            <video alt="video" controls>
            <source src="${files[i]}">
            </video>
        </div>`
        }
    }
    return div
}

function constructCard(object) {
    var service = object.service
    var id = object.id
    var rating = object.rating
    var rating_no = object.rating_number 
    var start_price = object.start_price
    var comment = object.detail
    var files = object.files
    var fileshtml = contructFiles(files);
    var temp = `<div class="scrolling-wrapper">
    <div class="img">
        <img src="/static/services/bnw.png" alt="img">
    </div>
    <div class="img">
        <img src="/static/services/logo_color.png" alt="img">
    </div>
    <div class="img">
        <img src="/static/images/products/products/ed1.jpg" alt="img">
    </div>
    </div>`
    var html = `<div class="col-xl-4 col-md-6">
    <div class="card">
    <div class="scrolling-wrapper">
        ${fileshtml}
    </div>
        <div class="card-body">
            <div class="item-card7-desc">
                <div class="item-card7-text">
                    <a href="/gigs/order/${id}/" class="text-dark"><h4 class="font-weight-semibold">${service}</h4></a>
                </div>
                <p class="mb-0"><a href="/gigs/order/${id}/">${comment}</a></p>
            </div>
        </div>
        <div class="card-body">
            <a href="/gigs/order/${id}/" class="icons">Starting at GHC ${start_price}</a>
            <a href="/gigs/order/${id}/" class="mr-4 float-right"><i class="fa fa-star text-warning"></i>${rating} Rating(${rating_no})</a>
        </div>
    </div>
</div>`
    return html
}

function execute_search() {
    var search_q = localStorage.getItem('query');
    if (exists(search_q)) {
        $("#query").val(JSON.parse(search_q).q)
        search(JSON.parse(search_q))
    }
}
document.getElementById('query').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.getElementById('search-btn').click();
    }

}
// when search button at home page is clicked
$('#search-btn').on("click", function (event) {
    // show loader
    $("#global-loader").addClass('show');
    // we save what the user searched for
    var query = $("#query").val()
    var category = ""
    const search = {
        q: query,
        category: category
    }
    localStorage.setItem('query', JSON.stringify(search))
    execute_search()
});
execute_search()