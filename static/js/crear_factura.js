
$(document).ready(function() {
	/********** VARIABLES DEL COMPONENTE BUSCAR Y AGREGAR CLIENTE **********/

	/****** Elementos que componen la ventana modal buscar cliente. *****/
	$modalBuscarCliente = $('div#modal-buscar-cliente');
	$formBuscarCliente = $('form#form-buscar-cliente');
	$btnBuscarCliente = $('button#btn-buscar-cliente');
	$preloaderBuscarCliente = $('div#preloader-buscar-cliente');
	$respuestaBuscarCliente = $('div#respuesta-busqueda-cliente');
	$triggerAgregarCliente = $('a#trigger-agregar-cliente');

	/****** Elementos que componen la ventana modal agregar cliente. ******/
	$modalAgregarCliente = $('div#modal-agregar-cliente');
	$formAgregarCliente = $('form#form-agregar-cliente');
	$btnAgregarCliente = $('button#btn-agregar-cliente');
	$preloaderAgregarCliente = $('div#preloader-agregar-cliente');

	/***** Elementos donde se visualizan los datos del cliente en la factura. *****/
	$infoCliente = {
		'cedula': $('div#cedula-cliente'),
		'nombre': $('div#nombre-cliente'),
		'direccion': $('div#direccion-cliente'),
		'ciudad': $('div#ciudad-cliente'),
		'telefono': $('div#telefono-cliente')	
	}

	/********** VARIABLES DEL COMPONENTE BUSCAR Y AGREGAR PRODUCTO **********/

	/* Elementos que componen la ventana modal buscar producto. */
	$modalBuscarProducto = $('div#modal-buscar-producto');
	$formBuscarProducto = $('form#form-buscar-producto');
	$btnBuscarProducto = $('button#btn-buscar-producto');
	$respuestaBuscarProducto = $('div#respuesta-busqueda-producto');
	$preloaderBuscarProducto = $('div#preloader-buscar-producto');

	/***** Elementeos donde se visualizan los datos del producto *****/
	$infoProducto = {
		'nombre': $('div#nombre-producto'),
		'marca': $('div#marca-producto'),
		'precio': $('div#precio-producto'),
		'stock': $('div#stock-producto'),
	}

	/* Este formulario envía una petición para agregar un nuevo producto a la factura. */
	$formAgregarProducto = $('form#form-agregar-producto');
	/* En este input se muestran la cantidad de productos que van a ser comprados */
	$cantidadProducto = $('select#input-cantidad');
	/*Botón para realizar para enviar el formulario*/
	$btnAgregarProducto = $('button#btn-agregar-producto');
	//Contenedor para mostrar los mensajes del formulario.
	$respuestaAgregarProducto = $('div#respuesta-agregar-producto');
	//preloader
	$preloaderAgregarProducto = $('div#preloader-agregar-producto');
	

	/********** DEFINICIÓN DE FUNCIONES **********/

	/* 
	Muestra la información de los clientes y los productos.
	contenedores: Son los elementos donde se muestran los mensajes.
	valores: Es la información. 
	*/
	function mostrarInfo(contenedores, valores) {
		for (campo in valores) {
			try {
				contenedores[campo].text(valores[campo]).fadeIn();
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

	/********** ASIGNACIÓN DE EVENTOS **********/

	/***** FORMULARIO BUSCAR CLIENTE *****/

	/* Esta función se ejecuta cuando el formulario de buscar cliente
	es enviado. */
	$formBuscarCliente.on('submit', function(event) {
		//Se evita que la página se recargue.
		event.preventDefault();
		//Se desactiva el botón submit del formulario.
		$btnBuscarCliente.addClass('disabled');
		//Se muestra la barra de cargando.
		$preloaderBuscarCliente.fadeIn();
		//Se oculta el botón de agregar cliente.
		$triggerAgregarCliente.fadeOut(200);

		//Datos que serán enviados al servidor.
		dato = {
			"cedula": this['cedula'].value
		};

		/*Procesa la respuesta del servidor.*/
		function procesarRespuestaBuscarCliente(data) {
			if (data.response == "success") {
					mostrarInfo($infoCliente, data);
					$modalBuscarCliente.modal('close');
					$formBuscarCliente[0].reset();
					$respuestaBuscarCliente.fadeOut(200);
			}
			else { 
				$respuestaBuscarCliente.text(data.mensaje).fadeIn();
			}

			$preloaderBuscarCliente.fadeOut(1000);
			$btnBuscarCliente.removeClass('disabled');
			$triggerAgregarCliente.fadeIn(500);
		}

		enviarPeticionAJAX(dato, 'buscar-cliente', this['csrfmiddlewaretoken'].value, procesarRespuestaBuscarCliente);
	});


	/***** FORMULARIO AGREGAR CLIENTE *****/

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

		/*Se procesa la respuesta del servidor*/
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


	/***** FORMULARIO BUSCAR PRODUCTO *****/

	$formBuscarProducto.on('submit', function(event) {
		//Se evita que la página recargue cuando se envía el formulario.
		event.preventDefault();
		//Se desactiva el botón de buscar producto, para evitar multiples peticiiones.
		$btnBuscarProducto.addClass('disabled');
		//Se muestra el preloader de buscar producto.
		$preloaderBuscarProducto.fadeIn(500);

		//Se obtienen los datos del formulario.
		dato = {'referencia': this['referencia'].value}

		function desactivarBotonAgregar() {
			$cantidadProducto.prop({'disabled': true}).html("");
			$btnAgregarProducto.addClass('disabled');
		}

		function ocultarInfoProducto() {
			for (campo in $infoProducto) {
				$infoProducto[campo].fadeOut();
			}
		}

		/*
		Esta función procesa la respuesta del servidor.
		*/
		function procesarRespuestaBuscarProducto(data) {
			console.log(data);
			if (data.response === 'success') {
				console.log('ok.. producto encontrado');
				
				mostrarInfo($infoProducto, data);
				$respuestaBuscarProducto.fadeOut();

				var options = "";

				if (data.stock > 0) {
					for (var i = 1; i < data.stock + 1; i++) {
						options += "<option value='" + i + "'>" + i + "</option>";
					}
					$cantidadProducto.html(options);

					$cantidadProducto.prop({'disabled': false});
					$btnAgregarProducto.removeClass('disabled');
					$formAgregarProducto[0]['referencia'].value = data.referencia;
				}
				else {
					$respuestaBuscarProducto.text('No hay unidades disponibles.').fadeIn();
					desactivarBotonAgregar();
				}
			}
			else { 
				$respuestaBuscarProducto.text(data.mensaje).fadeIn();
				ocultarInfoProducto();
				desactivarBotonAgregar();
			}

			$btnBuscarProducto.removeClass('disabled');
			$preloaderBuscarProducto.fadeOut();
		}

		enviarPeticionAJAX(dato, 'buscar-producto', this['csrfmiddlewaretoken'].value,procesarRespuestaBuscarProducto);
	});


	/***** FORMULARIO BUSCAR PRODUCTO *****/
	$formAgregarProducto.on('submit', function(event) {
		//Se evita que la página se recargue.
		event.preventDefault();
		//Se desactiva el botón que envía el formulario, para evitar multiples peticiones.
		$btnAgregarProducto.addClass('disabled');
		//Se activa el preloader
		$preloaderAgregarProducto.fadeIn();

		//datos que se serán enviados al servidor.
		datos = {
			"cantidad": this['cantidad'].value,
			"referencia": this['referencia'].value
		}

		/* Esta función procesa la respuesta del servidor */
		function procesarRespuestaAgregarProducto(data) {
			if (data.response === 'success') {

			}
		}

	});

});