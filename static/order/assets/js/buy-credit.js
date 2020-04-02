"use strict";

/*! signup.js | Friendkit | © Css Ninja. 2019-2020 */

/* ==========================================================================
Signup Process JS
========================================================================== */
Dropzone.autoDiscover = false;
// SETTINGS
axios.defaults.baseURL = window.location.origin;
axios.defaults.headers.common['Accept'] = 'application/json';

function exists(ele) {
    if (ele !== null && ele !== undefined) {
        return true
    } else {
        return false
    }
}
$(document).ready(function () {
  "use strict";

  $('.progress-wrap .dot').on('click', function () {
    var $this = $(this);
    var stepValue = $this.attr('data-step');
    $this.closest('.progress-wrap').find('.bar').css('width', stepValue + '%');
    $this.siblings('.dot').removeClass('is-current');
    $this.addClass('is-active is-current');
    $this.prevAll('.dot').addClass('is-active');
    $this.nextAll('.dot').removeClass('is-active');
    $('.process-panel-wrap').removeClass('is-active');
    $('.step-title').removeClass('is-active');

    if (stepValue == '0') {
      $('#signup-panel-1, #step-title-1').addClass('is-active');
    } else if (stepValue == '50') {
      $('#signup-panel-2, #step-title-2').addClass('is-active');
      var username = localStorage.getItem("user");
      var amount = $("#amount").val()
      var email = $("#email").val()
      $("#amount-disabled").val(amount)
      var credit = {
        user:username,
        amount:amount,
        email:email
      }
      localStorage.setItem("credit",JSON.stringify(credit))
    }
    else if (stepValue == '100') {
      var myobj = JSON.parse(localStorage.getItem("credit"))
      axios.post('/gigship-api/v1/accounts/create-transaction/', myobj)
      .then(function (response) {
        console.log(response);
        var data = response.data.data;
        var transid = data.transid
        $("#payment").attr('data-amount',data.amount)
        $("#payment").attr('data-transid',transid)
        $("#trans-info").text("Your order is being processed, please pay to complete it.")
        if (typeof someObject == 'undefined') $.loadScript('https://test.theteller.net/checkout/resource/api/inline/theteller_inline.js', function(){
         //Stuff to do after someScript has loaded
         console.log("let's pay now")
         document.getElementById("await-payment").style.display = "none"
       });
    //step should show after order creation is successful  
      $('#signup-panel-3, #step-title-3').addClass('is-active');
      })
      .catch(function (error) {
        if (exists(error.response)){
                  console.log(error.response.data)
              }
      });
      $('#signup-panel-3, #step-title-3').addClass('is-active');
    } 
    // else if (stepValue == '75') {
    //   $('#signup-panel-4, #step-title-4').addClass('is-active');
    // } else if (stepValue == '100') {
    //   $('#signup-panel-5, #step-title-5').addClass('is-active');
    // }
  });
  $('.process-button').on('click', function () {
    var $this = $(this);
    var targetStepDot = $this.attr('data-step');
    $this.addClass('is-loading');
    setTimeout(function () {
      $this.removeClass('is-loading');
      $('#' + targetStepDot).trigger('click');
    }, 800);
  });

  $('#signup-finish').on('click', function () {
    var $this = $(this);
    var url = '/feed.html';
    $this.addClass('is-loading');
    setTimeout(function () {
      window.location = url;
    }, 800);
  });
});