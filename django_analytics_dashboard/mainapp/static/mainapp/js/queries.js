document.addEventListener("DOMContentLoaded", function () {
    function attachAutocomplete(inputId, suggestionId, url) {
        const input = document.getElementById(inputId);
        const suggestions = document.getElementById(suggestionId);

        input.addEventListener("input", function () {
            const query = input.value.trim();
            if (query.length < 1) {
                suggestions.innerHTML = "";
                return;
            }

            fetch(`${url}?q=${[query]}`)
                .then(response => response.json())
                .then(data => {
                    suggestions.innerHTML = "";

                    data.results.forEach(item => {
                        const li = document.createElement("li");
                        li.textContent = item;
                        li.addEventListener("click", function () {
                            input.value = item;
                            suggestions.innerHTML = "";
                        });
                        suggestions.appendChild(li);
                    });
                });
        });

        // Скрытие списка при клике вне
        document.addEventListener("click", function (e) {
            if (!e.target.closest(`#${inputId}`) && !e.target.closest(`#${suggestionId}`)) {
                suggestions.innerHTML = "";
            }
        });
    }

    // Подключаем к каждому input
    attachAutocomplete("asset_search", "asset_suggestions", "/get-asset-list/");

    function buttonClick(url) {
        const input = document.getElementById("asset_search");
        const startdate = document.getElementById("start-date");
        const enddate = document.getElementById("end-date");
        const btn = document.getElementById("analytics_button");
        const avgprice = document.getElementById("average_price");
        const plotimg = document.getElementById("plot_image");
        const historytable = document.getElementById("history_table");

        btn.addEventListener("click", function (){
            const symbol = input.value.trim();
            if (!input) {
                avgprice.textContent = "Enter Asset!";
                return;
            }
            if (startdate>enddate) {
                avgprice.textContent = "End Date can't be earlier then Start Date!";
            }

            fetch(`${url}?q=${[input.value,startdate.value,enddate.value]}`)
            .then(response => response.json())
            .then(data => {
                avgprice.textContent = parseFloat(data.average);
                plotimg.setAttribute("src", data.plot_img)

                data.history.forEach(item => {
                        const row = document.createElement("tr");
                        const celldate = document.createElement("td");
                        const cellprice = document.createElement("td");
                        celldate.textContent = item.date;
                        cellprice.textContent = item.price;
                        row.appendChild(celldate)
                        row.appendChild(cellprice)
                        historytable.appendChild(row);
                    });
                })
                .catch(err => {
                 avgprice.textContent = "Request error";
                 console.error(err);
                 });
        });
    }

    buttonClick('/get-asset-stats/');
});