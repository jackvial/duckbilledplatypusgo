import React, { useState } from "react";

const ListItem = ({ item }) => {
    return (
        <div className="list-item">
            <b>Answer:</b> {item.answer}
            <br />
            <span className="text-sm text-gray-400">
                <b>Match: </b>
                {(item.score * 100).toFixed(1)}%
            </span>
        </div>
    );
};

const App = () => {
    const [searchResults, setSearchResults] = useState([]);
    const [query, setQuery] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    return (
        <>
            <img src="platypus_logo.png" id="logo" />
            <h1 id="brand-name">DuckBilledPlatypusGo</h1>
            <form method="GET" className="mt-2 w-full">
                <div className="search-input-group">
                    <input
                        id="search-input"
                        type="text"
                        name="q"
                        placeholder="Search..."
                        autoComplete="off"
                        className="search-input"
                        onKeyDown={(e) => setQuery(e.currentTarget.value)}
                        onChange={(e) => setQuery(e.currentTarget.value)}
                    />
                    <span className="search-input-addon bg-gray-700">
                        <button
                            id="search-button"
                            type="button"
                            className="p-1 focus:outline-none focus:shadow-outline"
                            onClick={(e) => {
                                if (!query) {
                                    return;
                                }
                                setIsLoading(true);
                                fetch(`/search?q=${query}`, {
                                    headers: {
                                        "Content-Type": "application/json",
                                    },
                                })
                                    .then((response) => response.json())
                                    .then((data) => {
                                        setSearchResults(data.results);
                                        setIsLoading(false);
                                    });
                            }}
                        >
                            {!isLoading ? (
                                <svg
                                    fill="none"
                                    stroke="currentColor"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    viewBox="0 0 24 24"
                                    className="w-6 h-6"
                                >
                                    <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                </svg>
                            ) : (
                                <svg
                                    className="animate-spin h-6 w-6"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                >
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    ></circle>
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    ></path>
                                </svg>
                            )}
                        </button>
                    </span>
                </div>
            </form>
            <div id="results-list" className="text-left w-full mt-4">
                {searchResults.map((item, index) => {
                    return <ListItem key={index} item={item} />;
                })}
            </div>
        </>
    );
};

export default App;
