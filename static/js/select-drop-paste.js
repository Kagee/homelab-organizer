// Declaration
class SDP {
    static defaultConfig = {
        /* function(msg: string) to show error message.
           Can be null, console.log, alert,
           rendering a bootstrap modal,
           up2u. Default is to print data to console
           based on `debug`.
        */
        showErrorCallback: SDP._logError,
        /* function() to hide error message.
           Useful when you i.e. have to
           hide the error message once it
           is no longer valid. Default null.
        */
        hideErrorCallback: null,
         /* function(file: File) to call when
           a new file has been accepted.
           Default is to print data to console
           based on `debug`.
        */
        newFileCallback: SDP._logNewFile,
        /* wether or not (default true) to replace 
           the file in `fileInputElement` when a new
           file has been accepted.
        */
        autoAssignFileToInput: true,
        /* File input element to listen to events from,
           potentially update based on `autoAssignFileToInput` 
         */
        fileInputElement: "#uploadFile",
        /* Element to use as drop zone */
        dropzoneElement: "#drop_zone",
        /* Acceptable mimetypes for files. Will be used 
           in String.startsWith(), so "image/" will match
           among others, image/png, image/jpeg and image/svg+xml.
        */
           acceptedMimeTypes: ['image/png', 'image/jpeg'],
        /* Wether or not to print debug messages to console.
        */
        debug: false,
    };

    constructor(config) {
        this._config = this.mergeConfig(config);
        window.addEventListener("load",function() {
            dze = document.querySelector(this._config.dropzoneElement);
            dze.addEventListener('drop', this._dropEventHandler);
            dze.addEventListener('dragover', (e) => {e.preventDefault()});
            document.addEventListener('paste', this._pastEventHandler);
        });
    }

    async _dropEventHandler(ev) {
        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
        if (ev.dataTransfer.items) {
        for (i=0; i < ev.dataTransfer.items.length; i++) {
            item = ev.dataTransfer.items[i];
            if (item.kind === "file") {
                console.log("Drophandler item kind file:")
                const file = item.getAsFile();
                if (use_file(file)) {
                    break;
                }
            }
        }
        } else {
            for (i=0; i < ev.dataTransfer.files.length; i++) {
                file = ev.dataTransfer.files[i];
                if (use_file(file)) {
                    break;
                }
            }
        }
    }

    async _pastEventHandler(e) {
        e.preventDefault();
        for (const clipboardItem of e.clipboardData.files) {
            if (this._isAcceptableMIMEType(clipboardItem.type)) {
                    this.use_file(clipboardItem)
            }
        }
    }
    
    mergeConfig(new_config) {
        new_config = !!new_config ? new_config : {} // if undefined

        let tc = typeof(new_config)
        if (tc != "object") {
            console.log(`SDP config was invalid type ${tc}`)
            new_config = {}
        }
        this.D = SDP.defaultConfig.debug || !!new_config.debug
        this.D && console.log("Debug output is enabled")
        let c = {}
        for (let option in SDP.defaultConfig) {
            if (option in new_config) {
                c[option] = new_config[option]
                this.D && console.log(`Non-default config for option ${option}:`, new_config[option])
                delete new_config[option];
            } else {
                c[option] = SDP.defaultConfig[option]
            }
        }
        if (!!new_config) {
            for (let option in new_config) {
                console.log(`Unknown config option '${option}' for SDP config:`, new_config[option])
            }
        }
        return c
    }

    _isAcceptableMIMEType(str) {
        for (let mimeType in acceptedMimeTypes) {
            if (str.startsWith(mimeType)) {
                this.D && console.log(`Accepted MIME type ${str}`)
                return true;
            }
        }
        this.D && console.log(`Rejected MIME type ${str}`)
        return false;
    }

    static _logError(msg) {
        this.D && console.log(msg)
    }

    static _logNewFile(file) {
        this.D && console.log(`A new file has been accepted: `, file)
    }

  }