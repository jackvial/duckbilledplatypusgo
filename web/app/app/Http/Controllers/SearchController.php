<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Article;
use DB;

class SearchController extends Controller
{
    public function search(Request $request)
    {
        $contexts = collect(DB::select(DB::raw("SELECT * from articles WHERE MATCH(body) AGAINST (?) LIMIT ?;"), [
            $request->q,
            env('SEARCH_LIMIT', 10),
        ]))->map(function($item) {
            return $item->body;
        })->take(env('TAKE_N_RESULTS', 5));
        $response = Http::post(env('QA_INFERENCE_HOST') . '/predict', [
            'question' => $request->q,
            'contexts' => $contexts,
        ]);
        return response()->json([
            "results" => $response->json()['results']
        ]);
    }
}
