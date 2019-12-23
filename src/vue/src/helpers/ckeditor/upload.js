class UploadAdapter {
    constructor (loader) {
        /* The file loader instance to use during the upload. */
        this.loader = loader
    }

    /* Starts the upload process. */
    upload () {
        return this.loader.file
            .then(file => new Promise((resolve, reject) => {
                this._initRequest()
                this._initListeners(resolve, reject, file)
                this._sendRequest(file)
            }))
    }

    /* Aborts the upload process. */
    abort () {
        if (this.xhr) {
            this.xhr.abort()
        }
    }

    /* Initializes the XMLHttpRequest object using the URL passed to the constructor. */
    _initRequest () {
        this.xhr = new XMLHttpRequest()
        this.xhr.open('POST', `${CustomEnv.API_URL}/files/`)
        this.xhr.responseType = 'json'
    }

    /* Initializes XMLHttpRequest listeners. */
    _initListeners (resolve, reject, file) {
        const xhr = this.xhr
        const loader = this.loader
        const genericErrorText = `Could not upload file: ${file.name}.`

        xhr.addEventListener('error', () => reject(genericErrorText))
        xhr.addEventListener('abort', () => reject())
        /* eslint-disable-next-line consistent-return */
        xhr.addEventListener('load', () => {
            const response = xhr.response

            if (!response || response.error) {
                return reject(response && response.error ? response.error.message : genericErrorText)
            }

            resolve({ default: response.download_url })
        })

        if (xhr.upload) {
            xhr.upload.addEventListener('progress', (evt) => {
                if (evt.lengthComputable) {
                    loader.uploadTotal = evt.total
                    loader.uploaded = evt.loaded
                }
            })
        }
    }

    _sendRequest (file) {
        const data = new FormData()
        data.append('file', file)
        this.xhr.send(data)
    }
}

export default {
    uploadAdapterPlugin (editor) {
        /* eslint-disable-next-line arrow-body-style */
        editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
            // Configure the URL to the upload script in your back-end here!
            return new UploadAdapter(loader)
        }
    },
}
