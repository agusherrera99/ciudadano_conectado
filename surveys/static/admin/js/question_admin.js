window.addEventListener('load', function() {
    function initToggle() {
        // Usar directamente django.jQuery que está garantizado en el admin
        var $ = django.jQuery;
        
        // Intentar diferentes selectores para encontrar el campo de tipo de pregunta
        var questionType = $('#id_question_type');
        var optionGroup = $('#options-group');

        // Estado inicial
        if (questionType.val() !== 'predefinida') {
            optionGroup.hide();
        }
        
        // Cuando cambia el valor
        questionType.on('change', function() {
            if (questionType.val() === 'predefinida') {
                optionGroup.show();
            }
            else {
                optionGroup.hide();
            }
        });
        return true;
    }
    
    initToggle()
});