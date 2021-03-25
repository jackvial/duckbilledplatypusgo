<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Search extends Component
{
    public $search;

    protected $queryString = ['search'];
    
    public function render()
    {
        return view('livewire.search', [
            'results' => ['one', 'two', 'three']
        ]);
    }
}
