$(function(){


	//Registrar cuenta


	//espacios adelante y atras


	//solo letras en nombre
	$("#nombre").keypress(function soloLetras(e){
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = "8-37-39-46";

    tecla_especial = false
    for(var i in especiales){
   	    if(key == especiales[i]){
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla)==-1 && !tecla_especial){
        return false;
    }
}

		);


//validacion rut
function check_rut(){
	var campo = $("#rut").val();
	if ( campo.length == 0 ){
		error_message ="RUN INVÁLIDO";
		error_rut=true;
	}else{
		if ( campo.length < 8 ){
			error_message = "RUT INVÁLIDO";
			error_rut=true;
		} else{
			campo = campo.replace('-','')
			campo = campo.replace(/\./g,'')
			var suma = 0;
			var caracteres = "1234567890kK";
			var contador = 0;    
			for (var i=0; i < campo.length; i++){
				u = campo.substring(i, i + 1);
				if (caracteres.indexOf(u) != -1)
				contador ++;
			}
			if ( contador==0 ) {
				error_message = "RUN INVÁLIDO";
				error_rut=true;
			} else{
			
				var rut = campo.substring(0,campo.length-1)
				var drut = campo.substring( campo.length-1 )
				var dvr = '0';
				var mul = 2;
				
				for (i= rut.length -1 ; i >= 0; i--) {
					suma = suma + rut.charAt(i) * mul
			                if (mul == 7) 	mul = 2
					        else	mul++
				}
				res = suma % 11
				if (res==1)		dvr = 'k'
			                else if (res==0) dvr = '0'
				else {
					dvi = 11-res
					dvr = dvi + ""
				}
				if ( dvr != drut.toLowerCase() ) {
					error_message = "RUN INVÁLIDO";
					error_rut=true;
				}
			}
		}
	}
}
function check_contrasenasIguales(){
	if ($("#contrasena").val() == $("#contrasena2").val()){
		error_contrasena=false;

	}else{
		error_message="Las contraseñas no coinciden";
		error_contrasena=true;
	}
	
}
function check_fechaNacimiento(){
	fecha = new Date($("#fec_nac"))
	hoy = new Date()
	ed = parseInt((hoy -fecha)/365/24/60/60/1000)
	if (ed < 16) {
		error_message="Eres menor de 16!!";
		error_fecha=true;
	}
	error_fecha=false;
	
}

$("#registraPersona").submit(function() {
		error_message="";
		error_rut=false;
		error_contrasena=false;
		error_fecha=false;
		check_rut();
		check_contrasenasIguales();
		var nom=$("#nombre").val();
		nom=$.trim(nom);
		$("#nombre").val(nom);
		if(error_rut==false && error_contrasena==false && error_fecha==false && nom!=""){
				
				$("#registraPersona").submit();

		}else{
			if(nom==""){
				alert("No se puede usar solo espacios");
				return false;
			}
			
			else{
			alert(error_message.toLowerCase());
			return false;	
			}
			
		}

	});


//Actualizar datos
$("#actualizaDatos").submit(function() {
		// if($("#nombre").val()=="" && $("#nombre").val()==null &&
		// $("#comuna").val()=="" && $("#comuna").val()==null &&
		// $("#correoAsociado").val()=="" && $("#correoAsociado").val()==null  ){
		// 		alert("Todos los campos estan en blanco, no se han realizado cambios javascrip");
		// 		return false;
		// }else{
		// 	$("#actualizaDatos").submit();
		// 	alert("Datos actualizados correctamente javascript");
		// }
		var nom=$("#nombre").val();
		nom=$.trim(nom);
		$("#nombre").val(nom);
	});

//Cambiar Contraseña
$("#cambiaContrasena").submit(function() {
		var actual=$("#actual").val();
		actual=$.trim(actual);
		$("#actual").val(actual);

		var contrasena1=$("#contrasena1").val();
		contrasena1=$.trim(contrasena1);
		$("#contrasena1").val(contrasena1);

		var contrasena2=$("#contrasena2").val();
		contrasena2=$.trim(contrasena2);
		$("#contrasena2").val(contrasena2);


		if($("#actual").val()=="" || $("#contrasena1").val()=="" || $("#contrasena2").val() ==""){
			alert("No puedes rellenar los campos con espacios!!!");
			return false;
		}else{
			if($("#contrasena1").val()!=$("#contrasena2").val()){
				alert("Las contraseñas no coinciden!");
				return false;
			}else{
				return true;
			}

		}
	});

//Recuperar contraseña 1
$("#recuperaContrasena1").submit(function() {


		error_message="";
		error_rut=false;
		check_rut();
		if(error_rut==true){
			alert(error_message.toLowerCase());
			return false;	
		}else{

				return true;
			}
		
	});

//Recuperar contraseña 2
$("#recuperaContrasena2").submit(function() {

		var contrasena1=$("#contrasena1").val();
		contrasena1=$.trim(contrasena1);
		$("#contrasena1").val(contrasena1);

		var contrasena2=$("#contrasena2").val();
		contrasena2=$.trim(contrasena2);
		$("#contrasena2").val(contrasena2);


		if($("#contrasena1").val()=="" || $("#contrasena2").val() ==""){
			alert("No puedes rellenar los campos con espacios!!!");
			return false;
		}else{
			if($("#contrasena1").val()!=$("#contrasena2").val()){
				alert("Las contraseñas no coinciden!");
				return false;
			}else{
				return true;
			}

		}
		
	});


//Eliminar cuenta
$("#eliminaCuenta").submit(function() {
		if (confirm("Todas sus reservas van a eliminarse")){
			return true;
		}
		else{
			return false;
		}

	});


});
