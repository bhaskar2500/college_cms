
function edit(){
edit_button='<input type="button" value="Edit" >';
$('.field-remarks').each(function(){

$(this).append(edit_button);
});
edit_click();
}
function edit_click()
{
$('input[value="Edit"]').on("click",function(){

	bn= this;
			id=$(this).parentsUntil('tr').find('.field-order_line_id').val();

		console.log('id-------------->',id)

	value=$(bn).parents('.field-remarks').text();
	prams={}
	prams['old_value']=value;
	$(this).hide();
	$(this).parents('.field-remarks').html('<input type="hidden" name="id"/><textarea name="text" id="area" rows="1" cols="5" >'+value+'</textarea> <input type="button" value="Save" > <input type="button" value="Cancel" >');
	
	console.log('iiiiiiiiddddddddddd',id);
});
		var prams = {};

	
	$('.field-remarks').on('click', 'input[value="Save"]',function()

	{	
		console.log('------------------------------weeeeeeeeeeeeee--------',prams['old_value']);
		$(bn).show();
		var id= $(this).parents('tr').find('.field-order_line_id').text();
		var new_remarks = $(this).parents('.field-remarks').find('textarea').val();
			prams['id'] = id;
		prams['value'] = new_remarks;
		console.log(prams);
		$(this).parents('.field-remarks').html(new_remarks+'<input type="button" value="Edit" />')

		$.post('/admin/orders/remarks/',prams);
		// if($(this).parents('.field-remarks').find('input[value="Edit"]).data('clicked',true))
		// {
		edit_click();

	});


$('.field-remarks').on('click', 'input[value="Cancel"]', function()
	{
		console.log(edit_button);
		var new_remarks = $(this).parents('.field-remarks').text();

	

	$(this).parents('.field-remarks').html(new_remarks+'<input type="button" value="Edit" />');
	edit_click();

	});


}