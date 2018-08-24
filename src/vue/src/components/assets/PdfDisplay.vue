<template>
    <div>
        <h5>
            {{ fileName }}
            <icon v-if="!show" @click.native="handleDownload" name="eye" class="action-icon"/>
            <icon v-if="show" @click.native="handleDownload" name="ban" class="crossed-icon"/>
        </h5>

        <div v-if="show && loaded && numPages !== 0" class="pdf-menu-container">
            <icon name="arrow-left" @click.native="page = (page - 1 > 0) ? page - 1 : numPages" class="action-icon"/>
            <icon name="arrow-right" @click.native="page = (page + 1 > numPages) ? 1 : page + 1" class="action-icon"/>
            <!-- TODO find appropriate icons and decide if rotating is a wanted functionality -->
            <!-- <button @click="rotate += 90">&#x27F3;</button> -->
            <!-- <button @click="rotate -= 90">&#x27F2;</button> -->
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
            userAPI.getUserFile(this.fileName, this.authorUID)
                .then(response => {
                    let blob = new Blob([response.data], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)

                    this.downloadLink = document.createElement('a')
                    this.downloadLink.href = this.fileURL
                    this.downloadLink.download = this.fileName
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
    }
}
</script>

<style lang="sass">
.pdf-menu-container
    text-align: center
</style>
