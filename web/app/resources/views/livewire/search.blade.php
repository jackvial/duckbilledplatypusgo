<h1 id="brand-name">DuckBilledPlatypusGo</h1>
<form method="GET" class="mt-4 w-full">
    <div class="relative text-gray-200 focus-within:text-gray-400">
        <input
            id="search-input"
            type="text"
            name="q"
            placeholder="Search..."
            autocomplete="off"
            class="w-full py-2 text-sm text-white bg-gray-600 rounded-md pl-10 focus:outline-none focus:bg-white focus:text-gray-900">
        <span class="absolute inset-y-0 right-0 flex items-center pl-2">
            <button
                id="search-button"
                type="button"
                class="p-1 focus:outline-none focus:shadow-outline">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                    stroke-width="2" viewBox="0 0 24 24" class="w-6 h-6">
                    <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
            </button>
        </span>
    </div>
    <input wire:model="search" type="search" placeholder="Search posts by title...">

    <h1>Search Results:</h1>

    <ul>
        @foreach($results as $res)
        <li>{{ $res }}</li>
        @endforeach
    </ul>
</form>
<div id="results-list" class="text-left w-full mt-4"></div>