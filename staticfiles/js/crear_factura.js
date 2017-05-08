
$(document).ready(function() {

	function closeIt()
	{ return "";}

	//window.onbeforeunload = closeIt;

	function ListaDetalle() {
		this.lista = new Array();

		this.listaVacia = function() {
			return (this.lista.length == 0);
		}

		this.agregarDetalle = function(detalle) {
			this.lista.push(detalle);
		}

		this.eliminarDetalle = function(referencia) {
			if (this.lista.length > 0) {
				var indiceEliminar = -1;

				for (var i = 0; i < this.lista.length; i++) {

					if (this.lista[i].referencia == referencia) {
						indiceEliminar = i;
						break;
					}
				}

				if (indiceEliminar >= 0) {
					this.lista.splice(indiceEliminar, 1);
				}
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
	$triggerBuscarCliente = $('a#trigger-buscar-cliente');

	/****** Elementos que componen la ventana modal agregar cliente. ******/
	$modalAgregarCliente = $('div#modal-agregar-cliente');
	$formAgregarCliente = $('form#form-agregar-cliente');
	$btnAgregarCliente = $('button#btn-agregar-cliente');
	$preloaderAgregarCliente = $('div#preloader-agregar-cliente');
	//Indica si el cliente ya se agrego a la factura.
	clienteAgregado = false;
	//Input para guardar el id del cliente.
	$inputCliente = $('input#cliente');

	/***** Elementos donde se visualizan los datos del cliente en la factura. *****/
	$infoCliente = {
		'cedula': $('span#cedula-cliente'),
		'nombre': $('span#nombre-cliente'),
		'direccion': $('span#direccion-cliente'),
		'ciudad': $('span#ciudad-cliente'),
		'telefono': $('span#telefono-cliente')	
	}

	/********** VARIABLES DEL COMPONENTE BUSCAR Y AGREGAR PRODUCTO **********/

	/* Elementos que componen la ventana modal buscar producto. */
	$modalBuscarProducto = $('div#modal-buscar-producto');
	$formBuscarProducto = $('form#form-buscar-producto');
	$btnBuscarProducto = $('button#btn-buscar-producto');
	$respuestaBuscarProducto = $('div#respuesta-busqueda-producto');
	$preloaderBuscarProducto = $('div#preloader-buscar-producto');
	$triggerBuscarProducto = $('a#trigger-buscar-producto');

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

	listaDetalle = new ListaDetalle();
	objetoBusquedaProducto = null;
	
	/* Elementos del componente guardar factura. */
	$formGuardarFactura = $('form#form-guardar-factura');
	//Botón para guardar la factura.
	$btnGuardarFactura = $('button#btn-guardar-factura');
	//Detalle de la factura.
	$detalleFactura = $('#body-factura');
	//Contendor para mostrar los mensajes en caso de error.
	$respuestaGuardarFactura = $('div#respuesta-guardar-factura');
	//Preloader guardar factura.
	$preloaderGuardarFactura = $('div#preloader-guardar-factura');

	subtotalFactura = ivaFactura = totalFactura = 0; 
	
	$totalFactura = {
		"subtotal": $('input#subtotal-factura'),
		"iva": $('input#iva-factura'),
		"total": $('input#total-factura')
	}


	/********** DEFINICIÓN DE FUNCIONES **********/

	/* 
	Muestra la información de los clientes y los productos.
	contenedores: Son los elementos donde se muestran los mensajes.
	valores: Es la información. 
	*/
	function mostrarInfo(contenedores, valores, id) {
		for (campo in valores) {
			try {
				if (campo == 'precio') {
					contenedores[campo].text(convertirPesos(String(valores[campo]))).fadeIn();
				}
				else {
					contenedores[campo].text(valores[campo]).fadeIn();
				}	
			} catch(err) {}
		}
	}

	function activarBotonGuardarFactura() {
		if (clienteAgregado && !listaDetalle.listaVacia()) {
			$btnGuardarFactura.removeClass('disabled');
		}
		else {
			$btnGuardarFactura.addClass('disabled');
		}

		if (clienteAgregado) {
			$triggerBuscarCliente.removeClass('pulse red').addClass('blue');
		}
		else {
			$triggerBuscarCliente.removeClass('blue').addClass('pulse red');	
		}

		if (!listaDetalle.listaVacia()) {
			$triggerBuscarProducto.removeClass('pulse red').addClass('blue');
			
		}
		else {
			$triggerBuscarProducto.removeClass('blue').addClass('pulse red');
		}
	}

	function actualizarTotalFactura(operacion, subtotal, iva, total) {

		var valido = (subtotal > 0) && (iva > 0) && (total > 0);

		if (valido) {
			if (operacion === 'sumar') {
				subtotalFactura += subtotal;
				ivaFactura += iva;
				totalFactura += total;
			}
			else if (operacion === 'restar') {
				if (subtotalFactura > 0 && ivaFactura > 0 && totalFactura > 0) {
					subtotalFactura -= subtotal;
					ivaFactura -= iva;
					totalFactura -= total;
				}
			}
		}

		$totalFactura.subtotal.val(subtotalFactura);
		$totalFactura.iva.val(ivaFactura);
		$totalFactura.total.val(totalFactura);
	}

	/* Esta función obtiene y retorna una lista con los ID'S y las cantidades 
	de cada producto que hay en el detalle de la factura. */
	function obtenerInfoDetalle() {
		var $detalles = $('td.cantidad-productos');
		var listaProductos = Array();

		$detalles.each(function(i) {
			var producto = this.childNodes[0].value;
			var cantidad = this.childNodes[1].value;

			listaProductos.push({"producto": producto, "cantidad": cantidad});
		});

		return listaProductos;
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

   
	function convertirPesos(cadena) {
		var cadenaPuntuacion = "";
		var cadenaConvertida = "$";
		var cont = 1;
		var j = cadena.length - 1;

		for (j; j >= 0; j--) {
			cadenaPuntuacion += cadena.charAt(j);
			if (cont % 3 == 0 && (j != cadena.length - 1) && (j != 0)) {
				cadenaPuntuacion += ".";
			}
			cont++;
		}

		var i = cadenaPuntuacion.length - 1;

		for (i; i >= 0; i--) {
			cadenaConvertida += cadenaPuntuacion.charAt(i);
		}

		return cadenaConvertida;
	}

	function asignarIDCliente(id) {
		$inputCliente.val(id);
		clienteAgregado = true;
		activarBotonGuardarFactura();
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
		var dato = {
			"cedula": this['cedula'].value
		};

		/*Procesa la respuesta del servidor.*/
		function procesarRespuestaBuscarCliente(data) {
			if (data.response == "success") {
					mostrarInfo($infoCliente, data);
					asignarIDCliente(data.id);
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
		var datos = {
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
				mostrarInfo($infoCliente, data);
				asignarIDCliente(data.id);
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
		var dato = {'referencia': this['referencia'].value}

		/*
		Esta función procesa la respuesta del servidor.
		*/
		function procesarRespuestaBuscarProducto(data) {
			if (data.response === 'success') {
				
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
		var $select = $("<select id='select-" + referencia + "' name='cantidad-" + referencia + "' class='browser-default'></select>");
		$select.append("<option value='1' selected>1</option>");

		if (stock > 1) {
			for (var i = 2; i <= stock; i++) {

				$select.append("<option value='" + i + "'>" + i + "</option>");
			}
		}

		$select.on('blur', function(event) {
			var $precio = $('input#precio-' + referencia);
			var $subtotal = $('input#subtotal-' + referencia);
			var $iva = $('input#iva-' + referencia);
			var $total = $('input#total-' + referencia);

			var subtotalAnt = Number($subtotal.val());
			var ivaAnt = Number($iva.val());
			var totalAnt = Number($total.val());

			actualizarTotalFactura('restar', subtotalAnt, ivaAnt, totalAnt);

			var cantidad = Number(this.value);
			var precio = Number($precio.val());
			var subtotal = cantidad * precio;
			var iva = Math.round(subtotal * 0.19);
			var total = subtotal + iva;

			actualizarTotalFactura('sumar', subtotal, iva, total);

			$subtotal.val(subtotal);
			$iva.val(iva);
			$total.val(total);

			//actualizarTotalFactura();
		});

		return $select;
	}

	function eliminarDetalle(event) {
		var referencia = this.dataset.referencia;

		var subtotal = $('input#subtotal-' + referencia).val();
		var iva = $('input#iva-' + referencia).val();
		var total = $('input#total-' + referencia).val();

		actualizarTotalFactura('restar', subtotal, iva, total);

		var $tr = $('tr#' + referencia).remove();

		listaDetalle.eliminarDetalle(referencia);
		activarBotonGuardarFactura();
	}

	function crearBotonEliminarDetalle(referencia) {
		var $botonEliminar = $("<a class='btn btn-floating red darken-1' title='Eliminar producto de la factura' data-referencia='" + referencia + "'><i class='material-icons'>delete</i></a>");
		$botonEliminar.on('click', eliminarDetalle);

		return $('<td class="precio-detalle"></td>').append($botonEliminar);
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
				nuevoDetalle = clonarObjeto(objetoBusquedaProducto);
				objetoBusquedaProducto = null;

				var referencia = nuevoDetalle.referencia;
				var precio = Number(nuevoDetalle.precio);
				var $selectCantidad = generarSelectCantidad(referencia, nuevoDetalle.stock);
				var cantidad = Number($selectCantidad.val());
				var subtotal = precio * cantidad;
				var iva = Math.round(subtotal * 0.19);
				var total = subtotal + iva;
				var $tr =$("<tr id='" + referencia + "' class='detalle-factura'></tr>");
				var $tdCantidad = $("<td class='cantidad-productos'><input type='hidden' name='producto-" + referencia + "' value='" + nuevoDetalle.id + "' / ></td>"); 
				
				$tdCantidad.append($selectCantidad);
				$tr.append(crearBotonEliminarDetalle(referencia));
				$tr.append("<td>"+ referencia + "</td>");
				$tr.append("<td>" + nuevoDetalle.nombre + "</td>");
				$tr.append($tdCantidad);
				$tr.append("<td class='precio-detalle'><input id='precio-" + referencia + "' type='text' value='" + precio + "' readonly /></td>");
				$tr.append("<td class='precio-detalle'><input id='subtotal-" + referencia + "' type='text' value='" + subtotal + "' readonly /></td>")
				$tr.append("<td class='precio-detalle'><input id='iva-" + referencia + "' value='" + iva + "' readonly /></td>");
				$tr.append("<td class='precio-detalle'><input id='total-" + referencia + "' value='"+ total + "' readonly /></td>");
				$detalleFactura.append($tr);

				actualizarTotalFactura('sumar', subtotal, iva, total);

				listaDetalle.agregarDetalle(nuevoDetalle);
				
				$modalBuscarProducto.modal('close');
				$formBuscarProducto[0].reset();
				ocultarInfoProducto();
				activarBotonGuardarFactura();
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

	/***** FORMULARIO GUARDAR FACTURA *****/
	$formGuardarFactura.on('submit', function(event) {
		//Se evita que la página recargue.
		event.preventDefault();
		//Se activa el preloader.
		$preloaderGuardarFactura.fadeIn();
		//Se desactiva el botón que envía el formulario para evitar multiples peticiones.
		$btnGuardarFactura.addClass('disabled');
		$respuestaGuardarFactura.fadeOut();

		//Se generan los datos que van a ser enviados al servidor.
		var datos = {
			"cliente": $inputCliente.val(),
			"detalle": obtenerInfoDetalle()
		}

		function procesarRespuestaGuardarFactura(data) {
			if (data.response === 'success') {
				location.replace(data.url);
			}
			else if (data.response === 'error') {
				$respuestaGuardarFactura.html(data.mensaje).fadeIn();
			}

			$preloaderGuardarFactura.fadeOut();
			$btnGuardarFactura.removeClass('disabled');
		}

		enviarPeticionAJAX(datos, "", this['csrfmiddlewaretoken'].value, procesarRespuestaGuardarFactura);

	});
	
});