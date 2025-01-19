document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("conversion-form");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const sourceCurrency = form.source_currency.value;
        const targetCurrency = form.target_currency.value;
        const amount = parseFloat(form.amount.value);

        fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'source_currency': sourceCurrency,
                'target_currency': targetCurrency,
                'amount': amount
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при конверсии');
            }
            return response.json();
        })
        .then(data => {

            document.getElementById("result").innerHTML =
                `Результат: ${data.result} ${data.target_currency} (Курс: ${data.rate})`;
        })
        .catch(error => console.error('Ошибка:', error));
    });
});
