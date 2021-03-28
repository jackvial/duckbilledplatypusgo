const SearchApp = () => {
    const searchInputElem = document.getElementById("search-input");
    const searchButtonElem = document.getElementById("search-button");
    const resultsListElem = document.getElementById("results-list");

    const ListItemComponent = (item) => {
        return `<div class="list-item">
                  <b>Answer:</b> ${item.answer} 
                  <br>
                  <span class="text-sm text-gray-400"><b>Match: </b>${(
                      item.score * 100
                  ).toFixed(1)}%</span>
              </div>`;
    };

    searchButtonElem.addEventListener("click", (e) => {
        e.preventDefault();
        fetch(`/search?q=${searchInputElem.value}`, {
            headers: { "Content-Type": "application/json" },
        })
            .then((response) => response.json())
            .then((data) => {
                resultsListElem.innerHTML = "";
                data.results.forEach((item) => {
                    resultsListElem.insertAdjacentHTML(
                        "beforeend",
                        ListItemComponent(item)
                    );
                });
            });
    });
};
SearchApp();
