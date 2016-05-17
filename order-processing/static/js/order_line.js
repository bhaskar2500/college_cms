

  // var alert_change=["qc-packaging","seller-accepted"];
  function clos(){

 $('.btn-danger').on('click',function () { $("#modal-start").remove();});  

   $('.close').on('click',function () { $("#modal-start").remove();});

  }

  function bb(thisEl,params,message,prev_stat,comm_dict){

  b=bootbox.dialog 
    ({
      title: " T",
      message: 
 '<div class="modal" id="modal-start" style="box-shadow:none">' +
     '<div class="modal-header">' +
        '<h3 class="title">Confirmation of order status change</h3>' +
     '</div>' +
      
  '<div class="modal-body" >' +
     '<div style="display:block;"> Orderline :'+params['order_line_id']+'</div>'+
     '<div style="display:inline-block"> Old status:'+prev_stat.toUpperCase()+'</div>'+'---->'+'<div style="display:inline-block">Selected-status:'+params['order_status'].toUpperCase()+'</div>'
      +'<div style="display:block">Mode of communication</div>'+
   '<table width="400px" cellpadding="1">'+
       '<tr><td colspan="2" style="text-align:center ;border:1px solid black;">'
       +'<label> Customer </label> ' +
       '</td>'+
       '<td colspan="2" style="padding-left:0px;text-align:center; border:1px solid black;">'+'<label> Vendor</label> ' +
       '</td>'+'</tr>'
       +'<tr>'+
      '<td>'+
        '<label> <input type="checkbox" name="message" id="user_sms" value="sms_seller" >Sms</label> ' +
      '</td> <td><label> <input type="checkbox" name="message" id="user_email" value="email_seller" >Email</label> </td>'+
      '</td>'+
      '<td >'+
      '<label><input type="checkbox" name="message" id="seller_sms" value="sms_vendor" > Sms</label> ' +
      '</td> <td><label><input type="checkbox" name="message" id="seller_email"  value="email_vendor">Email</label> </td>'+
      '</tr>'+
      ' </table>'+

 +'</div>'
 +'</div>',
 animation:false,
backdrop:false,
      buttons:
  { 
      success:
    {
      label:"Change Status",
      callback:function(e)
      {
      
       message=[];
      $("input[name='message']:checked").each(function(){ message.push($(this).val()); }) ;
      params['message']=message;


      if (message.length!=0){
      $('.btn-default').text('Sending...');
      console.log("-----> wait ");    
      onsave(thisEl,params,message,prev_stat);
 

      
      return false;
      }
      else {
              onsave(thisEl,params,prev_stat);


      }


    }
  },
      
      "Danger!":
    { 
      
      label:"Cancel",
      callback:function()
        {
          oncancel(thisEl, prev_stat);
        }
    }


  },  onEscape: function() { oncancel(thisEl,prev_stat );}


   });
b.find('.modal-body').css({'background':'#ffffff','border-bottom':'0px',"height":"86px","overflow":"hidden"} );

b.find('.modal-footer').css({'background':'#ffffff','z-index':'1100','position':'relative','border-top':'0px','margin-top':'10px','padding-top':'0px'} );
b.find('.btn-default').css({'background':'#2f96b4','color':'#000000','width':'auto','font-size':'13px'});
b.find('.btn-primary').css({'background':'#B94A48','color':'white'});


  }
function close_modal(thisEl,prev_stat){

      $(".btn-danger").on('click',function () { $("#modal-start").remove();});  

   $(".close").on('click',function () { $("#modal-start").remove();});
   oncancel(thisEl,prev_stat);
  }
function post(params)
  {
 
      
$.post('/admin/orders/change_status', params,function(data) 
{

  data = JSON.parse(data);
  if(data.status_code == 200) 
      {
        $('.in').remove();
      $(".modal-dialog").remove();
          $("#modal-start").hide();


        console.log('hidden saaweaew');

        alert('Changes successfully saved for order id: '+ params["order_line_id"]);
      }
  else
      {$('.in').remove();
        $(".modal-dialog").remove();
            $("#modal-start").hide();

        alert('Error while updating:' + data.status_msg);
      }

});


}
  
function oncancel(thisEl, prev_stat)
  {
    console.log('---------> after cancel', prev_stat);    
    var x=$(thisEl).attr('data-selected_status',prev_stat).val(''); // find a select with value prev_stat and set its value null 
    console.log(x);
    x.find('option[value="'+ prev_stat+'"]').prop('selected', true);
    $(thisEl).focus();
       
  }
function onsave(thisEl,params,prev_stat)
{

    var x=$(thisEl).attr('data-selected_status',params['order_status']).val('');
     // select with value ordr_stat and set its value null 
    console.log(params['message']);
     x.find('option[value="'+ params['order_status']+'"]').prop('selected', true);
    console.log($(thisEl),'---->----------------------------ew',prev_stat);
    $(thisEl).focus();
        params['prev_stat']=prev_stat;
        console.log(params['prev_stat'],'=========================');
      post(params);                 
   

  }
