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

            fetch(`${url}?q=${query}`)
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
    attachAutocomplete("crypto_symbol_search", "crypto_symbol_suggestions", "/get-crypto-list/");
    attachAutocomplete("stock_symbol_search", "stock_symbol_suggestions", "/get-stock-list/");
    attachAutocomplete("fccy_symbol_search", "fccy_symbol_suggestions", "/get-ccy-list/");
    attachAutocomplete("sccy_symbol_search", "sccy_symbol_suggestions", "/get-ccy-list/");

    function buttonClick(inputID,buttonID, pricefieldId, url, secondinputID = "None") {
        const input = document.getElementById(inputID);
        const btn = document.getElementById(buttonID);
        const pfld = document.getElementById(pricefieldId);

        if (secondinputID != "None"){
            const secondinput = document.getElementById(secondinputID);

            btn.addEventListener("click", function (){
                const symbol = input.value.trim();
                const symbol2 = secondinput.value.trim();
                if (!symbol || !symbol2) {
                    pfld.textContent = "Enter Symbol!";
                    return;
                }

                fetch(`${url}?q=${symbol}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === "ok") {
                        pfld.textContent = data.results;
                    } else {
                        pfld.textContent = parseFloat(data.results);
                    }
                })
                .catch(err => {
                    pfld.textContent = "Request error";
                    console.error(err);
                });
            });
        } else{
            btn.addEventListener("click", function (){
                const symbol = input.value.trim();
                if (!symbol) {
                    pfld.textContent = "Enter Symbol!";
                    return;
                }

                fetch(`${url}?q=${symbol}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === "ok") {
                        pfld.textContent = data.results;
                    } else {
                        pfld.textContent = parseFloat(data.results);
                    }
                })
                .catch(err => {
                    pfld.textContent = "Request error";
                    console.error(err);
                });
            });
        }



    }

    buttonClick('crypto_symbol_search', 'crypto_submit_button', 'price_crypto_date', '/get-crypto-price/');
    buttonClick('stock_symbol_search', 'stock_submit_button', 'price_stock_date', '/get-stock-price/');
    buttonClick('fccy_symbol_search', 'ccy_submit_button', 'price_ccy_date', '/get-crypto-price/', "sccy_symbol_search");
});