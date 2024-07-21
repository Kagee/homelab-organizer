// Declaration
class SDP {
    static defaultConfig = {
        /* function(msg: string) to show error message.
           Can be null, console.log, alert,
           rendering a bootstrap modal,
           up2u. Default is to print data to console
           based on `debug`.
        */
        showErrorCallback: SDP._show_error,
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
        newFileCallback: SDP._new_file,
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
        /* Wether or not to print debug messages to console.
        */
        debug: false,
    };

    constructor(config) {
      this._config = this.merge_config();
    }

    merge_config(new_config) {
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

    static _show_error(msg) {
        this.D && console.log(msg)
    }

    static _new_file(file) {
        this.D && console.log(`A new file has been accepted: `, file)
    }

  }