<?php
get_header();
if (function_exists('wc_get_page_permalink')) : ?>
<main id="main">
<section class="dy-hero"><h1>Ordinea, făcută frumos.</h1>
<p>Obiecte alese pentru casa, biroul și călătoriile tale.</p>
<a class="button" href="<?php echo esc_url(wc_get_page_permalink('shop')); ?>">Toate produsele</a></section>
<h2>Ordine, în fiecare colț.</h2>
<nav class="dy-collections" aria-label="Colecții">
<?php foreach (array('Home & Organization','Desk & Tech','Travel & Car','Beauty & Rituals','Gifts') as $name) {
    $term = get_term_by('name', $name, 'product_cat');
    if ($term) {
        $link = get_term_link($term);
        if (!is_wp_error($link)) {
            printf('<a href="%s">%s</a>', esc_url($link), esc_html($name));
        }
    }
} ?>
</nav><h2>Noutăți</h2>
<?php echo do_shortcode('[products limit="10" columns="3" orderby="date" order="DESC"]'); ?>
</main>
<?php endif;
get_footer();
