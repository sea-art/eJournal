<template>
    <div>
        <div v-if="commentObject2 !== null">
            <div v-for="(commentObject, index) in commentObject2.entrycomments" :key="index">
                <b-row>
                    <b-col cols="2">
                        <img class="profilePic" id="nav-profile-image" slot="button-content" :src="commentObject.author.picture">
                        {{ commentObject.author.name }}
                    </b-col>
                    <b-col cols="10">
                        <b-card class="no-hover" :class="'pink-border'">
                            {{ commentObject.text }}
                        </b-card>
                    </b-col>
                </b-row>
            </div>
        </div>
        <b-row>
            <b-col cols="2">
                <img class="profilePic" id="nav-profile-image" slot="button-content" :src="userData.picture">
            </b-col>
            <b-col cols="10">
                <b-textarea v-model="tempComment" placeholder="Add your beautiful comment here"></b-textarea><br>
                <b-button @click="addComment">Add your comment</b-button>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import userApi from '@/api/user.js'
import entryApi from '@/api/entry.js'

export default {
    props: ['eID'],

    data () {
        return {
            tempComment: '',
            userData: '',
            commentObject2: null
        }
    },
    watch: {
        eID: function () {
            this.newCommentObject = this.commentObject
            this.tempComment = ''
            entryApi.get_entrycomments(this.eID).then(response => { this.commentObject2 = response })
        }
    },
    created () {
        this.getAuthorID()
        this.get_entrycomments()
    },
    methods: {
        getAuthorID: function () {
            userApi.getOwnUserData()
                .catch(_ => alert('Error while loading in user data.'))
                .then(response => { this.userData = response })
        },
        get_entrycomments: function () {
            entryApi.get_entrycomments(this.eID).then(response => { this.commentObject2 = response })
        },
        addComment: function () {
            if (this.tempComment !== '') {
                entryApi.create_entrycomment(this.eID, this.userData.uID, this.tempComment)
                this.commentObject2.entrycomments.push({
                    entrtyID: this.eID,
                    authour: this.userData.name,
                    text: this.tempComment
                })
                this.tempComment = ''
                console.log('derp')
            }
        }
    }
}
</script>
