$(function () {

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-quiz").modal("show");
            },
            success: function (data) {
                $("#modal-quiz .modal-content").html(data.html_form);
            }
        });
    };


    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#quiz-table tbody").html(data.html_quiz_list);  // <-- Replace the table body
                    $("#modal-quiz").modal("hide");  // <-- Close the modal
                }
                else {
                    $("#modal-quiz .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };
    // Create quiz
    $(".js-create-quiz").click(loadForm);
    $("#modal-quiz").on("submit", ".js-quiz-create-form", saveForm);

    // Update quiz
    $("#quiz-table").on("click", ".js-update-quiz", loadForm);
    $("#modal-quiz").on("submit", ".js-quiz-update-form", saveForm);

    // Delete quiz
    $("#quiz-table").on("click", ".js-delete-quiz", loadForm);
    $("#modal-quiz").on("submit", ".js-quiz-delete-form", saveForm);
});