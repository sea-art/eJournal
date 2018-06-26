<template>
    <div id="app">
        <header-bar/>
        <router-view class="fit-height"/>
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
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700');

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
    --theme-add-unselected: #99ff99;
    --theme-add-selected: #1aff1a;
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
    white-space: pre;
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

.trash-icon:hover {
    fill: var(--theme-red);
}

.trash-icon {
    fill: var(--theme-red);
    cursor: pointer;
}

.add-icon:hover {
    fill: var(--theme-add-selected) !important;
}

.add-button {
    border-color: var(--theme-blue) !important;
    background-color: var(--theme-add-unselected) !important;
}

.add-button:hover {
    border-color: var(--theme-blue) !important;
    background-color: var(--theme-add-selected) !important;
    color: black !important;
}

.delete-button {
    border-color: var(--theme-blue) !important;
    background-color: var(--theme-pink) !important;
}

.delete-button:hover {
    border-color: var(--theme-dark-blue) !important;
    background-color: red !important;
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
