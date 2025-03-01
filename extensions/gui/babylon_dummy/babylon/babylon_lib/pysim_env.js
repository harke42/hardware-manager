var world_objects = {}


// =====================================================================================================================
class PysimScene extends Scene {
    constructor(id, config) {

        super(id);
        this.config = config
        this.createScene();
    }

    createScene() {
        // --- CAMERA ---
        this.camera = new BABYLON.ArcRotateCamera("Camera", 0, 0, 20, new BABYLON.Vector3(0,0.1,0), this.scene);
        // this.camera.setPosition(new BABYLON.Vector3(-0.02, 2.278,2.24));
        // this.camera.setPosition(new BABYLON.Vector3(0.81, 0.82,1.6));
        // this.camera.setPosition(new BABYLON.Vector3(2.2, 1.7, 2.5));
        this.camera.setPosition(new BABYLON.Vector3(0.02, 1.11, 2.3));
        this.camera.attachControl(this.canvas, true);
        // console.log(this.camera.inputs.attached)
        this.camera.inputs.attached.keyboard.detachControl()
        this.camera.wheelPrecision = 100;
        this.camera.minZ = 0.1
        // --- LIGHTS ---
        this.light1 = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0.5,1,0), this.scene);
        this.light1.intensity = 1

        const gl = new BABYLON.GlowLayer("glow", this.scene);
        gl.intensity = 0

        // --- BACKGROUND ---
        // this.defaultBackgroundColor = new BABYLON.Color3(0.75,0.75,0.75)
        // this.defaultBackgroundColor = new BABYLON.Color3(1,1,1)
        this.defaultBackgroundColor = new BABYLON.Color3(0.75,0.75,0.75)
        this.scene.clearColor = this.defaultBackgroundColor;

        // --- Textbox ---
        this.ui = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("ui", true, this.scene);
        this.textbox_time = new BABYLON.GUI.TextBlock();
        this.textbox_time.fontSize = 40;
        this.textbox_time.text = "";
        this.textbox_time.color = "black";
        this.textbox_time.paddingTop = 3;
        this.textbox_time.paddingLeft = 3;
        this.textbox_time.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        this.textbox_time.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        this.ui.addControl(this.textbox_time);

        this.textbox_status = new BABYLON.GUI.TextBlock();
        this.textbox_status.fontSize = 40;
        this.textbox_status.text = "";
        this.textbox_status.color = "black";
        this.textbox_status.paddingTop = 3;
        this.textbox_status.paddingRight = 30;
        this.textbox_status.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        this.textbox_status.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_RIGHT
        this.ui.addControl(this.textbox_status);


        this.textbox_title = new BABYLON.GUI.TextBlock();
        this.textbox_title.fontSize = 40;
        this.textbox_title.text = "";
        this.textbox_title.color = "black";
        this.textbox_title.paddingTop = 3;
        this.textbox_title.paddingLeft = 3;
        this.textbox_title.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        this.textbox_title.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_CENTER;
        this.ui.addControl(this.textbox_title);

        // --- Coordinate System ---
        this.drawCoordinateSystem(0.25)

        // --- GENERATION OF OBJECTS ---
        this.buildWorld()

        // --- WEBAPP CONFIG ---
        if ('webapp_config' in this.config && this.config['webapp_config'] != null){
            if ('title' in this.config['webapp_config']){
                this.textbox_title.text = this.config['webapp_config']['title']
            }
            if ('record' in this.config['webapp_config']){
                var recorder = new BABYLON.VideoRecorder(this.engine);
                recorder.startRecording(this.config['webapp_config']['record']['file'], this.config['webapp_config']['record']['time']);
            }
            if ('background' in this.config['webapp_config']){
                console.log(new BABYLON.Color3(this.config['webapp_config']['background'][0],this.config['webapp_config']['background'][1],this.config['webapp_config']['background'][2]))
                this.scene.clearColor = new BABYLON.Color3(this.config['webapp_config']['background'][0],this.config['webapp_config']['background'][1],this.config['webapp_config']['background'][2])
            }
        }

        return this.scene;
    }

    buildWorld() {
        // Check if the config has the appropriate entries:
        if (!("world" in this.config)){
            console.warn("No world definition in the config")
            return
        }
        if (!('objects' in this.config['world'])){
            console.warn("No world objects specified in the config")
            return
        }

        // Loop over the config and extract the objects
        for (const [key, value] of Object.entries(this.config['world']['objects'])){
            // Check if the object type is in the object config
            let babylon_object_name
            if (value.object_type in this.config['object_config']){
                babylon_object_name = this.config['object_config'][value.object_type]['BabylonObject']
                let objectPtr = eval(babylon_object_name)
                world_objects[key] = new objectPtr(this.scene, key, value.object_type, value, this.config['object_config'][value.object_type]['config'])

            } else {
                console.warn("Cannot find the object type in the object definition")
            }
        }
    }

    // -----------------------------------------------------------------------------------------------------------------
    drawCoordinateSystem(length) {
        const points_x = [
            ToBabylon([0, 0, 0]),
            ToBabylon([length, 0, 0])
        ]
        const points_y = [
            ToBabylon([0, 0, 0]),
            ToBabylon([0, length, 0])
        ]
        const points_z = [
            ToBabylon([0, 0, 0]),
            ToBabylon([0, 0, length])
        ]
        new BABYLON.Color3(1, 0, 0);
        var line_x = BABYLON.MeshBuilder.CreateLines("line_x", {points: points_x}, this.scene);
        line_x.color = new BABYLON.Color3(1, 0, 0);

        var line_y = BABYLON.MeshBuilder.CreateLines("line_y", {points: points_y}, this.scene);
        line_y.color = new BABYLON.Color3(0, 1, 0);

        var line_z = BABYLON.MeshBuilder.CreateLines("line_z", {points: points_z}, this.scene);
        line_z.color = new BABYLON.Color3(0, 0, 1);
    }

    // -----------------------------------------------------------------------------------------------------------------
    onSample(sample) {
        // console.log(this.camera.position)
        if ('world' in sample){
            for (const [key, value] of Object.entries(sample['world']['objects'])){
                if (key in world_objects){
                    world_objects[key].update(value)
                }
            }
        } else {
            console.warn("No world data in current sample")
        }
        if ('time' in sample){
            this.textbox_time.text = 'Time: ' + sample['time'].toFixed(2) + ' s'
        } else {
            console.warn("No time data in current sample")
        }

        if ('settings' in sample){
            if ('status' in sample['settings']){
                this.textbox_status.text = sample['settings']['status']
            }
            if ('background_color' in sample['settings']){
                if (sample['settings']['background_color'] === 0){
                    this.scene.clearColor = this.defaultBackgroundColor;
                } else {
                    this.scene.clearColor = new BABYLON.Color3(sample['settings']['background_color'][0],sample['settings']['background_color'][1],sample['settings']['background_color'][2])
                }

            }
        }

    }
}