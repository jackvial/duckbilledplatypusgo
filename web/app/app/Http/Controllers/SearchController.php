<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Article;

class SearchController extends Controller
{
    public function search(Request $request)
    {
        $contexts = Article::all()->map(function($item) {
            return $item->body;
        });
        $response = Http::post('http://platypus_inference/predict', [
            'question' => $request->q,
            'contexts' => $contexts,
        ]);
        return response()->json([
            "results" => $response->json()['results']
        ]);
    }
}
