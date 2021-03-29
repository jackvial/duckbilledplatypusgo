<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class ArticlesAddFulltextIndex extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        // Use the ngram parser (default ngram = 1) https://dev.mysql.com/doc/refman/5.7/en/fulltext-search-ngram.html_entity_decode
        // This will help better match different word forms like venom and venomous.
        // e.g. "Is the platypus venomous?" Should now match to the word venom
        DB::statement('ALTER TABLE articles ADD FULLTEXT articles_fulltext(body) WITH PARSER ngram;');
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //
    }
}
