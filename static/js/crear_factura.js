
$(document).ready(function() {
	
	var l = Array("hola");
	
	var s = "mundo";
	var indice = undefined;

	console.log(l);

	/*for (var i = 0; i < l.length; i++) {
		if (l[i] === s) {
			indice = i;
			break;
		}
	}
	*/

	l.splice(0, 1);

	console.log(l);

	function closeIt()
	{ return "";}

	window.onbeforeunload = closeIt;

	function ListaDetalle() {
		this.lista = new Array();

		this.agregarDetalle = function(detalle) {
			this.lista.push(detalle);
		}

		this.eliminarDetalle = function(referencia) {
			if (this.lista.length > 0) {
				var indiceEliminar = -1;

				for (var i = 0; i < this.lista.length; i++) {
					console.log("---------------------");
					console.log("ref1: " + this.lista[i].referencia);
					console.log("ref2: " + referencia);

					if (this.lista[i].referencia == referencia) {
						indiceEliminar = i;
						console.log("incideEliminar: " + indiceEliminar);
						break;
					}
					console.log("---------------------");
				}

				if (indiceEliminar >= 0) {
					this.lista.splice(indiceEliminar, 1);
					console.log('eliminado');
				}

				console.log("Numero de detalles: " + this.lista.length);
			}
		}

		this.getDetalle = function(referencia) {
			var detalle = null;
			
			if (this.lista.length > 0) {

				for (detalle in this.lista) {
					if (this.lista[detalle].referencia === referencia) {
						detalle = this.lista[detalle];
					}
				}
			}

			console.log("getDetalle");
				console.log(detalle);
			
			return detalle;
		}

		this.existe = function(referencia) {
			var existe = false;
			
			if (this.lista.length > 0) {

				for (detalle in this.lista) {
					if (this.lista[detalle].referencia === referencia) {
						existe = true;
					}
				}
			}
			
			return existe;
		}

	}

	function DetalleFactura(id, referencia, nombre, precio, stock) {
		this.id = id || "";
		this.referencia = referencia || "";
		this.nombre = nombre || "";
		this.precio = precio || 0;
		this.stock = stock || 0;
	}

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
	/*Botón para realizar para enviar el formulario*/
	$btnAgregarProducto = $('button#btn-agregar-producto');
	//Contenedor para mostrar los mensajes del formulario.
	$respuestaAgregarProducto = $('div#respuesta-agregar-producto');
	//preloader
	$preloaderAgregarProducto = $('div#preloader-agregar-producto');
	//Detalle de la factura.
	$detalleFactura = $('#body-factura');

	listaDetalle = new ListaDetalle();
	objetoBusquedaProducto = null;
	

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
			} catch(err) {}
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
				mostrarInfo($infoCliente, data);
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

	function desactivarBotonAgregar() {
		$btnAgregarProducto.addClass('disabled');
	}

	function activarBotonAgregar() {
		$btnAgregarProducto.removeClass('disabled');
	}

	function ocultarInfoProducto() {
		for (campo in $infoProducto) {
			$infoProducto[campo].fadeOut();
		}
	}


	/***** FORMULARIO BUSCAR PRODUCTO *****/

	$formBuscarProducto.on('submit', function(event) {
		//Se evita que la página recargue cuando se envía el formulario.
		event.preventDefault();
		//Se desactiva el botón de buscar producto, para evitar multiples peticiiones.
		$btnBuscarProducto.addClass('disabled');
		//Se muestra el preloader de buscar producto.
		$preloaderBuscarProducto.fadeIn(500);
		$respuestaAgregarProducto.fadeOut();

		//Se obtienen los datos del formulario.
		dato = {'referencia': this['referencia'].value}

		/*
		Esta función procesa la respuesta del servidor.
		*/
		function procesarRespuestaBuscarProducto(data) {
			console.log(data);
			if (data.response === 'success') {
				console.log('ok.. producto encontrado');
				
				mostrarInfo($infoProducto, data);
				$respuestaBuscarProducto.fadeOut();

				if (data.stock > 0) {
					activarBotonAgregar();
					objetoBusquedaProducto = new DetalleFactura(data.id, data.referencia, data.nombre, data.precio, data.stock);
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

	function generarSelectCantidad(referencia, stock) {
		var $select = $("<select id='select-" + referencia + "' name='" + referencia + "' class='browser-default'></select>");
		$select.append("<option value='1' selected>1</option>");

		if (stock > 1) {
			for (var i = 2; i <= stock; i++) {

				$select.append("<option value='" + i + "'>" + i + "</option>");
			}
		}

		$select.on('blur', function(event) {
			var $precioDetalle = $('input#precio-' + referencia);
			var $totalDetalle = $('input#total-' + referencia);
			var cantidad = Number(this.value);
			var precio = Number($precioDetalle.val());
			$totalDetalle.val(cantidad * precio);
		});

		return $("<td class='select-cantidad'></td>").append($select);
	}

	function eliminarDetalle(event) {
		var referencia = this.dataset.referencia;
		var $tr = $('tr#' + referencia).remove();

		listaDetalle.eliminarDetalle(referencia);
	}

	function crearBotonEliminarDetalle(referencia) {
		var $botonEliminar = $("<a class='btn btn-floating red darken-1' data-referencia='" + referencia + "'><i class='material-icons'>delete</i></a>");
		$botonEliminar.on('click', eliminarDetalle);

		return $('<td></td>').append($botonEliminar);
	}

	function clonarObjeto() {
		var objectoClone = null;

		if (objetoBusquedaProducto != null) {
			objetoClone = new DetalleFactura(
				objetoBusquedaProducto.id,
				objetoBusquedaProducto.referencia,
				objetoBusquedaProducto.nombre,
				objetoBusquedaProducto.precio,
				objetoBusquedaProducto.stock
			);
		}

		return objetoClone;
	}

	function agregarProductoFactura(event) {

		if (objetoBusquedaProducto != null) {
			if (!listaDetalle.existe(objetoBusquedaProducto.referencia)) {
				console.log("Agregando detalle...");
				nuevoDetalle = clonarObjeto(objetoBusquedaProducto);
				objetoBusquedaProducto = null;

				var $tr =$("<tr id='" + nuevoDetalle.referencia + "'></tr>");
				$tr.append(crearBotonEliminarDetalle(nuevoDetalle.referencia));
				$tr.append(generarSelectCantidad(nuevoDetalle.referencia, nuevoDetalle.stock));
				$tr.append("<td>"+ nuevoDetalle.referencia + "</td>");
				$tr.append("<td>" + nuevoDetalle.nombre + "</td>");
				$tr.append("<td class='precio-detalle'><input id='precio-" + nuevoDetalle.referencia + "' type='text' value='" + nuevoDetalle.precio + "' readonly /></td>");
				$tr.append("<td class='precio-detalle'><input id='total-" + nuevoDetalle.referencia + "' value='"+ nuevoDetalle.precio + "' readonly /></td>");
				$detalleFactura.append($tr);

				listaDetalle.agregarDetalle(nuevoDetalle);
				console.log(listaDetalle);
				$modalBuscarProducto.modal('close');
				$formBuscarProducto[0].reset();
				ocultarInfoProducto();
			}
			else {
				$respuestaAgregarProducto.text("Este producto ya se agrego a la factura.").fadeIn();
			}
		}
		else {
			$respuestaAgregarProducto.text("No se ha seleccionado un producto para agregar.").fadeIn();
		}

		desactivarBotonAgregar();
	}


	$btnAgregarProducto.on('click', agregarProductoFactura);

	/***** FORMULARIO AGREGAR DETALLE FACTURA *****/
	
});