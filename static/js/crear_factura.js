
$(document).ready(function() {
	//Elementos que componen la ventana modal buscar cliente.
	$modalBuscarCliente = $('div#modal-buscar-cliente');
	$formBuscarCliente = $('form#form-buscar-cliente');
	$btnBuscarCliente = $('button#btn-buscar-cliente');
	$preloaderBuscarCliente = $('div#preloader-buscar-cliente');
	$respuestaBuscarCliente = $('div#respuesta-busqueda-cliente');

	//Elementos que componen la ventana modal agregar cliente.
	$modalAgregarCliente = $('div#modal-agregar-cliente');
	$formAgregarCliente = $('form#form-agregar-cliente');
	$btnAgregarCliente = $('button#btn-agregar-cliente');
	$preloaderAgregarCliente = $('div#preloader-agregar-cliente');

	//Elementos donde se visualizan los datos del cliente en la factura.
	$infoCliente = {
		'cedula': $('div#cedula-cliente'),
		'nombre': $('div#nombre-cliente'),
		'direccion': $('div#direccion-cliente'),
		'ciudad': $('div#ciudad-cliente'),
		'telefono': $('div#telefono-cliente')	
	}

	/* Muestra la información del cliente en la factura.*/
	function mostrarInfoCliente(datos) {
		for (campo in datos) {
			try {
				$infoCliente[campo].text(datos[campo]);
			} catch(err) {console.log(err)}
		}
	}

	/*
	Envía una petición XMLHttpResquest al servidor por el método POST.
	Los datos se envían en formato JSON.
	*/
	function enviarPeticionAJAX(datos, url, csrfmiddlewaretoken, procesarRespuesta) {
		$.ajax({
			type: 'POST',
			data: JSON.stringify(datos),
			dataType: 'json',
			headers: {
				'X-CSRFToken': csrfmiddlewaretoken,
				'Content-Type': "application/json; charset=UTF-8"
			},
			url: url,
			success: function(data) { procesarRespuesta(data) }
		});
	}

	/* Esta función se ejecuta cuando el formulario de buscar cliente
	es enviado. */
	$formBuscarCliente.on('submit', function(event) {
		//Se evita que la página se recargue.
		event.preventDefault();
		//Se desactiva el botón submit del formulario.
		$btnBuscarCliente.addClass('disabled');
		//Se muestra la barra de cargando.
		$preloaderBuscarCliente.fadeIn();

		//Datos que serán enviados al servidor.
		dato = {
			"cedula": this['cedula'].value
		};

		/*  
		Mediante el objeto AJAX se envía una petición al servidor.
		En este caso se envía el número de cédula del cliente, para 
		consultar sus datos.
		Los datos son enviados a través de un objedto JSON.
		*/

		function procesarRespuestaBuscarCliente(data) {
			if (data.response == "success") {
					mostrarInfoCliente(data);
					$modalBuscarCliente.modal('close');
					$formBuscarCliente[0].reset();
					$respuestaBuscarCliente.fadeOut();
			}
			else { 
				$respuestaBuscarCliente.text(data.mensaje).fadeIn();
			}

			$preloaderBuscarCliente.fadeOut(1000);
			$btnBuscarCliente.removeClass('disabled');
		}

		enviarPeticionAJAX(dato, 'buscar-cliente', this['csrfmiddlewaretoken'].value, procesarRespuestaBuscarCliente);
	});


	/* Esta función se activa cuando el formulario de agregar cliente
	es enviado. */
	$formAgregarCliente.on('submit', function(event) {
		event.preventDefault();
		$btnAgregarCliente.addClass('disabled');
		$preloaderAgregarCliente.fadeIn(500);

		//Mensajes de los formularios
		$contenedoresMensaje = {
			'cedula': $('div#message-input-cedula'),
			'nombres': $('div#message-input-nombres'),
			'apellidos': $('div#message-input-apellidos'),
			'ciudad': $('div#message-input-ciudad'),
			'direccion': $('div#message-input-direccion'),
			'telefono': $('div#message-input-telefono')
		}

		//Se limpian los mensajes de los contenedores.
		for (contenedor in $contenedoresMensaje) {
			$contenedoresMensaje[contenedor].fadeOut(500);
		}

		//Datos que serán enviados al servidor.
		datos = {
			"cedula": this['cedula'].value,
			"nombres": this['nombres'].value,
			"apellidos": this['apellidos'].value,
			"ciudad": this['ciudad'].value,
			"direccion": this['direccion'].value,
			"telefono": this['telefono'].value
		}

		/*  
		Mediante el objeto AJAX se envía una petición al servidor.
		En este caso se envía el número de cédula del cliente, para 
		consultar sus datos.
		Los datos son enviados a través de un objedto JSON.
		*/
		function procesarRespuestaAgregarCliente(data) {
			if (data.response === 'success') {
				console.log('ok...');
				console.log(data);
				mostrarInfoCliente(data);
				$modalAgregarCliente.modal('close');
				$modalBuscarCliente.modal('close');
				$formAgregarCliente[0].reset();
				$formBuscarCliente[0].reset();
				$respuestaBuscarCliente.fadeOut();
			}
			else if (data.response === 'error') {	
				for (campo in data.errors) {
					$contenedoresMensaje[campo].text(data.errors[campo]).fadeIn(1000);
				}
			}
			
			$btnAgregarCliente.removeClass('disabled');
			$preloaderAgregarCliente.fadeOut(500);
		}

		enviarPeticionAJAX(datos, 'registrar-cliente', this['csrfmiddlewaretoken'].value, procesarRespuestaAgregarCliente);
	});
});