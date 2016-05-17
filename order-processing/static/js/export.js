function fields_data(){
field_value=window.location.search;

$('#toolbar').append('<input type="button" name="Export" value="Export all" class="btn"/>')


console.log(field_value,'aaa');
$("input[name='Export']").on("click",function(){

if (field_value.search('status__exact')||field_value.search('store_id')||field_value.search('order_line_id') )
	{
		if(field_value.length!=0)
		{
		console.log('not entered');
		window.location.href='/admin/orders/as_excel/'+field_value;
	} 

	}

if($('#changelist-form :checked').val()=='on')
	{

		window.location.href='/admin/orders/as_excel/?all=all';
	}
		
else{
objects={};

	objects['selected_val']=[];
$(".action-checkbox").find("input").each(function(){

		if ($(this).prop('checked')==true){

			objects['selected_val'].push($(this).val());
			
			}

	});
}
console.log(objects,'aaaaaaaaaa');

if ($('.action-select').prop('checked')==true)
{

window.location.href='/admin/orders/as_excel/?selected_val='+objects['selected_val'];

}

	});

}

// function get_excel(field_data)
// {


// $.get('/admin/orders/as_excel/',field_data);

// }
// while(i<arr.length && arr[i]!="")
// {
// 	console.log(arr.length);	

// 	if (arr[i].search('status__exact')||arr[i].search('store_id'))
// 		{
// 			temp=arr[i];
// 			new_arr=arr[i].split('=');
// 			console.log(new_arr);
// 			field_data[new_arr[0].toString()]=new_arr[1].toString();
// 			window.location.href='/admin/orders/as_excel/?'+field_data
// 			console.log(field_data);


// 		}
// 		else
// 		{


// 			console.log('aaaaaaaaaaaaa');
// 		}
// 	i++;

// }
