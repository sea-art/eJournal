<template>
    <div id="app">
        <header-bar/>
        <router-view :key="$route.path" class="fit-height"/>
    </div>
</template>

<script>
import Header from '@/Header'

export default {
    components: {
        'header-bar': Header
    }
}
</script>

<style>
/* @import url('https://fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700'); */

:root {
    --theme-dark-blue: #252C39;
    --theme-peach: #E9A480;
    --theme-dark-peach: #dE8F3F;
    --theme-light-grey: #EEEEEE;
    --theme-dark-grey: #BBBBBB;
    --theme-pink: #E64769;
    --theme-blue: #22648A;
    --theme-red: #c83b4b;
    --theme-medium-grey: #DEDEDE;
    --theme-positive-unselected: #99ff99;
    --theme-positive-selected: #1aff1a;
    --theme-negative-unselected: #99ff99;
    --theme-negative-selected: #1aff1a;
    --theme-change-unselected: #99ff99;
    --theme-change-selected: #1aff1a;
}

* {
    border-radius: 0px !important;
    text-decoration: none !important;
    color: var(--theme-dark-blue);
    text-align: left;
}

img {
    max-width: 100%;
    max-height: 100%;
}

h1 {
    font-weight: bold;
    font-size: 60px;
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
}

h2 {
    font-weight: bold;
    font-size: 35px;
}

h3 {
    font-weight: bold;
    font-size: 35px;
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
}

h4 {
    font-weight: bold;
    font-size: 30px;
    color: var(--theme-blue);
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
    margin-bottom: 0px;
}

h5 {
    font-size: 30px;
    margin-bottom: 0px;
}

h6 {
    font-size: 20px;
    color: var(--theme-blue);
    margin-bottom: 0px;
}

h4 a {
    color: var(--theme-blue) !important;
}

#app {
    overflow-x: hidden;
    font-family: 'Roboto', sans-serif;
    font-size: 20px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    flex-flow: column;
    height: 100%;
    padding-top: 70px;
}

.btn, .form-control, input {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 20px;
    background-color: white !important;
    color: var(--theme-dark-blue) !important;
    border: none;
    margin-bottom: 10px;
}

.fit-height {
    flex: 1 1 auto;
    display: flex;
}

.form-control, input {
    border-left: 15px solid var(--theme-dark-grey) !important;
}

input, select {
    padding: 0.375rem 0.75rem !important;
}

.btn {
    border-left: 15px solid var(--theme-blue) !important;
}

.btn:hover {
    background-color: var(--theme-dark-grey) !important;
    border-left: 15px solid var(--theme-blue) !important;
    color: white;
}

.card {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
}

.card-body {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
}

.hover {
    cursor: pointer;
}

.card-last-elem-button .card-body {
    padding-bottom: 2px !important;
}

.no-hover:hover {
    background-color: var(--theme-light-grey) !important;
}

.multi-form {
    margin-bottom: 10px !important;
}

.card:hover {
    background-color: var(--theme-dark-grey);
}

.card.pink-border {
    border-left-color: var(--theme-pink);
}

.card.peach-border {
    border-left-color: var(--theme-peach);
}

.card.blue-border {
    border-left-color: var(--theme-blue);
}

.showEnters {
    white-space: pre-wrap;
}

.portrait-container {
    height: 100px;
    width: 100px;
}

.portrait-container-sm {
    height: 50px;
    width: 50px;
}

.add-icon {
    fill: var(--theme-light-grey) !important;
    cursor: pointer;
}

.add-icon:hover {
    fill: var(--theme-positive-selected) !important;
}

.trash-icon:hover {
    fill: var(--theme-negative-selected) !important;
}

.trash-icon {
    fill: var(--theme-dark-grey) !important;
    cursor: pointer;
}

.add-button {
    background-color: var(--theme-positive-unselected) !important;
}

.add-button:hover {
    background-color: var(--theme-positive-selected) !important;
}

.delete-button {
    background-color: var(--theme-negative-unselected) !important;
}

.delete-button:hover {
    background-color: var(--theme-negative-selected) !important;
}

.lti-button-option {
    width: 275px;
    height: 100px;
    margin-top: 20px;
}

.lti-button-text {
    font-size: 20px;
    text-align: center;
}

.lti-intro-text {
    margin-left: 15px;
    margin-right: 15px;
}

.portrait {
    max-width: 175px;
}

.full-width {
    width: 100%;
}

.no-hover:hover {
    background-color: var(--theme-light-grey);
}

.settings-card {
    margin-top: 12px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
    border-left-color: var(--theme-blue);
}
</style>
