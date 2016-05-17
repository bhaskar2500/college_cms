function checkboxes(comm_dict)

{
    var keys = [];
  for (var key in comm_dict) 
    {
        keys.push(key);
    }
    console.log(keys);

    keys.forEach(function(key){  

        var value = comm_dict[key];
        
    if (key=='cust_mail' && value=='\u0000')
      {     
       $('#user_email').parent('label').hide(); 

       
      }
      else if (value=='\u0001' && key=='cust_mail')

      {
        $('#user_email').prop('checked',true);
      }


       if (key=='seller_sms' && value=='\u0000')
      {     
       $('#seller_sms').parent('label').hide(); 


      }
            else if (value=='\u0001' && key=='seller_sms')

     {
          $('#seller_sms').prop('checked',true);      
      }

     if (key=='seller_email' && value=='\u0000')
     {      
       $('#seller_email').parent('label').hide(); 

      }
      else if(value=='\u0001' && key=='seller_email')
      {
        $('#seller_email').prop('checked',true);
      }
     if (key=='cust_sms' && value=='\u0000')
      {     
       $('#user_sms').parent('label').hide(); 

       
      }
       else if(value=='\u0001' && key=='cust_sms')
      {
       $('#user_sms').prop('checked',true)
      }
        // Use `key` and `value`
    });  
  }


$(document).ready(function(){
  fields_data();
  edit();
console.log('This is hello from github');
  var prev_stat='';
  var particular=['processing','qc-packaging','delivered']

  $('.field-custom_stat').on('focus','select',function () {
           // Store the current value on focus and on change
        prev_stat = $(this).val();
                console.log('on focus', prev_stat);


  }).on('change', 'select', function() {
      var thisEl = this;    
     $(this).blur();
      header_id=$(this).parents('tr').find('.field-order_id').text();    
      console.log(header_id);

     var params = {
              'order_line_id': $(this).parents('tr').find('.field-order_line_id').text(),
              'order_status': $(this).val(),
              'date':null ,
              'header_id':header_id,
              'message':null ,
                  }

  
    comm_dict=$(this).find("option:selected").data('comm')
    console.log(comm_dict);
    console.log(comm_dict['seller_email']);

if(!$(this).val()) 
    {
      alert('Status cannot be left blank !'+params['header_id']);
      return false;
    }


else //Ask for the confirmation of changing status
{
  console.log('prev staaaaaaaaaaaaat',prev_stat);
  thisEl=$(this);
  message=null;
  if (params["order_status"]=="seller-accepted")
  {      
          
    create_strap();
    checkboxes(comm_dict);
    var date=$('input[name="datetimepicker"]').datetimepicker({ });  
    $('.btn-success').one("click",function(e)
     {
     message=[];
    $("input[name='message']:checked").each(function(){ message.push($(this).val()); }) ;
    params['message']=message;

    console.log('date',date);
    params['date']=date.val()+':00';
    new_date=new Date(date.val());
    new_date=new_date.toString();
    date_array=new_date.split(' '); 
    django_date=date_array[1]+'. '+date_array[2]+', '+date_array[3]+" "+date_array[4];

    set_date=thisEl.parents('tr').find('.field-pickup_date').html(django_date+'<input type="button" class="pick_button" value="Change"/>');
    



  if(date==null)
     {
      alert('date cant be empty');
      oncancel(thisEl,prev_stat);
      return;
     }    


if(message.length!=0)
{
 $('.btn-success').text('Sending...');
      console.log("-----> wait ");    
      onsave(thisEl,params,message,prev_stat);

      return false;
}
else 
{
    onsave(thisEl,params,message,prev_stat);


}

  });

  close_modal(thisEl,prev_stat);
  }
else 
  {  
    params['prev-stat']=prev_stat;

    console.log(params);
    bb(thisEl,params,message,prev_stat);
    console.log(comm_dict);
    b=comm_dict;

    checkboxes(comm_dict);

  }



  }
 

                
});
});