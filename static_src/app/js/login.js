(function(_global){
  // here is the login code using jquery
  // you can manage your own login post using another way
  // 
  $(function () {
    var LOGIN_URL = "/login/";
    var MAIN_URL = "/";
    var error={
      login:{
        "en":"username not exist or password is wrong!",
        "zh-cn":"用户名不存在或密码错误！",
        "zh-tw":"用户名不存在或密码错误！",
      }
    };
    $(document).ajaxSend(function(elm, xhr, s){
      if (s.type == "POST") {
        xhr.setRequestHeader('x-csrf-token', getcsrf());
      }
    });
    function getcsrf(){
      return $("input[name=csrfmiddlewaretoken]").val();
    }
    $.urlParam = function(name){
      var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(_global.location.href);
      if (results){
        return results[1] || null;
      }else{
        return null;
      }
    };

    function hasLocalStorage(){
      if (typeof (Storage) !== "undefined") {
        return true;
      } else {
        if (alert){
          // window.alert(config.alert.localStorage.error);
        }
        return false;
        
      }
    }
    function getLocal(name) {
      if (hasLocalStorage()){
        return localStorage.getItem(name);
      }
    }


    function redirect_to_next(){
      var next = $.urlParam('next');

      if (next){
        location.href = decodeURIComponent(next);
      }else{
        location.href = decodeURIComponent(MAIN_URL);
      }
    }
    function showError(){
      /*TO DO*/
      // console.log('show error message');
      var lang =getLocal("NG_TRANSLATE_LANG_KEY") || "en";
      $("#login_error").html(error.login[lang]);
      $("#login_form").addClass("has-error");
      $("#login_error").show();

    }
    function clearInput(){
      // $("#username").val("");
      $("#password").val("");
    }

    $('body').keypress(function (e) {
      var key = e.which;
      if(key == 13)  // the enter key code
      {
        $("#login_btn").click();
        return false;  
      }
    });

    $("#login_btn").click(function (e) {
        var isValid = true;

        if( isValid ) {
            $.ajax({
                type: "POST",
                url: LOGIN_URL,
                dataType: "json",
                data: {
                  username:$("#username").val(),
                  password:$("#password").val(),
                  csrfmiddlewaretoken:getcsrf(),
                }
            }).done(function(res){
              if (res.code === 0){
                redirect_to_next();
              }else{
                clearInput();
                showError(res.code);
              }
            });
            e.preventDefault();
            return false;
        }
        e.preventDefault();
        return false;
    });
  });

})(window);