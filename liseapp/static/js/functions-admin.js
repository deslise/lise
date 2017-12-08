
console.log('functions-admin');

var updateData = function() {
    console.log('update-data');
    var loading = $('#loading');
    var content = $('#content_update');
    loading.show();
    content.hide();
    $.ajax({
        url: '/admin/update_data/',
        dataType:'json',
        success: function(data){
            console.log('ok');
            location.reload();
        }
    });
}

function editItem(id){
    var item = $('#item'+id);
    console.log(item);
    item.hide();
    window.open('/admin/managedata/itemtopic/'+id, '_blank');
}
function recusarItem(id){
    var item = $('#item'+id);
    console.log(item);
    item.hide();
	$.ajax({
		url: '/admin/recusar_item/'+id,
		dataType:'json'
	});
}

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("searchByCat");
  filter1 = input.value.toUpperCase();
  input = document.getElementById("searchByTop");
  filter2 = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
    var td1 = tr[i].getElementsByTagName("td")[1];
    var td2 = tr[i].getElementsByTagName("td")[2];
    tr[i].style.display = "";
    if (filter1 && filter2){
    	if (td2.innerHTML.toUpperCase().includes(filter2) && td1.innerHTML.toUpperCase().includes(filter1)){
    		console.log('ok');
    		tr[i].style.display = "";

    	}else{
			tr[i].style.display = "none";
    	}
    }else if (filter1 || filter2){
		if (filter1 && td1.innerHTML.toUpperCase().includes(filter1)) {
			tr[i].style.display = "";
		}else if (filter2 && td2.innerHTML.toUpperCase().includes(filter2)) {
			tr[i].style.display = "";
		} else {
			tr[i].style.display = "none";
		}
	}
  }
}
