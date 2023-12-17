<?php

namespace App\Http\Controllers;

class MainController extends Controller
{
    function index()
    {
        return view("index", ['flag' => $_ENV["FLAG"]]);
    }
}
