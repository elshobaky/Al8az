// view user activities/logs
var loghtml_temp = '<div class="act-time" num="%num%">' +                                 
                    '<div class="activity-body act-in">' +
                        '<span class="arrow"></span>' +
                        '<div class="text">' +
                            '<a href="%url%" class="activity-img"><img class="avatar" src="/style/img/%cat%.png" alt=""></a>' +
                            '<p class="attribution"><a href="/user/%user_id%">%user_name%</a> at %created%</p>' +
                            '<p>%msg%</p>' +
                        '</div>' +
                    '</div>' +
                '</div>'
var msg_temp = 'لقد قام <a href="/user/%user_id%">%user_name%</a> ب%cat% <a href="%url%">%item_name%</a>'
var logData = {
            's'   : 0,
            'n'   : 20,
            'uid' : uid,
        };
function load_logs() {
    $.ajax({
        type     : 'GET',
        url      : '/ajax/getlog',
        data     : logData,
        dataType : 'json', 
        encode   : true
        })
      .done(function(data) {
        //console.log(data)
        var logs = $.parseJSON(data.logs)
        var count = data.count
        var current = data.current
        //console.log(current)
        for (i in logs) {
            item = logs[i]
            //item = $.parseJSON(item)
            //console.log(item)
            var loghtml = loghtml_temp
            var msg = msg_temp.replace('%user_name%',item.user_name);
            msg = msg.replace('%user_id%',item.user_id);
            loghtml = loghtml.replace('%num%',i);
            loghtml = loghtml.replace('%user_name%',item.user_name);
            loghtml = loghtml.replace('%user_id%',item.user_id);
            loghtml = loghtml.replace('%url%',item.url);
            loghtml = loghtml.replace('%created%',item.created);
            loghtml = loghtml.replace('%cat%',item.cat);
            msg = msg.replace('%url%',item.url);
            msg = msg.replace('%item_name%',item.item_name);
            if (item.cat==='q') {
                msg = msg.replace('%cat%','حل لغز');
            }
            if (item.cat==='qtry') {
                msg = msg.replace('%cat%','محاولة حل لغز');
            }
            if (item.cat==='g') {
                msg = msg.replace('%cat%','لعب لعبة');
            }
            loghtml = loghtml.replace('%msg%',msg);
            $('#logs').append(loghtml);
        }
        if (count>current) {
            $('#profile-loadmore-logs').css('display','block');
            logData.s = current
        }
        else {
            $('#profile-loadmore-logs').css('display','none');
        }
      });
}



// edit profile handler
$(document).ready(function() {
    //load logs
    load_logs();
    $('#loadmore').button().click(function() {
        load_logs();
    });
    // process the edit basic info form
    $('#edit_profile').submit(function(event) {

        $('#edit_profile').append('<img src="/style/img/loader.gif" id="loading">');
        $('.edit_error').css('display','none');
        $('#submit_state').remove()
        var formData = {
            'firstname'   : $('input[name=firstname]').val(),
            'lastname'    : $('input[name=lastname]').val(),
            'email'       : $('input[name=email]').val(),
            'about'       : $('textarea[name=about]').val(),
            'country'     : $('input[name=country]').val(),
            'ajax'        : 't'
        };
        var ajax_data = {
            type        : 'POST', 
            url         : '/profile', 
            data        : formData,
            dataType    : 'json', 
            encode      : true
        }
        $.ajax(ajax_data)
            .done(function(data) {
                console.log(data);
                $('#loading').remove();
                if (data.edit_profile===true) {
                    $('#edit_profile_end').append('<a class="btn btn-success" id="submit_state" href="/profile"><i class="icon_check_alt2" style="font-size:18px;"></i> تم الحفظ (إضغط لإعادة تحميل الصفحة)</a>');
                    //window.location.reload();
                }
                else {
                    if (data.error_name) {
                      $('#error_name').text('يجب أن يحتوى الاسم على حروف فقط');
                      $('#error_name').toggle();
                    }
                    if (data.error_email) {
                      $('#error_email').text('بريد إلكتروني غير صحيح');
                      $('#error_email').toggle();
                    }
                    if (data.email==='used') {
                      $('#error_email').text('هذا البريد الإلكتروني مستخدم من قبل');
                      $('#error_email').toggle();
                    }  
                  }
            });
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
    
    // process the edit basic info form
    $('#edit_contact').submit(function(event) {

        $('#edit_contact').append('<img src="/style/img/loader.gif" id="loading">');
        $('.contact_error').css('display','none');
        $('#submit_state').remove()
        var formData = {
            'f'    : $('input[name=f]').val(),
            't'    : $('input[name=t]').val(),
            'g'    : $('input[name=g]').val(),
            'i'    : $('input[name=i]').val(),
            'ajax' : 't'
        };
        var ajax_data = {
            type        : 'POST', 
            url         : '/profile/changecontact', 
            data        : formData,
            dataType    : 'json', 
            encode      : true
        }
        $.ajax(ajax_data)
            .done(function(data) {
                console.log(data);
                $('#loading').remove();
                if (data.change_contact===true) {
                    $('#edit_contact_end').append('<a class="btn btn-success" id="submit_state" href="/profile"><i class="icon_check_alt2" style="font-size:18px;"></i> تم الحفظ (إضغط لإعادة تحميل الصفحة)</a>');
                    //window.location.reload();
                    }
                else {
                    if (data.error_f) {
                      $('#error_f').text('الرابط غير صالح');
                      $('#error_f').toggle();
                    }
                    if (data.error_t) {
                      $('#error_t').text('الرابط غير صالح');
                      $('#error_t').toggle();
                    }
                    if (data.error_g) {
                      $('#error_g').text('الرابط غير صالح');
                      $('#error_g').toggle();
                    }
                    if (data.error_i) {
                      $('#error_i').text('الرابط غير صالح');
                      $('#error_i').toggle();
                    } 
                  }
                });
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

});




