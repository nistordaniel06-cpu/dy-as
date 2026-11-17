#!/usr/bin/env bash
# Run from a fresh staging WordPress installation with WP-CLI.
set -eu
kit_dir="$(cd "$(dirname "$0")" && pwd)"
wp plugin install woocommerce woocommerce-gateway-stripe --activate
wp theme install storefront
wp theme install "$kit_dir/dy-as-theme.zip" --activate
wp option update blogname DY-AS
wp option update woocommerce_currency EUR
wp option update woocommerce_enable_guest_checkout yes
wp option update woocommerce_enable_signup_and_login_from_checkout no
wp eval 'WC_Install::create_pages();'
wp option patch update woocommerce_stripe_settings testmode yes || wp eval '$s=(array)get_option("woocommerce_stripe_settings",array()); $s["testmode"]="yes"; update_option("woocommerce_stripe_settings",$s);'
