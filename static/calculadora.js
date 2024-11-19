$(document).ready(function () {
    let expression = "";

    $(".button").click(function () {
        const value = $(this).data("value");
        if (value === "C") {
            expression = "";
            $("#display").text("");
            $("#tree").attr("src", "");
        } else if (value !== undefined) {
            expression += value;
            $("#display").text(expression);
        }
    });

    $("#calcular").click(function () {
        $.ajax({
            url: "/calcular",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ expression }),
            success: function (response) {
                if (response.valid) {
                    expression = response.result.toString();
                    $("#display").text(expression);
                    const treeImageUrl = "/static/" + response.tree;
                    $("#tree").attr("src", treeImageUrl);
                } else {
                    $("#display").text("Error");
                    $("#tree").attr("src", "");
                }
            },
            error: function () {
                $("#display").text("Error");
            }
        });
    });
});
