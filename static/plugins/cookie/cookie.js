

 $(document).ready(function() {
     if (localStorage['accepted_cookies']){}else{
        $('body').ihavecookies({
            title: 'Cookies & Privacy Policy?',
            message: 'There are no cookies used on this site, but if there were this message could be customised to provide more details. Click the <strong>accept</strong> button below to see the optional callback in action...',
            delay: 600,
            expires: 1,
            link: '#privacy',
            onAccept: function(){
                var myPreferences = $.fn.ihavecookies.cookie();
                console.log('Yay! The following preferences were saved...');
                console.log(myPreferences);
                localStorage['accepted_cookies'] = true
            },
            uncheckBoxes: true,
            acceptBtnLabel: 'Accept Cookies',
            moreInfoLabel: 'More information'
        });}

        if ($.fn.ihavecookies.preference('marketing') === true) {
            localStorage['accepted_cookies'] = true
            console.log('This should run because marketing is accepted.');
        }
    });