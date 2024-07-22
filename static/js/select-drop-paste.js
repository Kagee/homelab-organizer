// Declaration
class SDP {
    static defaultConfig = {
        /* function(msg: string) to show error message.
           Can be null, console.log, alert,
           rendering a bootstrap modal,
           up2u. Default is to print data to console
           based on `debug`.
        */
        showErrorCallback: SDP._log,
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
        fileInputElement: "#uploadfile",
        /* Element to use as drop zone */
        dropzoneElement: "#dropzone",
        /* Acceptable MIME types for files. Will be used 
           in String.startsWith(), so "image/" will match
           among others, image/png, image/jpeg and image/svg+xml.
        */
        acceptedMimeTypes: ['image/png', 'image/jpeg'],
        /* Wether or not to print debug messages to console.
        */
        debug: false,
    };
    dze = null;
    fie = null;
    constructor(config) {
        this._config = this._mergeConfig(config);

        window.addEventListener("load", function () {
            /* This must happen here and not in the 
               constructor so the elements are loaded. */
            this.dze = document.querySelector(this._config.dropzoneElement);
            this.fie = document.querySelector(this._config.fileInputElement);

            this.dze.addEventListener('drop', this._dropEventHandler.bind(this));
            this.dze.addEventListener('dragover', (ev) => { ev.preventDefault() });

            this.fie.addEventListener('change', this._fileFieldChange.bind(this));

            document.addEventListener('paste', this._pastEventHandler.bind(this));
        }.bind(this));
    }

    _fileFieldChange(ev) {
        const file = ev.target.files.item(0)
        if (this._isAcceptableMIMEType(file.type)) {
            this._newFile(file);
        } else {
            ev.target.value = null;
            if (this._config.showErrorCallback) {
                this._config.showErrorCallback('Invalid MIME type for selected file:', file.type)
            }
        }
    }

    _dropEventHandler(ev) {
        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
        if (ev.dataTransfer.items) {
            for (let item of ev.dataTransfer.items) {
                if (item.kind === "file") {
                    const file = item.getAsFile();
                    if (this._isAcceptableMIMEType(file.type)) {
                        this._newFile(file);
                        break;
                    }
                }
            }
        } else if (ev.dataTransfer.files) {
            for (let file of ev.dataTransfer.files) {
                if (this._isAcceptableMIMEType(file.type)) {
                    this._newFile(file);
                    break;
                }
            }
        }
    }

    async _pastEventHandler(ev) {
        ev.preventDefault();
        for (const clipboardItem of ev.clipboardData.files) {
            if (this._isAcceptableMIMEType(clipboardItem.type)) {
                this._newFile(clipboardItem)
            }
        }
    }

    _mergeConfig(new_config) {
        new_config = !!new_config ? new_config : {} // if undefined

        let tc = typeof (new_config)
        if (tc != "object") {
            console.log(`SDP config was invalid type ${tc}`)
            new_config = {}
        }
        this.D = SDP.defaultConfig.debug || !!new_config.debug
        this._log("Debug output is enabled")
        let c = {}
        for (let option in SDP.defaultConfig) {
            if (option in new_config) {
                c[option] = new_config[option]
                this._log(`Non-default config for option ${option}:`, new_config[option])
                delete new_config[option];
            } else {
                c[option] = SDP.defaultConfig[option]
            }
        }
        if (!!new_config) {
            for (let option in new_config) {
                this._log(`Unknown config option '${option}' for SDP config:`, new_config[option])
            }
        }
        return c
    }

    _isAcceptableMIMEType(str) {
        for (let mimeType of this._config.acceptedMimeTypes) {
            if (str.startsWith(mimeType)) {
                this._log(`Accepted MIME type: ${str}`)
                return true;
            }
        }
        this._log(`Rejected MIME type: ${str}`)
        return false;
    }

    _newFile(file) {
        if (this._config.hideErrorCallback) {
            this._config.hideErrorCallback()
        }
        if (this._config.autoAssignFileToInput) {
            let container = new DataTransfer();
            container.items.add(file);
            this.fie.files = container.files;
        }
        if (this._config.newFileCallback) {
            this._config.newFileCallback(file)
        }
    }

    _log(msg) {
        this.D && console.log(msg)
    }

    _logNewFile(file) {
        this._log(`A new file has been accepted: `, file)
    }
    
}