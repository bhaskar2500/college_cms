
$(document).ready(function() 
{
  

   function clos(){

 $('.btn-danger').on('click',function () { $("#modal-start").remove();});  

   $('.close').on('click',function () { $("#modal-start").remove();});

  }


   var alert_change=["qc-packaging","seller-accepted"];

  $pick_edit='<input type="button" class="pick_button" value="Change">';
   
    $(document).ready(function(){

  $('.field-pickup_date').each(function() {
        order_stat=$(this).parents('tr').find('.field-custom_stat').find('option:selected').val();
        console.log(order_stat);
      if (($.inArray(order_stat,alert_change)+1))
    {
    $(this).append($pick_edit);
    }
   }); 


});
  
  $('body').on('click', '.pick_button', function(){  
    b=$(this);
    comm_dict=b.parents('tr').find('.field-custom_stat').find('option:selected').data('comm');
    console.log('---------',comm_dict);
    checkboxes(comm_dict);  
    
    order_stat=b.parents('tr').find('.field-custom_stat').find('option:selected').val();

    create_strap();
  clos();
  prev_date=b.parents('tr').find('.field-pickup_date').text();  
  date=$('input[name="datetimepicker"]').datetimepicker({});


$('.btn-success').on("click",function(e)
{  

  date=$('input[name="datetimepicker"]').datetimepicker({});
  
   line=b.parents('tr').find('.field-order_line_id').text();

     button_params={
    'order_line_id':line, 
    'message':null,'header_id':b.parents('tr').find('.field-order_id').text(),
}
     message=[];
    $("input[name='message']:checked").each(function(){ message.push($(this).val()); }) ;
    button_params['message']=message ;
    button_params['prev_date']=prev_date;
    button_params['order_status']=b.parents('tr').find('.field-custom_stat').find('option:selected').val();

    button_params['date']=date.val()+':00';
    console.log(button_params['date']);
    
    change_date=new Date(date.val()).toString();
    console.log(change_date,'passed ob');
    date_array=change_date.split(' ');
    date=date_array[1]+'. '+date_array[2]+', '+date_array[3]+' '+date_array[4];
    console.log(button_params['order_line_id'],'date',button_params['date']);
    console.log(typeof(date_array[1]));
    if (date_array[2]==undefined)
    {
      alert('date cant be null');
      return ;
    }
    post(button_params);

    htm=b.parents('td').html(date+'<input type="button" class="pick_button" value="Change"/>');
    $('#modal-start').remove();


   
  });
});
 

 });


