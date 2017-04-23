
$(document).ready(function() {

    $form = $('form#activar-cuentas-form');
    $botonGuardar = $('#boton-guardar');
    $switches = $('.input-switch');

    $form.on('submit', function(event) {
        $botonGuardar.prop('disabled', true);
    });

    $switches.each(function(index) {
    	$(this).on('click', function(event) {
    		if (this.checked) {
    			if ($botonGuardar.hasClass('disabled')) {
    				$botonGuardar.removeClass('disabled');
    			}
    		}
    		else {
    			var deshabilitar = true;
    			
    			$switches.each(function(index) {
    				if (this.checked) {
    					deshabilitar = false;
    					return false;
    				}
    			});

    			if (deshabilitar) {
	    			if (!$botonGuardar.hasClass('disabled')) {
	    				$botonGuardar.addClass('disabled');
	    			}	
    			}
    		}
    	});
    });
});