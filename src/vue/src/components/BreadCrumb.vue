<!--
    Breadcrumb vue component
    Uses the current router to create breadcrumb
    Caches named page names in store
    Aliases and page extensions can be defined in data
-->

<template>
    <div class="bread-crumb-container">
        <b-row>
            <b-col cols="12" md="12">
                <h4>
                    <!-- Assumes on a page above guest page (guest page matches every page first) -->
                    <span v-for="breadcrumb in breadedCrumbs.slice(1, -1)" :key="breadcrumb.name">
                        <b-link tag="b-button" :to="breadcrumb.route">{{ breadcrumb.display }}</b-link> /
                    </span>
                </h4>
                <h1 id="h1-current-page-breadcrumb">
                    {{ breadedCrumbs.slice(-1)[0].display }}
                    <slot>
                        <icon name="eye" @click.native="eyeClick()" class="eye-icon" scale="1.75"></icon>
                        <b-button v-if="canEdit()" @click="editClick()" class="float-right change-button"> Edit</b-button>
                    </slot>
                </h1>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import icon from 'vue-awesome/components/Icon'
import store from '@/Store.vue'

export default {
    components: {
        icon
    },
    /*
        cachedMap: list of crumb objects of named pages, with displayname, synced with the store
        aliases: aliases for non named pages
        paramMap: translation table for router params and names
        crumbs: list of crumb objects in the path, without displayname
        (computed) breadedCrumbs: data used to display the breadcrumb on the page
    */
    data () {
        return {
            cachedMap: [],
            aliases: {
                'Home': 'Courses',
                'FormatEdit': 'Format Editor',
                'CourseEdit': 'Course Editor',
                'AssignmentEdit': 'Assignment Editor',
                'AssignmentsOverview': 'Assignment Overview',
                'UserRoleConfiguration': 'User Role Configuration'
            },
            paramMap: {
                'Course': 'cID',
                'cID': 'Course',
                'Assignment': 'aID',
                'aID': 'Assignment',
                'Journal': 'jID',
                'jID': 'Journal'
            },
            crumbs: []
        }
    },
    methods: {
        // finds segments of the current path
        findCrumbs () {
            // grab route matched object
            var routeMatched = this.$route.matched[0].path
            var params = this.$route.params

            // grab router
            var routerRoutes = this.$router.options.routes
            routerRoutes.sort((a, b) => a.path.length - b.path.length)

            // match routes that prepend the current path, push partial crumbs
            for (var route of routerRoutes) {
                if (routeMatched.startsWith(route.path)) {
                    this.crumbs.push({ name: route.name, param: params[this.paramMap[route.name]], paramName: this.paramMap[route.name] })
                }
            }
        },
        // fills currently missing parts in the cache
        fillCache () {
            // get cached map
            this.cachedMap = store.state.cachedMap.slice()

            // fill missing parts of the request
            var request = {}
            for (var crumb of this.crumbs) {
                if (!(typeof crumb.param === 'undefined')) {
                    if (this.cachedMap.filter(map => map.name === crumb.name && map.param === crumb.param).length === 0) {
                        request[crumb.paramName] = crumb.param
                    }
                }
            }
            // fill the displaymap cache
            if (!(Object.keys(request).length === 0 && request.constructor === Object)) {
                commonAPI.get_names(request).then(data => {
                    var localMap = {
                        'cID': 'course',
                        'aID': 'assignment',
                        'jID': 'journal'
                    }
                    for (var entry of Object.entries(request)) {
                        this.cachedMap.push({ name: this.paramMap[entry[0]], param: entry[1], paramName: entry[0], display: data[localMap[entry[0]]] })
                    }
                }).then(_ => {
                    // set the cached map
                    store.setCachedMap(this.cachedMap)
                })
            }
        },
        eyeClick () {
            this.$emit('eye-click')
        },
        editClick () {
            this.$emit('edit-click')
        },
        canEdit () {
            var pageName = this.$route.name

            if ((pageName === 'Home' && this.$root.isAdmin()) ||
               (pageName === 'Course' && this.$root.canEditCourse()) ||
               (pageName === 'Assignment' && this.$root.canEditCourse())) {
                return true
            }
        }
    },
    computed: {
        // display-ready version of the crumb list, created from the crumb list combined with the cached displaymap
        breadedCrumbs () {
            var breadedCrumbs = []
            for (var crumb of this.crumbs) {
                // set the displayname per breadcrumb
                var display
                if (typeof crumb.param === 'undefined') {
                    // use alias if regular page and applicable
                    if (this.aliases[crumb.name]) {
                        display = this.aliases[crumb.name]
                    } else {
                        display = crumb.name
                    }
                } else {
                    // get the display from cache, cachedmap is watched here so this happens before and after async
                    display = this.cachedMap.filter(map => map.name === crumb.name && map.param === crumb.param)[0]
                    if (typeof display === 'undefined') {
                        display = ''
                    } else {
                        display = display.display
                    }
                }
                breadedCrumbs.push({
                    display: display,
                    route: {
                        name: crumb.name,
                        params: this.$route.params
                    }
                })
            }
            return breadedCrumbs
        }
    },
    created () {
        // find current path segments
        this.findCrumbs()

        // request missing parts
        this.fillCache()
    }
}
</script>

<style>
#h1-current-page-breadcrumb {
    margin-bottom: 0px !important;
}

/* Most paddings/margins relate to full responive build, please take care.*/
.bread-crumb {
    padding: 0px;
    background-color: var(--theme-medium-grey);
    margin-bottom: 0px;
}

.bread-crumb-container {
    padding-right: 10px;
    padding-bottom: 12px;
    margin-bottom: -4px;
}

@media(max-width:992px) {
    .bread-crumb-container  {
        padding-top: 12px !important;
        margin-top: -4px !important;
    }
}

.eye-icon {
    fill: var(--theme-light-grey) !important;
    cursor: pointer;
}

.eye-icon:hover {
    fill: var(--theme-change-selected) !important;
}
</style>
