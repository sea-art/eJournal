<template>
    <div class="bread-crumb-container">
        <b-row>
            <b-col cols="12" md="12">
                <h4>
                    <span v-for="crumb in crumbsUpper" :key="crumb.key">
                        <b-link tag="b-button" :to="crumb.route">{{ crumb.string }}</b-link> /
                    </span>
                </h4>
                <h1 id="h1-current-page-breadcrumb">
                    {{ idea }}
                    <slot>
                        <icon name="eye" @click.native="eyeClick()" class="eye-icon" scale="1.75"></icon>
                        <b-button v-if="canEdit()" @click="editClick()" class="float-right edit-button"> Edit</b-button>
                    </slot>
                </h1>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import store from '@/Store.vue'

export default {
    components: {
        icon
    },
    computed: {
        assocParam (name, params) {

        },
        idea () {
            // grab route matched object
            var routeMatched = this.$route.matched[0].path
            var params = this.$route.params

            // grab router
            var routerRoutes = this.$router.options.routes

            var crumbs = []
            // fill list using routes list matches with route match
            for (var route of routerRoutes) {
                if (routeMatched.startsWith(route.path)) {
                    // add to list
                    crumbs.push({ name: route.name, param: assocParam(route.name, params), display: "" })
                }
            }
            crumbs.sort((a, b) => { b.name.length - a.name.length })

            // get parammed page names

            // use current page params + names for linking

            // create display mapping from hardcode + anonymous functions, using name as key
            var map = []
            // map.push({ name:  })

            // cache internally using router objects
            return crumbs
        },
        // Internal list of crumbs (object representations of individual parts of the breadcrumb)
        internalList () {
            var splittedPath = this.$route.path.split('/').slice(1)
            var segmentedPath = []
            var idedElements = ['Course', 'Assignment', 'Journal']

            // Merge page/id parts into segments
            for (var i = 0; i < splittedPath.length; i++) {
                if (idedElements.includes(splittedPath[i])) {
                    segmentedPath.push(splittedPath[i] + '/' + splittedPath[++i])
                } else {
                    segmentedPath.push(splittedPath[i])
                }
            }

            var cachedList = store.state.breadCrumb
            var tempList = []

            // Rebuild path equal to cached as long as possible
            for (var j = 0; j < segmentedPath.length; j++) {
                if (!cachedList[j] || segmentedPath[j] !== cachedList[j].segment) {
                    break
                }
                tempList.push(cachedList[j])
            }

            // Fetch rest of path
            for (; j < segmentedPath.length; j++) {
                var crumb = { segment: segmentedPath[j] }
                this.fetchDBName(crumb)
                tempList.push(crumb)
            }

            store.setBreadcrumb(tempList)
            return tempList
        },
        // Data for 'trail' part of breadcrumb
        crumbsUpper () {
            var crumbs = []
            for (var crumb of this.internalList.slice(0, -1)) {
                crumbs.push({
                    route: {
                        name: crumb.segment.split('/')[0],
                        params: this.$route.params
                    },
                    string: crumb.string,
                    key: crumb.segment
                })
            }
            return crumbs
        },
        // Current page name
        crumbsLower () {
            return this.internalList.slice(-1)[0].string
        }
    },
    methods: {
        eyeClick () {
            this.$emit('eye-click')
        },
        editClick () {
            this.$emit('edit-click')
        },
        fetchDBName (crumb) {
            // --TODO: add api link
            crumb.string = crumb.segment.split('/')[0]
        },
        splitPath () {
            this.$router.currentRoute.path.split('/').slice(1, -1)
        },
        canEdit () {
            var pageName = this.$route.name

            if ((pageName === 'Home' && this.$root.isAdmin()) ||
               (pageName === 'Course' && this.$root.canEditCourse()) ||
               (pageName === 'Assignment' && this.$root.canEditCourse())) {
                return true
            }
        }
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
    fill: var(--theme-pink) !important;
}
</style>
