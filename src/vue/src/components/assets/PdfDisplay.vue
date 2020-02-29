<template>
    <div>
        <div
            class="pdf-controls mb-2 unselectable"
            @click="handleDownload"
        >
            <icon name="align-left"/>
            <i><span>{{ file.file_name }}</span></i>
        </div>

        <div
            v-if="show && loaded && numPages !== 0"
            class="pdf-menu-container"
        >
            <icon
                name="arrow-left"
                class="action-icon"
                @click.native="page = (page - 1 > 0) ? page - 1 : numPages"
            />
            <icon
                name="arrow-right"
                class="action-icon"
                @click.native="page = (page + 1 > numPages) ? 1 : page + 1"
            />
            <icon
                name="undo"
                class="action-icon"
                @click.native="rotate -= 90"
            />
            <icon
                name="undo"
                class="action-icon redo"
                @click.native="rotate += 90"
            />
            <icon
                name="print"
                class="action-icon"
                @click.native="print"
            />
            <icon
                name="save"
                class="action-icon"
                @click.native="downloadLink.click()"
            />
            {{ page }} / {{ numPages }}
            <input
                v-model="displayPageNumber"
                :max="numPages"
                type="number"
                min="1"
                @input="validatePageInput"
            />
        </div>
        <div>
            <div
                v-if="loadedRatio > 0 && loadedRatio < 1"
                :style="{ width: loadedRatio * 100 + '%' }"
                style="background-color: green; color: white; text-align: center"
            >
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
                @loaded="loaded = true"
            />
        </div>
    </div>
</template>

<script>
import pdf from 'vue-pdf'
import auth from '@/api/auth.js'
import sanitization from '@/utils/sanitization.js'

export default {
    components: {
        pdf,
    },
    props: {
        file: {
            required: true,
        },
        authorUID: {
            required: true,
            String,
        },
        display: {
            default: false,
        },
        entryID: {
            required: true,
            String,
        },
        nodeID: {
            required: true,
            String,
        },
        contentID: {
            required: true,
            String,
        },
    },
    data () {
        return {
            show: false,
            fileURL: null,
            loadedRatio: 0,
            page: 1,
            displayPageNumber: 1,
            numPages: 0,
            rotate: 0,
            loaded: false,
            downloadLink: null,
        }
    },
    watch: {
        page (val) { this.displayPageNumber = val },
    },
    created () {
        this.show = this.display

        if (this.show) { this.fileDownload() }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
        /* Ensures the input is within range of the PDF pages. */
        validatePageInput (input) {
            const parsed = parseInt(input.data, 10)

            if (parsed < 1) {
                this.page = 1
            } else if (parsed > this.numPages) {
                this.page = this.numPages
            } else if (!Number.isNaN(parsed)) {
                this.page = parseInt(input.data, 10)
            }
        },
        password () {
            this.$toasted.error('Password handling is not implemented.')
        },
        error (err) {
            this.$toasted.error(sanitization.escapeHtml(err))
        },
        print () {
            this.$refs.pdf.print()
        },
        fileDownload () {
            auth.downloadFile(this.file.download_url)
                .then((response) => {
                    try {
                        const blob = new Blob([response.data], { type: response.headers['content-type'] })
                        this.fileURL = window.URL.createObjectURL(blob)

                        this.downloadLink = document.createElement('a')
                        this.downloadLink.href = this.fileURL
                        this.downloadLink.download = this.file.file_name
                        document.body.appendChild(this.downloadLink)
                    } catch (_) {
                        this.$toasted.error('Error creating file.')
                    }
                })
        },
    },
    destroy () { this.downloadLink.remove() },
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
