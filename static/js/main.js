window.specials = ['first']
    window.specialfiles = ['first']
    function makeid(length) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    function addService() {
        var id = makeid(5)
        window.specials.push(id)
        // forms = document.getElementById("services")
        $("#services").append(`<br/><br/><div class="animated slideInUp" id="` + id + `">
								<a class="btn btn-danger btn-sm" style="float:right" onclick="removeService('` + id + `')" href="#/">Remove</a>
								<h3 class="card-title mb-3">Services details </h3>
                                <div class="form-group">
                                <label class="form-label text-dark">Service</label>
                                <input required="required" name="`+id+`service" type="text" class="form-control" placeholder="Eg: Logo Design">
                            </div>
                            <div class="row">
                                <div class="col-sm-6 col-md-6">
                                    <div class="form-group m-0">
                                        <label class="form-label text-dark">Price</label>
                                        <div class="row gutters-xs">
                                            <div class="col-6">
                                                <input required="required" name="`+id+`start_price" type="number" step=".01" min="0.0" class="form-control" placeholder="Starting Price">
                                            </div>
                                            <div class="col-6">
                                                <select name="`+id+`category" class="form-control select2-show-search  border-bottom-0" data-placeholder="Select Category">
                                                <optgroup label="Categories">
                                                    <option>All Categories</option>
                                                    <option value="Accountant">Accountant</option>
                                                    <option value="IT Software">IT Software</option>
                                                    <option value="Banking">Banking</option>
                                                    <option value="Finances">Finaces</option>
                                                    <option value="Cooking">Cook/Chef</option>
                                                    <option value="Driving">Driving</option>
                                                    <option value="7">HR Recruiter</option>
                                                    <option value="IT Hardware">IT Hardware</option>
                                                    <option value="Sales">Sales</option>
                                                </optgroup>
                                                </select>                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-6 col-md-6">
                                    <div class="form-group">
                                        <label class="form-label text-dark">Year Experience</label>
                                        <div class="row gutters-xs">
                                            <div class="col-12">
                                                <input required="required" name="`+id+`experience" type="number" class="form-control" placeholder="Year Experience">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group text-dark">
                                <label class="form-label text-dark">Service Detail</label>
                                <textarea required="required" name="`+id+`service_detail" class="form-control" name="example-textarea-input" rows="5" placeholder="Eg: I will design fascinating logo with free revision" required></textarea>
                            </div>
                            <div class="form-group text-dark">
                                <label class="form-label text-dark">Add Experience Files</label>
                                <input name="`+id+`fileInput" type="file" id='`+id+`fileInput' multiple><br>
                            </div>
                            <div>
                            <br/>
                            </div>
                            </div>`)
    }

    function removeService(id) {
        $("#" + id).remove();
    }

    function collectForm(){
        let myForm = document.getElementById("serviceform");
                        var saved = "first";
                        let formData = new FormData(myForm);
                        // var myfile = document.getElementById(saved+"file");
                        // console.log(myfile.files[0])

                        // formData.append("file", myfile.files[0]);
                        var myarray = [];
                        var big = {}
                        var info = {};
                        //This will build the form from name, value pairs

                        for(var pair of formData.entries()){
                            var str = pair[0]
                            var res = str.substring(0,5);
                            if (window.specials.includes(res)){
                            if(saved === res){
                                if (pair[0].includes('fileInput')){

                                    info['file'] = pair[0]
                                }else{
                                var key = (pair[0]).replace(res,"")
                                info[key] = pair[1]
                            }

                            }
                            else{
                                myarray.push(info)
                                var info = {};
                                if (pair[0].includes('fileInput')){
                                    info['file'] = pair[0]
                                }else{
                                var key = (pair[0]).replace(res,"")
                                info[key] = pair[1]
                                }

                                saved = (pair[0]).substring(0,5);
                            }
                            }else{
                                big[pair[0]] = pair[1]
                            }
                        }
                        myarray.push(info)
                        big['services']=myarray
                        return big
		};

        function submitForm(){
            document.getElementById('submitbtn').innerHTML = 'processing...'
            $("#submitbtn").prop("disabled",true);
            const data = collectForm()
            // console.log(data)
            data['username']=localStorage.getItem('gig-username');
            url = window.location.origin +"/gigs/create-services/";
            // console.log(url)
            const http = new XMLHttpRequest();
                        http.open('POST', url);
                        http.setRequestHeader('Content-type', 'application/json');
                        console.log(JSON.stringify(data))
                            // http.setRequestHeader('Authentication','id_token');
                            http.send(JSON.stringify(data)); // Make sure to stringify

                            // http.onreadystatechange=(e)=>{
                            //     // console.log(
                            //     //     http.responseText
                            //     // )
                            // }
                        http.onload = function() {
                        state = true;
                        var resp = http.responseText;
                        var json_resp = JSON.parse(resp);
                        // You can now use the response for what you want
                        if(json_resp['success']){

                            for(var i=0;i<json_resp['services'].length;i++){
                                var service = json_resp['services'][i]
                                const file = $("#"+service['fileId']).prop('files')

                                if(i === (json_resp['services'].length)-1){
                                    final = true
                                    uploadFile(file,window.location.origin+'/gigs/service-files/'+service['serviceId']+'/',final);
                                    toast('Please wait...',3000);
                                }else{
                                    final = false
                                    uploadFile(file,window.location.origin+'/gigs/service-files/'+service['serviceId']+'/',final);
                                    toast('Please wait...',3000);
                                }

                                }
                            }
                            // toast('Successfully saved',3000);
                            // var url = window.location.href
                            //
                            else{
                            toast(json_resp['message'],3000)
                        }
                        console.log(json_resp)
                        }

        }
        function toast(msg,time) {
          var x = document.getElementById("snackbar");
          x.innerHTML = msg;
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, time);
        }



function fileValidation(id){
    var fileInput = document.getElementById(id+"file");
    var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif|\.mp4|\.mpeg)$/i;
    if(!allowedExtensions.exec(filePath)){
        alert('Please upload only images or videos');
        fileInput.value = '';
        return false;
    }
    // else{
    //     if (imageValidation(id)){
    //           //Image preview
    //     if (fileInput.files && fileInput.files[0]) {
    //         var reader = new FileReader();
    //         reader.onload = function(e) {
    //             document.getElementById(id+'imagePreview').innerHTML = '<img height="200px" width="200px" src="'+e.target.result+'"/>';
    //             document.getElementById(id+'imagePreview').style.display = "block";
    //         };
    //         reader.readAsDataURL(fileInput.files[0]);
    //     }

    // }
// }
}
function imageValidation(id){
    var fileInput = document.getElementById(id+"file");
    var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if(!allowedExtensions.exec(filePath)){
        console.log('File is not an image so no preview');
        document.getElementById(id+"type").value = 'video'
        document.getElementById(id+'imagePreview').style.display = "none";
        return true;
    }else{
        document.getElementById(id+"type").value = 'image'
        return true
    }
}

// function used to send files
function sendFile(id){
var formData = new FormData();
var imagefile = document.querySelector('#'+id+'files');
formData.append("image", imagefile.files[0]);
axios.post("/gigs/service-files/"+id+"/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
})}

const uploadFile = (files,url,final) => {
    console.log("Uploading file...");
    const API_ENDPOINT = url;
    const request = new XMLHttpRequest();
    const formData = new FormData();

    request.open("POST", API_ENDPOINT, true);
    request.onreadystatechange = () => {
      if (request.readyState === 4 && request.status === 200) {
        console.log(request.responseText);
        // this is how we know the files have been uploaded
        if(final){
            setTimeout(function () {
            window.location.reload(true);
            }, 3000);
        }
      }
    };

    for (let i = 0; i < files.length; i++) {
      formData.append(files[i].name, files[i])
    }
    request.send(formData);
  };


//   $('#firstfileInput').on("change", function (event) {
//     const files = event.target.files;
//     uploadFile(files,'http://127.0.0.1:8000/gigs/service-files/5/');
//   });