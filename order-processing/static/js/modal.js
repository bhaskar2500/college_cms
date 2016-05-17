
  function create_strap()
  {

    $('body').append('<div class="modal" id="modal-start">' +
       '<div class="modal-header">' +
         '<button type="button" class="close" data-dismiss="modal">×</button>' +
         '&nbsp;&nbsp;<b><p style="font-size:14px;">Select date and time on which pick up from the seller will be initiated .'+
        '</p>' +
       '<div class="modal-body" style="padding:0px;">' +
        '<input  type="text"  id="datetimepickers"  name="datetimepicker" data-provide="datetimepicker"/>'
        +'</div>'+
       '<div class="modal-footer" >' +
        '<table width="200px" style="float:left; border:1px solid black;  ">'+
       '<tr><td colspan="2  " style="text-align:center; border:1px solid black">'
       +'<label>Customer</label> ' +
       '</td>'+
       '<td colspan="2" style="text-align:center;padding-left:22px ;border:1px solid black"><label>Vendor</label> ' +
       '</td>'+'</tr>'+
       '<tr>'+'<td colspan="2">'
       +'<tr> <td>'+
      '<label><input type="checkbox" name="message"  id="user_sms" value="sms_seller">Sms</label> ' +
      '</td> <td><label> <input type="checkbox"   name="message" id="user_email" value="email_seller"> Email</label> </td>'+
      '</td>'+
      '<td >'+
      '<label> <input type="checkbox"  name="message" id="seller_sms" value="sms_seller">Sms</label> ' +
      '</td> <td><label><input  type="checkbox" name="message" id="seller_email" value="email_seller">  Email</label> </td>'+
      '</td></tr> </table>'+




         '<a href="#" class="btn btn-danger" value="cancel" data-dismiss="modal">Cancel</a>' +
         '<a href="#" class="btn btn-success" value="change_status">Change Date & Send</a>' +
       '</div>'

  );  
  }
 