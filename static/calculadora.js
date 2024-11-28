$(document).ready(function () {
    let expression = "";
    let memoryValue = null; 

    $(".buttons").append(`
        <button class="button memory" id="ms">MS</button>
        <button class="button memory" id="mr">MR</button>
    `);

    $("#negativo").click(function() {
        if (expression === "" || 
            ['+', '-', '*', '/', '('].includes(expression.slice(-1))) {
            expression += "-";
            $("#display").text(expression);
        }
    });
    
    function updateTokenValuesTable(tokenValues) {
        const tbody = $("#token-values-table tbody");
        tbody.empty();
        tokenValues.forEach(([token, value]) => {
            tbody.append(`
                <tr>
                    <td>${token}</td>
                    <td>${value}</td>
                </tr>
            `);
        });
    }

    function updateTokenFrequenciesTable(frequencies) {
        const tbody = $("#token-frequencies-table tbody");
        tbody.empty();
        Object.entries(frequencies).forEach(([token, frequency]) => {
            tbody.append(`
                <tr>
                    <td>${token}</td>
                    <td>${frequency}</td>
                </tr>
            `);
        });
    }

    $(".button").click(function () {
        const value = $(this).data("value");
        if (value === "C") {
            expression = "";
            $("#display").text("");
            $("#tree").attr("src", "");
            $("#token-values-table tbody").empty();
            $("#token-frequencies-table tbody").empty();
        } else if (value === "backspace") {
            expression = expression.slice(0, -1);
            $("#display").text(expression);
        } else if (value !== undefined) {
            expression += value;
            $("#display").text(expression);
        }
    });

    $("#ms").click(function() {
        if ($("#display").text() !== "") {
            $.ajax({
                url: "/calcular",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ expression }),
                success: function (response) {
                    if (response.valid) {
                        memoryValue = response.result;
                        alert(`Valor ${memoryValue} guardado en memoria`);
                    }
                },
                error: function () {
                    alert("Error al guardar valor en memoria");
                }
            });
        }
    });

    $("#mr").click(function() {
        if (memoryValue !== null) {
            expression += memoryValue.toString();
            $("#display").text(expression);
        } else {
            alert("No hay ningún valor en memoria");
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
                    updateTokenValuesTable(response.token_values);
                    updateTokenFrequenciesTable(response.token_frequencies);
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