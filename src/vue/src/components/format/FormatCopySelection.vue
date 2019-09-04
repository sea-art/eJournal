<template>
    <div>
        <b-card
            :class="$root.getBorderClass($route.params.cID)"
            class="no-hover overflow-x-hidden"
        >
            <div
                v-for="copyable in copyableFormats"
                :key="`copyable-${copyable.course.id}`"
            >
                <main-card
                    :key="`course-${copyable.course.id}-copy`"
                    :line1="copyable.course.name"
                    :line2="copyable.course.startdate ? (copyable.course.startdate.substring(0, 4) +
                        (copyable.course.enddate ? ` - ${copyable.course.enddate.substring(0, 4)}` : '')) : ''"
                    @click.native="() => {
                        selectedCourse = copyable.course.id
                    }"
                />
                <div
                    v-if="selectedCourse === copyable.course.id"
                    class="pl-5"
                >
                    <assignment-card
                        v-for="assignment in copyable.assignments"
                        :key="`assignment-${assignment.id}-copy`"
                        :assignment="assignment"
                        @click.native="$emit('copyFormat', assignment.id)"
                    />
                </div>
            </div>
            <div v-if="!copyableFormats">
                <h4>No existing assignments available</h4>
                <hr class="m-0 mb-1"/>
                Only assignments where you have permission to edit are available for copy.
            </div>
        </b-card>
    </div>
</template>

<script>
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import mainCard from '@/components/assets/MainCard.vue'

export default {
    components: {
        assignmentCard,
        mainCard,
    },
    props: ['copyableFormats'],
    data () {
        return {
            selectedCourse: null,
        }
    },
}
</script>
