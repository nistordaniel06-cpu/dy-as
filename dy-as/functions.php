<?php
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('dy-as', get_stylesheet_uri(), array('storefront-style'), '0.1.0');
});
