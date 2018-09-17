<template>
    <div>
        <div class="pdf-controls mb-2 unselectable" @click="handleDownload">
            <icon name="align-left"/>
            <i><span>{{ fileName }}</span></i>
        </div>

        <div v-if="show && loaded && numPages !== 0" class="pdf-menu-container">
            <icon name="arrow-left" @click.native="page = (page - 1 > 0) ? page - 1 : numPages" class="action-icon"/>
            <icon name="arrow-right" @click.native="page = (page + 1 > numPages) ? 1 : page + 1" class="action-icon"/>
            <icon name="undo" @click.native="rotate -= 90" class="action-icon"/>
            <icon name="undo" @click.native="rotate += 90" class="action-icon redo"/>
            <icon name="print" @click.native="print" class="action-icon"/>
            <icon @click.native="downloadLink.click()" name="save" class="action-icon"/>
            {{ page }} / {{ numPages }}
            <input v-model.number="page" type="number" min="1" :max="numPages">
        </div>
        <div>
            <div
                v-if="loadedRatio > 0 && loadedRatio < 1"
                style="background-color: green; color: white; text-align: center"
                :style="{ width: loadedRatio * 100 + '%' }">
                {{ Math.floor(loadedRatio * 100) }}%
            </div>
            <pdf
                v-if="show && fileURL"
                :ref="'pdf'"
                :src="fileURL"
                :page="page"
                :rotate="rotate"
                @password="password"
                @progress="loadedRatio = $event"
                @error="error"
                @num-pages="numPages = $event"
                @link-clicked="page = $event"
                @loaded="loaded = true">
            </pdf>
        </div>
    </div>
</template>

<script>
import pdf from 'vue-pdf'
import userAPI from '@/api/user.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        fileName: {
            required: true,
            String
        },
        authorUID: {
            required: true,
            String
        },
        display: {
            default: false
        }
    },
    components: {
        icon,
        pdf
    },
    data () {
        return {
            show: false,
            fileURL: null,
            loadedRatio: 0,
            page: 1,
            numPages: 0,
            rotate: 0,
            loaded: false,
            downloadLink: null
        }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
        password (updatePassword, reason) {
            this.$toasted.error('Password handling is not implemented.')
        },
        error (err) {
            this.$toasted.error(err)
        },
        print () {
            this.$refs.pdf.print()
        },
        fileDownload () {
            userAPI.download(this.authorUID, this.fileName)
                .then(response => {
                    let blob = new Blob([response.data], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)

                    this.downloadLink = document.createElement('a')
                    this.downloadLink.href = this.fileURL
                    this.downloadLink.download = this.fileName
                    document.body.appendChild(this.downloadLink)
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
                .catch(_ => {
                    this.$toasted.error('Error creating file.')
                })
        }
    },
    created () {
        this.show = this.display

        if (this.show) { this.fileDownload() }
    },
    destroy () { this.downloadLink.remove() }
}
</script>

<style lang="sass">
.pdf-menu-container
    text-align: center

.pdf-controls
    &:hover
        cursor: pointer
    span
        text-decoration: underline !important
    svg
        margin-bottom: -2px

.redo
    -moz-transform: scale(-1, 1)
    -webkit-transform: scale(-1, 1)
    -o-transform: scale(-1, 1)
    -ms-transform: scale(-1, 1)
    transform: scale(-1, 1)
</style>
