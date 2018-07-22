# CSS Structure

Taken from: http://thesassway.com/beginner/how-to-structure-a-sass-project

As we require more structure when it comes to our CSS, I figured this would be a good place to start. The format is inspired by: https://smacss.com
An incredibly modular approach to scaling css structure.

**The goal is to adapt this to our need, take it as starting point.**

## Modules
The modules directory is reserved for Sass code that doesn't cause Sass to actually output CSS. Things like mixin declarations, functions, and variables.

## Partials
The partials directory is where the meat of the CSS is constructed. Finegrained ala SMACCS style. (typography, buttons, textboxes, selectboxes, etc…).

## Vendor
The vendor directory is for third-party CSS. This is handy when using prepackaged components developed by other people (or for your own components that are maintained in another project). jQuery UI and a color picker are examples of CSS that you might want to place in the vendor directory. As a general rule I make it a point not to modify files in the vendor directory. If I need to make modifications I add those after the vendored files are included in the primary stylesheet. This should make it easy for me to update the third-party stylesheets to more current versions in the future.
