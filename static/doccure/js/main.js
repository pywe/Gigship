axios.defaults.baseURL = 'https://pharst.pywe.org';
axios.defaults.headers.common['Accept'] = 'application/json';

window.delivered_img = "assets/img/doctors/1.png" 
window.default_img = "assets/img/doctors/2.png"


function getImage(status){
    if (status === "Delivered"){
        return window.delivered_img
    }else{
        return window.default_img
    }
}


function getOrdersShortInfo(username){
    axios.post('/pharstapi/v1/orders/all-orders-short-info/', {username:username
    })
      .then(function (response) {
        console.log(response);
        if (response.data){
            for (var i=0;i<response.data.objects.length;i++){
                // we append here 
                var order = response.data.objects[i]
                var number = order.order_no
                var status = order.status
                var time = order['date_created']
                var html = contructOrder(username,number,status,time)
                $("#orders-list").append(html);
            }
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    function contructOrder(username,number,status,time){
        var img = getImage(status)
        var html = `<a href="javascript:void(0);" onclick="getOrderInfo('${username}','${number}')" class="media">
        <div class="media-img-wrap">
            <div class="avatar avatar-online">
                <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
            </div>
        </div>
        <div class="media-body">
            <div>
                <div class="user-name">${number}</div>
                <div class="user-last-chat">${status}</div>
            </div>
            <div>
                <div class="last-chat-time block">${time}</div>
            </div>
        </div>
    </a>`
    return html

    }
    getOrdersShortInfo('TheoElia')

    function getOrderInfo(username,order_no){
        axios.post('/pharstapi/v1/orders/get-order/', {username:username,
            order_no:order_no
        })
          .then(function (response) {
            console.log(response);
            if (response.data){
               var object = response.data.objects;
               var time = object.date_created
            //    order begins
            $("#chat-list").text('')
               $("#chat-list").append(`<li class="media sent">
                    <div class="media-body">
                        <div class="msg-box">
                            <div>
                                <p>Hello there, I need these drugs, can you get them for me?</p>
                                <ul class="chat-msg-info">
                                    <li>
                                        <div class="chat-time">
                                            <span>${time}</span>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>`)
                // drugs are added to the order by customer
               var bightml = ``
               for (var i=0;i<object.drugs.length;i++){
                   var drug = object.drugs[i]
                   if(i === 0){
                    var html = constructFirstDrug(drug);
                   }else if(i === object.drugs.length-1){
                    var html = constructLastDrug(drug);
                   }else{
                    var html = constructDrug(drug);
                }
                    bightml += html
                    
               }
               $("#chat-list").append(bightml);
            if(object.reviewed){
               var rbightml = ``
            //    we reply the customer with the cost of their order
               for (var i=0;i<object.drugs.length;i++){
                   var drug = object.drugs[i]
                   if(i === 0){
                    var rhtml = constructFirstCost(object.status,drug);
                   }else if(i === object.drugs.length-1){
                    var rhtml = constructLastCost(drug);
                   }else{
                    var rhtml = constructCost(drug);
                }
                    rbightml += rhtml
                    
               }
               $("#chat-list").append(rbightml);
            //    total cost of the order is made known to the customer
               var total = constructTotalCost(object)
               $("#chat-list").append(total);
            }else{
                // we are yet to confirm
            }
            //    now let's check if this order was confirmed
            if(object.confirmed){
                var confirm = constructConfirm(object)
                $("#chat-list").append(confirm);
                // respondng to customer confirmation
                var resp = constructConfirmResponse(object);
                $("#chat-list").append(resp);
                // Customer's address taken
                var useraddress = constructAddress(object.address);
                $("#chat-list").append(useraddress);
                // Reply we got the address
                var addressresp = constructAddressResponse(object)
                $("#chat-list").append(addressresp);
                // have we dispatched the order?
                if(object.dispatched){
                    var dispatched = constructDispatched(object)
                    $("#chat-list").append(dispatched);
                    // has the rider already delivered
                    if(object.rider_delivered){
                        var riderdelivered = constructDelivered(object);
                        $("#chat-list").append(riderdelivered);
                        // has the customer signed?
                        if(object.customer_received){
                            var customerreceived = constructCustomerReceived(object)
                            $("#chat-list").append(customerreceived);
                        }else{
                            // the customer has not signed yet
                        }
                    }else{
                        // we are yet to deliver
                    }

                }else{
                    // we are yet to dispatch
                }
            }else if(object.cancelled){
                var confirm = constructCancel()
                $("#chat-list").append(confirm); 
            }else{
                // user yet to confirm the order
            }
        //        $("#chat-list").append(`<li class="media received">
        //        <div class="avatar">
        //            <img src="assets/img/doctors/1.png" alt="User Image" class="avatar-img rounded-circle">
        //        </div>
        //        <div class="media-body">
        //            <div class="msg-box">
        //                <div>
        //                    <div class="msg-typing">
        //                        <span></span>
        //                        <span></span>
        //                        <span></span>
        //                        <span></span>
        //                        <span></span>
        //                    </div>
        //                </div>
        //            </div>
        //        </div>
        //    </li>`)

            }
          })
          .catch(function (error) {
            console.log(error);
          });
        }

function constructDrug(drug){
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var html = `
        <div class="msg-box">
            <div>
                <p>Drug name: ${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:30 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>`
return html
}
function constructFirstDrug(drug){
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var html = `<li class="media sent">
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Drug name: ${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:30 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>`
return html
}
function constructLastDrug(drug){
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var html = `
        <div class="msg-box">
            <div>
                <p>Finally,</p>
                <p>Drug name: ${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:30 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}
function constructFirstCost(status,drug){
    var img = getImage(status)
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var price = drug.price
    var total = parseFloat(quantity)*parseFloat(price)
    $("#myimage").attr('src', img);
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Drug Name:${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <p>Cost: ${total}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:35 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>`
return html
}
function constructLastCost(drug){
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var price = drug.price
    var total = parseFloat(quantity)*parseFloat(price)
    var html = `
        <div class="msg-box">
            <div>
                <p>And Finally,</p>
                <p>Drug Name:${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <p>Cost: ${total}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:35 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}
function constructCost(drug){
    var name = drug.name
    var quantity = drug.quantity
    var division = drug.division
    var price = drug.price
    var total = parseFloat(quantity)*parseFloat(price)
    var html = `<div class="msg-box">
            <div>
                <p>Drug Name:${name}</p>
                <p>Division: ${division}</p>
                <p>Quantity: ${quantity}</p>
                <p>Cost: ${total}</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:35 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        `
return html
}
function constructTotalCost(order){
    var img = getImage(order.status)
    var time = order.time_reviewed
    var delivery = order.delivery
    var total_drugs_cost = order.drugs_cost
    var total_cost = parseFloat(delivery)+parseFloat(total_drugs_cost)
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>With those prices, your order will then sum up as follows:</p>
                <p><b>Drugs Cost: ${total_drugs_cost}</b></p>
                <p><b>Delivery Fee: ${delivery}</b></p>
                <p><b>Total Cost: ${total_cost}</b></p>
                <p>If these are okay with you, then please confirm</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>${time}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructConfirm(order){
    var time = order.time_confirmed
    var html = `<li class="media sent">
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Hello Pharst Care,</p>
                <p>Please, I confirm this order for delivery</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>${time}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructCancel(){
    var html = `<li class="media sent">
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Hello Pharst Care,</p>
                <p>Please, I am sorry, I do not want the order any longer</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:30 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructConfirmResponse(order){
    var img = getImage(order.status)
    var delivery = order.delivery
    var order_no = order.order_no
    var total_drugs_cost = order.drugs_cost
    var total_cost = parseFloat(delivery)+parseFloat(total_drugs_cost)
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Right, we will be delivering your order very soon.</p>
                <p>Take note of the order details below:</p>
                <p><b>Your order Number: ${order_no}</b></p>
                <p><b>Drugs Cost: ${total_drugs_cost}</b></p>
                <p><b>Delivery Fee: ${delivery}</b></p>
                <p><b>Total Cost: ${total_cost}</b></p>
                <p>Please, give us the address to which the order should be delivered.</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:35 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructAddress(address){
    var country = address.country
    var region = address.region
    var town = address.town
    var phone = address.contacts
    var address = address.address
    for (var i=0;i<phone.length;i++){
        var myphone = phone[i]
    }
    var html = `<li class="media sent">
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>These are the address and contact information of where you should deliver to:</p>
                <p><b>Country: ${country}</b></p>
                <p><b>Region: ${region}</b></p>
                <p><b>Town: ${town}</b></p>
                <p><b>Home/Office address: ${address}</b></p>
                <p>You can contact <b>${myphone}</b> while delivering.</p>
                <p>Thank you</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:30 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}
function constructAddressResponse(order){
    var img = getImage(order.status) 
    var time = order.time_reviewed 
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Thank you for confirming your address, your order urgency status
                has been noted and we will act accordingly.</p>
                <p>We will soon dispatch your order and let you know</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>${time}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}
function constructDispatched(order){
    var img = getImage(order.status)
    
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Hello there, your order has just been dispatched</p>
                <p>Be expecting it soon</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>8:35 AM</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructDelivered(order){
    var img = getImage(order.status)
    var time = order.time_delivered;
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Hello there, our rider just notified us that he has delivered</p>
                <p>Please make sure you sign your order. This will tell us you received the order</p>
                <p>Our rider can help you sign</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>${time}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}

function constructCustomerReceived(order){
    var img = getImage(order.status)
    var time = order.time_received;
    var html = `<li class="media received">
    <div class="avatar">
        <img src="${img}" alt="User Image" class="avatar-img rounded-circle">
    </div>
    <div class="media-body">
        <div class="msg-box">
            <div>
                <p>Thank you for signing. We are confident you have the right package</p>
                <p>Have a wonderful one. We are very pleased to have you.</p>
                <ul class="chat-msg-info">
                    <li>
                        <div class="chat-time">
                            <span>${time}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>`
return html
}
// getOrderInfo('TheoElia','GH-T1-107-wqZma')

