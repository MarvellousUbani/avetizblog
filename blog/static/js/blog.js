$('#menubutton').click(function(){
      var menu=$('.menu').css("display")
    if (menu=='none'){
      $(".menu").css("display","block").fadeIn('slow');
    }
     if(menu=='block'){
      $(".menu").css("display","none")
     }

    })

$(".navbar-toggle, .navbar-brand").on("click", function () {
     $("#navbar-hamburger").toggleClass("active");
     $(".social-icon").toggleClass("hidden");
  });

$(document).on('click',function(){
   $('#navbar-hamburger').removeClass("active");
});

    $(document).ready(function(){
      console.log('im here')
      navheight=$('#headernav').height();
      $('.menu').css('top',navheight);
      width=$(window).width()
      if (width < 992 && width >= 768){
      
      $('img.js-third').parent().css('display', 'block')
      sideheight=$('.post-box').height()/4;
      $('.js-third').height(sideheight);
      }
      if (width < 768){
          //$('img.js-third').parent().css('display', 'none')
        }
      if (width >= 992){
          
          $('img.js-third').parent().css('display', 'block')
          sideheight=$('.post-box').height()/4;
          $('.js-third').height(sideheight);
          
          console.log($('.js-firstside').width())
        }

      $(window).resize(function(){
        navheight=$('#headernav').height();
        $('.menu').css('top',navheight);
        width=$(window).width()
        
        if (width < 992 && width >=768){
          $('img.js-third').parent().css('display', 'block')
          sideheight=$('.post-box').height()/4;
          $('.js-third').height(sideheight);
        }

        if (width < 768){
         // $('img.js-third').parent().css('display', 'none')
        }
        if (width >= 992){
          
          $('img.js-third').parent().css('display', 'block')
          sideheight=$('.post-box').height()/4;
          $('.js-third').height(sideheight);
          
          console.log($('.js-firstside').width())
        }
      })
      })



 $(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-product").modal("show");
      },
      success: function (data) {
        $("#modal-product .modal-content").html(data.html_form);
      
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    var formdata = new FormData(form);
    //console.log(formdata)
    $.ajax({
      url: form.attr("action"),
      data: formdata,//form.serialize(), //formData,
      type: form.attr("method"),
      //processData: false,
      contentType: false,
      success: function (data) {
        if (data.form_is_valid) {
          $("#product-table tbody").html(data.html_list);
          $("#modal-product").modal("hide");
        }
        else {
          $("#modal-product .modal-content").html(data.html_form);
        }
      },
      error: function (theRequest, theStatus, theError) 
     {
        alert(theError);
    },
      
    });
    return false;
  };

var makePayt = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      async:false,
      dataType: 'json',
      success: function(dic) {
        if (dic.form_is_valid) {
          payWithPaystack(dic)
          //$("#product-table tbody").html(data.html_list);
          $("#modal-product").modal("hide");
         
        }
        else {
          $("#modal-product .modal-content").html(dic.html_form);
        }
      },
      error: function (e) {
        alert('error')
      },
    });
    return false;
  };

  function payWithPaystack(data){
    var handler = PaystackPop.setup({
      key: 'pk_test_d7ed8771f755bc62d8d023a93e531101a3ac4eb8',
      email: data.email,
      amount: data.amount,
      metadata: {
        cartid: data.id,
        orderid: data.id,
        custom_fields: [
          {
            display_name: "Paid on",
            variable_name: "paid_on",
            value: 'AvetiZBlog'
          },
          {
            display_name: "Paid via",
            variable_name: "paid_via",
            value: 'Inline Popup'
          }
        ]
      },
      callback: function(response){
        // post to server to verify transaction before giving value
        var verifying = $.get( '/verify.php?reference=' + response.reference);
        verifying.done(function( data ) { /* give value saved in data */ });
      },
      onClose: function(){
        alert('Click "Pay now" to retry payment.');
      }
    });
    handler.openIframe();
  }
  $(".js-add-product").click(loadForm);
  $("#modal-product").on("submit", ".js-product-create-form", saveForm);

  // Update Product
  $("#product-table").on("click", ".js-update-product", loadForm);
  $("#modal-product").on("submit", ".js-post-update-form", saveForm);

  //Delete Product
  $("#product-table").on("click", ".js-delete-product", loadForm);
  $("#modal-product").on("submit", ".js-post-delete-form", saveForm);

  //Submit Product
  $("#product-table").on("click", ".js-submit-product", loadForm);
  $("#modal-product").on("submit", ".js-post-submit-form", saveForm);

  //make payment
  $(".js-add-transaction").click(loadForm);
  $("#modal-product").on("submit", ".js-transaction-submit-form", makePayt);

  //create Advert
  $(".js-add-advert").click(loadForm);
  $("#modal-product").on("submit", ".js-advert-submit-form", saveForm);
 
});
