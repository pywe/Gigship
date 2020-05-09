// SETTINGS
axios.defaults.baseURL = "https://gigship.pywe.org";
axios.defaults.headers.common['Accept'] = 'application/json';
var iSettings = JSON.parse(localStorage.getItem("settings"))

// DB Settings
var db = new Dexie("Gigship");
db.version(1).stores({
    message: '++id,content,date_time,date,time,to_user,from_user,sent,received,read,reply,msg_id,msg_hash'
});

function save2db(dmsg) {
  db.message.put(dmsg);
}
function toaster(msg,time) {
    var x = document.getElementById("toaster");
    x.innerHTML = msg;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, time);
  }

// UTILITIES
function htmlToText(html){
    //remove code brakes and tabs
    html = html.replace(/\n/g, "");
    html = html.replace(/\t/g, "");

    //keep html brakes and tabs
    html = html.replace(/<\/td>/g, "\t");
    html = html.replace(/<\/table>/g, "\n");
    html = html.replace(/<\/tr>/g, "\n");
    html = html.replace(/<\/p>/g, "\n");
    html = html.replace(/<\/div>/g, "\n");
    html = html.replace(/<\/h>/g, "\n");
    html = html.replace(/<br>/g, "\n"); html = html.replace(/<br( )*\/>/g, "\n");

    //parse html into text
    var dom = (new DOMParser()).parseFromString('<!doctype html><body>' + html, 'text/html');
    return dom.body.textContent;
}

function convertValue(value){
    if (value === 'true'){
        return true
    }
    if (value === true){
        return 'true'
    }
    if (value === 'false'){
        return false
    }
    if (value === false){
        return 'false'
    }
    if (value === 'null'){
        return null
    }
    if (value === null){
        return 'null'
    }
    return value

}

function exists(ele){
    if (ele !== null && ele !== undefined){return true}else{return false}
}

function getMessages(otheruser){
var iSettings = JSON.parse(localStorage.getItem("settings"));
var obj = {thisuser:iSettings.user,otheruser:otheruser}
  axios.post('/api/v1/messages/get-messages/', obj)
  .then(function (response) {
    console.log(response)
})
  .catch(function (error) {
    if (exists(error.response)){
              console.log(error.response.data)
          }
  });

}
function momentTime(time){
    var t = moment(time).calendar();
    return t.replace("Last","")
}

// DOM SETTINGS
function isReading(){
    if (window.chatOpened && document.hasFocus()){
        return true
    }
    return false
}

// GET FUNCTIONS
function getPeople(){
    var iSettings = JSON.parse(localStorage.getItem("settings"));
    var obj = {username:iSettings.username}
  axios.post('/gigship-api/v1/chat/get-people/', obj)
  .then(function (response) {

    if (response.data.success){
    var people = response.data.objects
    // if we got more than one person
    if(people.length > 0){
        console.log(response)
        // We contruct the people
        for(var i=0;i<people.length;i++){
            var obj = people[i]
            var html = contructPerson(obj.username,obj.image,obj.lastMsg);
            // console.log(html)
            $("#orders-list").append(html);
    }
    }else{
        // we did not get anyone
        var obj ={
            username:"Gigship",
            image:"/static/images/svgs/jobs/work.svg",
            lastMsg:{
                content:"Hello there, welcome to Gigship",
                time:new Date(),
                count:1
            }
        }
        var html = contructGigship(obj.username,obj.image,obj.lastMsg);
            // console.log(html)
            $("#orders-list").append(html);
        toaster("No one availble",3000);
        console.log(response)
    }}else{
        console.log(response)
    }
})
  .catch(function (error) {
    if (exists(error.response)){
              console.log(error.response.data)
          }
  });
}

function getChats(username,image,page){
    $("#my-user-name").html(username)
    $("#count-"+username).html("")
    $("#myimage").attr("src",image);
    var iSettings = JSON.parse(localStorage.getItem("settings"));
    var obj = {thisuser:iSettings.username,otheruser:username,page:page}
    axios.post('/gigship-api/v1/chat/get-messages/',obj)
  .then(function (response) {
      console.log(response)
      if(response.data.success){
          var msgs = response.data.objects
          if(msgs.length > 0){
            //   we can now contruct the messages
          }else{
              toaster("No messages yet...",3000)
          }
      }
    })
    .catch(function (error) {
    if (exists(error.response)){
                console.log(error.response.data)
            }
    });

}

function getNoChats(username,image,page){
    $("#my-user-name").html(username)
    $("#count-"+username).html("")
    $("#myimage").attr("src",image);
}

getPeople()

// CONSTRUCT FUNCTIONS
function contructPerson(username,image,msgObj){
    var lastMsg = msgObj.content
    var time =  momentTime(msgObj.time)
    var count = msgObj.count
    div = `<a href="javascript:void(0);" onclick="getChats('${username}','${image}','1')" class="media">
    <div class="media-img-wrap">
        <div class="avatar avatar-online">
            <img src="${image}" alt="User Image" class="avatar-img rounded-circle">
        </div>
    </div>
    <div class="media-body">
        <div>
            <div class="user-name">${username}</div>
            <div class="user-last-chat">${lastMsg}</div>
        </div>
        <div>
            <div class="last-chat-time block">${time}</div>
            <div class="badge badge-success badge-pill" id="count-${username}">${count}</div>
        </div>
    </div>
</a>`
return div
}

function contructGigship(username,image,msgObj){
    var lastMsg = msgObj.content
    var time =  momentTime(msgObj.time)
    var count = msgObj.count
    div = `<a href="javascript:void(0);" onclick="getNoChats('${username}','${image}','1')" class="media">
    <div class="media-img-wrap">
        <div class="avatar avatar-online">
            <img src="${image}" alt="User Image" class="avatar-img rounded-circle">
        </div>
    </div>
    <div class="media-body">
        <div>
            <div class="user-name">${username}</div>
            <div class="user-last-chat">${lastMsg}</div>
        </div>
        <div>
            <div class="last-chat-time block">${time}</div>
            <div class="badge badge-success badge-pill" id="count-${username}">${count}</div>
        </div>
    </div>
</a>`
return div
}