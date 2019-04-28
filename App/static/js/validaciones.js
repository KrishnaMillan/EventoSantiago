$(function(){

	$("#eliminaCuenta").submit(function() {
		if (confirm("Todas sus reservas van a eliminarse")){
			return true;
		}
		else{
			return false;
		}

	});
});