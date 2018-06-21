<template>
    <content-single-columns>
        <!-- <bread-crumb @eye-click="customisePage"/> -->
        <course-participant-card v-for="p in participants" :key="p.uID"
            :uID="p.uID"
            :studentNumber="p.studentNumber"
            :name="p.name"
            :portraitPath="p.portraitPath"
            :role="p.role"/>
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import courseParticipantCard from '@/components/CourseParticipantCard.vue'

export default {
    name: 'CourseUserManagement',
    props: {
        cID: {
            required: true
        }
    },
    data () {
        return {
            participants: [{
                uID: 99,
                studentNumber: 6066364,
                name: 'Maarten Jochem van Keulen',
                portraitPath: '@/assets/logo.png',
                role: 'ta'
            }]
        }
    },
    components: {
        'content-single-columns': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'course-participant-card': courseParticipantCard
    }
}
</script>
