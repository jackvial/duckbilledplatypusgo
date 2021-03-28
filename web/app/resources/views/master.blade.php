<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title></title>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="{{ mix('css/app.css') }}" rel="stylesheet">
</head>

<body>
  <div class="flex flex-col items-center justify-center mt-16">
    <div class="flex flex-col items-center justify-center w-full sm:w-2/4 lg:w-1/3 p-4">
      <img src="platypus_logo.png" id="logo" />
      <h1 id="brand-name">DuckBilledPlatypusGo</h1>
      <form method="GET" class="mt-4 w-full">
        <div class="search-input-group">
          <input
            id="search-input"
            type="text"
            name="q"
            placeholder="Search..."
            autocomplete="off"
            class="search-input">
          <span class="search-input-addon">
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
      </form>
      <div id="results-list" class="text-left w-full mt-4"></div>
    </div>
  </div>
  <script src="/app.js"></script>
</body>

</html>