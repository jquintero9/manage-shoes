
$(document).ready(function() {

	$modal = $('div#modal-buscar-cliente');
	$formCliente = $('form#form-buscar-cliente');
	$btnBuscarCliente = $('button#btn-buscar-cliente');

	$formCliente.on('submit', function(event) {
		event.preventDefault();

		dato = {
			"cedula": this['cedula'].value
		};

		$.ajax({
			data:JSON.stringify(dato),
			type: "POST",
			dataType: "json",
			headers: {
				"X-CSRFToken": this['csrfmiddlewaretoken'].value,
				"Content-Type": "application/json; charset=UTF-8"
			},
			url:"buscar-cliente",
			success: function(data) {
				console.log(data);
				if (data.response == "success") {
					$('div#cedula-cliente').text(data.cedula);
					$('div#nombre-cliente').text(data.nombre);
					$('div#direccion-cliente').text(data.direccion);
					$('div#ciudad-cliente').text(data.ciudad);
					$('div#telefono-cliente').text(data.telefono);
					$modal.modal('close');
				}
				else { 
					$('span#respuesta-busqueda-cliente').text(data.mensaje);
				}
			}
		});

	});

});