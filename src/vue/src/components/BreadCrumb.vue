<template>
    <div class="bread-crumb-container">
        <b-row>
            <b-col cols="12" md="12">
                <h4>
                    <span  v-for="crumb in crumbsUpper">
                        <b-link tag="b-button" :to="crumb.route">{{ crumb.string }}</b-link> /
                    </span>
                </h4>
                <h1 id="h1-current-page-breadcrumb">
                    {{ crumbsLower }}
                    <slot>
                        <icon name="eye" @click.native="eyeClick()" class="eye-icon" scale="1.75"></icon>
                        <b-button v-if="this.$route.params.cID != undefined" class="float-right edit-button" :to="{name: 'CourseEdit', params: {cID: this.$route.params.cID, courseName: this.$route.params.courseName}}"> Edit </b-button>
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
                crumbs.push({ route: { name: crumb.segment.split('/')[0],
                                       params: this.$route.params },
                              string: crumb.string })
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
